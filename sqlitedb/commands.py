from .sql import SQL
from .fields import SQLType


class BaseCommand:

    def __init__(self, table_name):
        self.table_name = table_name
        self._can_add = True

    def _convert_values(self, values):
        converted = [SQLType.convert(v) for v in values]
        return converted


class Create(BaseCommand):

    def __init__(self, table_name, columns,
                 if_not_exists=False, without_rowid=False):

        super(Create, self).__init__(table_name)
        self.columns = columns
        self.if_not_exists = if_not_exists
        self.without_rowid = without_rowid

    def build(self):
        return SQL.create(
            table_name=self.table_name,
            columns=self.columns,
            if_not_exists=self.if_not_exists,
            without_rowid=self.without_rowid
        )

    def check_can_add(self, other):
        return False


class Add(BaseCommand):

    def __init__(self, table_name, columns, values):
        super(Add, self).__init__(table_name)
        self.columns = columns
        self.values = [self._convert_values(values)]

    def build_sql(self):
        return SQL.add(
            table_name=self.table_name,
            columns=self.columns,
            values=self.values
        )

    def check_can_add(self, other):
        return True

    def __add__(self, other):
        self.values += other.values
        del other
        return self


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
        clear_values, clear_columns = self.__remove_empty(values=self.values,
                                                          columns=self.columns)
        sql_values = self._convert_values(clear_values)
        return SQL.update(
            table_name=self.table_name, columns=clear_columns,
            values=sql_values, row_filter=self.where.build(),
            limit=self.limit, order_by=self.order_by
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
            table_name=self.table_name,
            row_filter=self.where.build(),
            limit=self.limit,
            offset=self.offset
        )

    def check_can_add(self, other):
        if self.limit == oher.limit and self.offset == other.offset:
            return True

        return False

    def __add__(self, other):
        self.where += other.where
        del other
        return self


class Builder:
    __priorety = ['DELETE', 'ADD', 'UPDATE']

    def __init__(self, table_name, fields):
        self.table_name = table_name
        self.fields = fields
        self.commands = {
            'DELETE': [],
            'ADD': [],
            'UPDATE': [],
        }

    def build(self):
        self.builded = []

        for type_command in self.__priorety:
            for command in self.commands[type_command]:
                self.builded.append(command.build_sql())

        return '\n'.join(self.builded)

    def __add_command(self, type_command, new_command):
        for command in self.commands[type_command]:
            if command.check_can_add(new_command):
                command += new_command
                return

        self.commands[type_command].append(new_command)

    def clear(self):
        for key in self.commands.keys():
            self.commands[key] = []

        self.builded.clear()

    def delete(self, where, limit=None, offset=None):
        new_command = Delete(
            table_name=self.table_name,
            where=where,
            limit=limit,
            offset=offset
        )
        self.__add_command(type_command='DELETE', new_command=new_command)

    def add(self, values):
        new_command = Add(
            table_name=self.table_name,
            columns=self.fields,
            values=values
        )
        self.__add_command(type_command='ADD', new_command=new_command)

    def update(self, values, where, order_by=None, limit=None):
        new_command = Update(
            table_name=self.table_name,
            columns=self.fields,
            values=values,
            where=where,
            limit=limit,
            order_by=order_by
        )
        self.__add_command(type_command='UPDATE', new_command=new_command)
