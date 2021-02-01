SELECT = """{SELECT} {FROM} {JOIN} {WHERE} {ORDER_BY} {LIMIT} {OFFSET} {GROUP_BY} {HAVING};
"""

_SELECT = """SELECT {DISTINCT} {columns}"""

_FROM = """FROM {tables}"""

_JOIN = """JOIN {table_name} ON {join_condition}"""

_WHERE = """WHERE {row_filter}"""

_ORDER_BY = """ORDER BY {column}"""

_LIMIT = """LIMIT {count}"""

_OFFSET = """OFFSET {offset}"""

_GROUP_BY = """GROUP BY {column}"""

_HAVING = """HAVING {group_filter}"""

CREATE = """{CREATE_TABLE} ({СREATE_COLUMN} {table_constraints}) {WITHOUT_ROWID};"""

_CREATE_TABLE = """CREATE TABLE {IF_NOT_EXISTS} {table_name}"""

_CREATE_COLUMN = """{column_name} {data_type} {DEFAULT} {NULL} {PRIMARY_KEY},"""

ADD = """{INSERT_INTO} {VALUES};"""

_INSERT_INTO = """INSERT INTO {table_name} ({columns})"""

_VALUES = """VALUES {values}"""

UPDATE = """{UPDATE} {SET} {WHERE} {ORDER} {LIMIT};"""

_ORDER = """ORDER"""

_UPDATE = """UPDATE {table_name}"""

_SET = """SET {column} = {value}"""

DELETE = """{DELETE_FROM} {WHERE} {ORDER_BY} {LIMIT} {OFFSET};"""

_DELETE_FROM = """DELETE FROM {table_name}"""
