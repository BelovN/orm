from .query import Q
from .sql import SQL
from .fields import SQLType


class BaseCommand:

    def __init__(self, table_name):
        self.table_name = table_name
        self._can_add = True

    @staticmethod
    def _convert_values(values):
        converted = [SQLType.convert(v) for v in values]
        return converted

    def check_intersection(self, other):
        return self.where.check_intersection(other)


class Create(BaseCommand):

    def __init__(self, table_name, columns,
                 if_not_exists=False, without_rowid=False):

        super(Create, self).__init__(table_name)
        self.columns = columns
        self.if_not_exists = if_not_exists
        self.without_rowid = without_rowid

    def build_sql(self):
        sql_columns = []

        for column in self.columns.values():
            sql_columns.append(
                (column.name, column._type.name, column.default, column.not_null, column.primary_key)
            )

        return SQL.create(
            table_name=self.table_name, columns=sql_columns,
            if_not_exists=self.if_not_exists, without_rowid=self.without_rowid
        )

    def check_can_add(self, other):
        return False


class Add(BaseCommand):

    def __init__(self, table_name, columns, values):
        super(Add, self).__init__(table_name)
        self.columns = columns
        self.values = [values]
        self.value_q = []

        for value_list in self.values:
            q = None
            for column, value in zip(self.columns, value_list):
                kwargs = {column: value}
                q = Q(**kwargs) | q

            self.value_q.append(q)

    def build_sql(self):
        self.converted_values = [self._convert_values(values_list) for values_list in self.values]

        return SQL.add(
            table_name=self.table_name, columns=self.columns.keys(), values=self.converted_values
        )

    def check_can_add(self, other):
        return True

    def __add__(self, other):
        self.values += other.values
        del other
        return self

    def __str__(self):
        return 'ADD ' + str(self.values[0])


class Update(BaseCommand):

    def __init__(self, table_name, columns, values,
                 where, order_by=None, limit=None):

        super(Update, self).__init__(table_name)

        self.columns = columns
        self.values = values
        self.where = where

        self.order_by = order_by
        self.limit = limit

    def __remove_empty(self, values, columns):
        clear_values = []
        clear_columns = []
        for value, column in zip(values, columns):
            if value is not None:
                clear_values.append(value)
                clear_columns.append(column)

        return clear_values, clear_columns

    def build_sql(self):
        clear_values, clear_columns = self.__remove_empty(
            values=self.values, columns=self.columns.keys()
        )
        sql_values = self._convert_values(clear_values)

        return SQL.update(
            table_name=self.table_name, columns=clear_columns, values=sql_values,
            row_filter=self.where.build(), limit=self.limit, order_by=self.order_by
        )

    def check_can_add(self, other):
        if isinstance(other, Update):
            if (self.where == other.where and
               self.limit == other.limit and
               self.order_by == other.order_by):

                return True

        return False

    def __add__(self, other):
        for i, value in enumerate(other.values):
            if value is not None:
                self.values[i] = value

        del other
        return self

    def __str__(self):
        return 'UPDATE ' + str(self.values[0]) + ' ' + str(self.where)


class Delete(BaseCommand):

    def __init__(self, table_name, where, limit=None, offset=None):
        super(Delete, self).__init__(table_name)
        self.where = where
        self.limit = limit
        self.offset = offset

        if limit is not None:
            self._can_add = False

    def build_sql(self):
        return SQL.delete(
            table_name=self.table_name, row_filter=self.where.build(),
            limit=self.limit, offset=self.offset
        )

    def check_can_add(self, other):
        if self.limit == other.limit and self.offset == other.offset:
            return True

        return False

    def __add__(self, other):
        self.where += other.where
        del other
        return self

    def __str__(self):
        return 'DELETE ' + str(self.where)


class Select(BaseCommand):

    def __init__(self, distinct, columns, _from, tables_list, where, order_by):
        self.distinct = distinct
        self.columns = columns
        self._from = _from
        self.tables_list = tables_list
        self.where = where
        self.order_by = order_by

    def build_sql(self):
        return SQL.select(
            self.distinct, self.columns, self.tables_list, self.where, self.order_by
        )


class Builder:

    def __init__(self, table_name, fields):
        self.table_name = table_name
        self.fields = fields
        self.commands = {
            'DELETE': [],
            'ADD': [],
            'UPDATE': [],
            'CREATE': [],
        }
        self.builded = []
        self.primary_key_fields = [
            field_name for field_name, field in self.fields.items() \
                if hasattr(field, 'primary_key') and field.primary_key
        ]
        self.__stack_commands = []

    def build(self):
        for command in self.__stack_commands:
            self.builded.append(command.build_sql())

        return '\n'.join(self.builded)

    def __add_command(self, type_command, new_command):
        for command in self.commands[type_command]:
            if command.check_can_add(new_command):
                command += new_command
                return

        self.__stack_commands.append(new_command)
        self.commands[type_command].append(new_command)

    def clear(self):
        self.__stack_commands.clear()

        for command_type in self.commands.keys():
            self.commands[command_type] = []

        self.builded.clear()

    def delete(self, where, limit=None, offset=None):
        new_command = Delete(
            table_name=self.table_name, where=where, limit=limit, offset=offset
        )
        self.__add_command(type_command='DELETE', new_command=new_command)

    def __add_validation(self, new_command):

        for command in self.commands['ADD']:
            is_unique = True
            for pk_field in self.primary_key_fields:
                num_field = list(new_command.columns.keys()).index(pk_field)
                is_unique &= not (new_command.values[0][num_field] == command.values[0][num_field])

            if not is_unique:
                print(f"Primary key violation in command {new_command}")
                return False

        return True

    def add(self, values):
        new_command = Add(
            table_name=self.table_name,
            columns=self.fields,
            values=values
        )
        self.__add_validation(new_command)
        self.__add_command(type_command='ADD', new_command=new_command)

    def update(self, values, where, order_by=None, limit=None):
        new_command = Update(
            table_name=self.table_name, columns=self.fields, values=values,
            where=where, limit=limit, order_by=order_by
        )
        self.__add_command(type_command='UPDATE', new_command=new_command)

    def create(self, if_not_exists=False, without_rowid=False):
        new_command = Create(
            table_name=self.table_name, columns=self.fields,
            if_not_exists=if_not_exists, without_rowid=without_rowid
        )
        self.__add_command(type_command='CREATE', new_command=new_command)

    def select(self, distinct, columns, _from, tables_list, where, order_by):
        new_command = Select(
            distinct=distinct, columns=columns, _from=_from,
            tables_list=tables_list, where=where, order_by=order_by
        )
        return new_command.build_sql()
