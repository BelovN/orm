
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

DB_NAME = 'database.db'
