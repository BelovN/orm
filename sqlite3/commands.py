from base import (
    SELECT, _SELECT, _FROM, _JOIN, _WHERE, _ORDER_BY, _LIMIT, _OFFSET, _GROUP_BY, _HAVING,
    CREATE, _CREATE_TABLE, _CREATE_COLUMN,
    ADD, _INSERT_INTO, _VALUES,
    UPDATE, _ORDER, _UPDATE, _SET,
    DELETE, _DELETE_FROM
)
from collections import namedtuple


class BaseCommand:
    sql: str

    def build(self):
        pass


class Select(BaseCommand):

    @staticmethod
    def build():
        pass

class Create(BaseCommand):
    # TODO: Сделать table_constraints FOREIGN_KEY
    # TODO: Проверить возможныезначения PRIMARY_KEY

    def create_table(self):
        pass

    def create_column(self):
        pass

    def build(self, table_name, if_not_exists=False):
        sql_query = CREATE
        CREATE_TABLE = _CREATE_TABLE.format(if_not_exists)
        pass

class Add(BaseCommand):

    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns
        self.values = []

    def __insert_into(self):
        formatted_columns = ', '.join(self.columns)
        insert_into = _INSERT_INTO.format(table_name=self.table_name, columns=formatted_columns)
        return insert_into

    def __correct_types(self):
        corrected_values = []

        for value in self.values:
            corrected = None

            if isinstance(value, str):
                corrected = '\'' + value + '\''
            elif value is None:
                corrected = "NULL"
            else:
                corrected = str(value)

            corrected_values.append(corrected)

        return corrected_values

    def __convert_values(self):
        converted_values = []
        for values in self.values:
            pass

    def __values(self):
        # corrected_values = self.__correct_types()
        values_list = ['(' + ', '.join(value) + ')' for value in corrected_values]
        formatted_values = ', '.join(values_list)
        values = _VALUES.format(values=formatted_values)
        return values

    def add_values(self, values):
        self.values.append(values)

    def build_sql(self):
        insert_into = self.__insert_into()
        values = self.__values()
        sql_query = ADD.format(INSERT_INTO=insert_into, VALUES=values)
        return sql_query


class Update(BaseCommand):

    def build():
        pass


class Delete(BaseCommand):
    pass


class Builder:
    commands = []

    def __init__(self, table_name, fields):
        self.table_name = table_name
        self.fields = fields

    def build(self):
        builded = []
        for command in self.commands:
            builded.append(command.build_sql())

        return '\n '.join(builded)

    def add(self, instance):
        add_command = None

        for command in self.commands:
            if isinstance(command, Add):
                add_command = command
                break

        if add_command is None:
            add_command = Add(table_name=self.table_name, columns=self.fields)
            self.commands.append(add_command)

        add_command.add_values(values=list(instance))
        # import pdb; pdb.set_trace()
