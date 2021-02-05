
class SQL:

    _WHERE = """WHERE {row_filter}"""

    _ORDER_BY = """ORDER BY {columns}"""

    _LIMIT = """DESC LIMIT {count}"""

    _OFFSET = """OFFSET {offset}"""

    _GROUP_BY = """GROUP BY {column}"""

    CREATE = """{create_table} ({create_columns}) {without_rowid};"""

    _CREATE_TABLE = """CREATE TABLE {if_not_exists} {table_name}"""

    _IF_NOT_EXISTS = """IF NOT EXISTS"""

    _WITHOUT_ROWID = """WITHOUT ROWID"""

    _CREATE_COLUMN = """{column_name} {data_type} {default} {not_null} {primary_key}"""

    _DEFAULT = """DEFAULT {default}"""

    _NOT_NULL = "NOT NULL"

    _PRIMARY_KEY = "PRIMARY KEY"

    ADD = """{insert_into} {values};"""

    _INSERT_INTO = """INSERT INTO {table_name} ({columns})"""

    _VALUES = """VALUES {values}"""

    UPDATE = """{update} {set} {where} {order_by} {limit};"""

    _UPDATE = """UPDATE {table_name}"""

    _SET = """SET {set_value}"""

    _SET_VALUE = """{column} = {value}"""

    DELETE = """{delete_from} {where} {limit} {offset};"""

    _DELETE_FROM = """DELETE FROM {table_name}"""

    @staticmethod
    def add(table_name, columns, values):
        sql_insert_into = SQL.__insert_into(table_name, columns)
        sql_values = SQL.__values(values)

        return SQL.ADD.format(insert_into=sql_insert_into, values=sql_values)

    @staticmethod
    def create(table_name, columns, if_not_exists=False, without_rowid=False):
        sql_create_table = SQL.__create_table(table_name, if_not_exists)

        sql_columns = []
        for column_name, data_type, default, not_null, primary_key in columns:
            sql_columns.append(SQL.__create_column(column_name=column_name,
                                                   data_type=data_type,
                                                   default=default,
                                                   not_null=not_null,
                                                   primary_key=primary_key))

        sql_create_columns = ', '.join(sql_columns)
        sql_without_rowid = SQL.__without_rowid(without_rowid)

        return SQL.CREATE.format(create_table=sql_create_table,
                                 create_columns=sql_create_columns,
                                 without_rowid=sql_without_rowid)

    @staticmethod
    def delete(table_name, row_filter, limit=None, offset=None):
        sql_delete_from = SQL.__delete_from(table_name)
        sql_where = SQL.__where(row_filter)
        sql_limit = SQL.__limit(limit)
        sql_offset = SQL.__offset(offset)

        return SQL.DELETE.format(delete_from=sql_delete_from, where=sql_where, limit=sql_limit, offset=sql_offset)

    @staticmethod
    def update(table_name, columns, values, row_filter, order_by=None, limit=None):
        sql_update = SQL.__update(table_name)
        sql_set = SQL.__set(columns, values)
        sql_where = SQL.__where(row_filter)
        sql_order_by = SQL.__order_by(order_by)
        sql_limit = SQL.__limit(limit)

        return SQL.UPDATE.format(update=sql_update, set=sql_set, where=sql_where, order_by=sql_order_by, limit=sql_limit)

    @staticmethod
    def __delete_from(table_name):
        return SQL._DELETE_FROM.format(table_name=table_name)

    @staticmethod
    def __where(row_filter):
        return SQL._WHERE.format(row_filter=row_filter)

    @staticmethod
    def __order_by(columns):
        if columns:
            sql_columns = ', '.join(columns)

            return SQL._ORDER_BY.format(columns=sql_columns)
        else:
            return ''

    @staticmethod
    def __limit(count):
        if count:
            return SQL._LIMIT.format(count=str(count))
        else:
            return ''

    @staticmethod
    def __offset(offset):
        if offset:
            return SQL._OFFSET.format(offset=offset)
        else:
            return ''

    @staticmethod
    def __create_table(table_name, if_not_exists=False):
        sql_if_not_exists = SQL.__if_not_exists(if_not_exists)

        return SQL._CREATE_TABLE.format(table_name=table_name, if_not_exists=sql_if_not_exists)

    @staticmethod
    def __if_not_exists(if_not_exists=False):
        if if_not_exists:
            return SQL._IF_NOT_EXISTS
        else:
            return ''

    @staticmethod
    def __without_rowid(without_rowid=False):
        if without_rowid:
            return SQL._WITHOUT_ROWID
        else:
            return ''

    @staticmethod
    def __create_column(column_name, data_type, default=None,
                        not_null=True, primary_key=False):

        sql_default = SQL.__default(default)
        sql_not_null = SQL.__not_null(not_null)
        sql_primary_key = SQL.__primary_key(primary_key)

        return SQL._CREATE_COLUMN.format(column_name=column_name,
                                         data_type=data_type,
                                         default=sql_default,
                                         not_null=sql_not_null,
                                         primary_key=sql_primary_key)

    @staticmethod
    def __default(default):
        if default:
            return SQL._DEFAULT.format(default=default)
        else:
            return ''

    @staticmethod
    def __not_null(not_null):
        if not_null:
            return SQL._NOT_NULL
        else:
            return ''

    @staticmethod
    def __primary_key(primary_key):
        if _primary_key:
            return SQL._PRIMARY_KEY
        else:
            return ''

    @staticmethod
    def __set(columns, values):
        set_values = []

        for column, value in zip(columns, values):
            set_values.append(SQL._SET_VALUE.format(column=column, value=value))

        sql_set_value = ', '.join(set_values)

        return SQL._SET.format(set_value=sql_set_value)

    @staticmethod
    def __update(table_name):
        return SQL._UPDATE.format(table_name=table_name)

    @staticmethod
    def __insert_into(table_name, columns):
        sql_columns = ', '.join(columns)

        return SQL._INSERT_INTO.format(table_name=table_name, columns=sql_columns)

    @staticmethod
    def __values(values):
        values_list = ['(' + ', '.join(v) + ')' for v in values]
        sql_values = ', '.join(values_list)

        return SQL._VALUES.format(values=sql_values)


class WHERE:

    _EQ = "{column_name} = {value}"

    _NEQ = "{column_name} <> {value}"

    _IN = "{column_name} IN {value}"

    _LIKE = "{column_name} LIKE {value}"

    _BETWEEN = "({column_name} BETWEEN {less_value} AND {more_value})"

    _LT = "{column_name} < {value}"

    _GT = "{column_name} > {value}"

    _LTE = "{column_name} <= {value}"

    _GTE = "{column_name} >= {value}"

    _AND = """({first_value} AND {second_value})"""

    _OR = """({first_value} OR {second_value})"""

    @staticmethod
    def _and(first_value, second_value):
        return WHERE._AND.format(first_value=first_value, second_value=second_value)

    @staticmethod
    def _or(first_value, second_value):
        return WHERE._OR.format(first_value=first_value, second_value=second_value)

    @staticmethod
    def _eq_value(column_name, value):
        return WHERE._EQ.format(column_name=column_name, value=value)

    @staticmethod
    def _neq_value(column_name, value):
        return WHERE._NEQ.format(column_name=column_name, value=value)

    @staticmethod
    def _in_value(column_name, value):
        sql_values = '(' + ', '.join(value) + ')'
        return WHERE._IN.format(column_name=column_name, value=sql_values)

    @staticmethod
    def _like_value(column_name, value):
        return WHERE._LIKE.format(column_name=column_name, value=value)

    @staticmethod
    def _between_value(column_name, value):
        return WHERE._BETWEEN.format(column_name=column_name, less_value=value[0], more_value=value[1])

    @staticmethod
    def _lt_value(column_name, value):
        return WHERE._LT.format(column_name=column_name, value=value)

    @staticmethod
    def _gt_value(column_name, value):
        return WHERE._GT.format(column_name=column_name, value=value)

    @staticmethod
    def _lte_value(column_name, value):
        return WHERE._LTE.format(column_name=column_name, value=value)

    @staticmethod
    def _gte_value(column_name, value):
        return WHERE._GTE.format(column_name=column_name, value=value)
