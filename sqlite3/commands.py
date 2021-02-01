from base import (
    SELECT, _SELECT, _FROM, _JOIN, _WHERE, _ORDER_BY, _LIMIT, _OFFSET, _GROUP_BY, _HAVING,
    CREATE, _CREATE_TABLE, _CREATE_COLUMN,
    ADD, _INSERT_INTO, _VALUES,
    UPDATE, _ORDER, _UPDATE, _SET,
    DELETE, _DELETE_FROM
)
from commands import SQLType


class BaseCommand: # TODO Abstract class
    sql: str

    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns

    def build(self):
        pass

class Select(BaseCommand): # TODO

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
        super(Add, self).__init__(table_name, columns)
        self.values = []

    def __insert_into(self):
        formatted_columns = ', '.join(self.columns)
        insert_into = _INSERT_INTO.format(table_name=self.table_name, columns=formatted_columns)
        return insert_into

    def __covnert_types_values(self, values_list): # Вынести в отдельный класс
        corrected_values = [SQLType.convert(value) for value in values_list]

        return corrected_values

    def __convert_values(self): # Вынести в отдельный класс
        converted_values = []
        for values_list in self.values:
            converted_values.append(self.__covnert_types_values(values_list))
        return converted_values

    def __values(self):
        corrected_values = self.__convert_values()
        values_list = ['(' + ', '.join(value) + ')' for value in corrected_values]
        formatted_values = ', '.join(values_list)
        values = _VALUES.format(values=formatted_values)
        return values

    def add(self, **kwargs): # ???????????
        self.values.append(values)

    def build_sql(self):
        insert_into = self.__insert_into()
        values = self.__values()
        sql_query = ADD.format(INSERT_INTO=insert_into, VALUES=values)
        return sql_query

class Update(BaseCommand): # TODO

    def build_sql(self):
        pass

class Delete(BaseCommand): # TODO

    def __init__(self, table_name, columns):
        pass

    def __delete_from(self):
        pass

    def __where(self):
        pass

    def __order_by(self):
        pass

    def __limit(self):
        pass

    def __offset(self):
        pass

    def add(self, values):
        pass

    def build_sql(self):
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

    def add(self, values): # ????????????????
        add_command = None

        for command in self.commands:
            if isinstance(command, Add):
                add_command = command
                break

        if add_command is None:
            add_command = Add(table_name=self.table_name, columns=self.fields)
            self.commands.append(add_command)

        add_command.add_values(values=values)
