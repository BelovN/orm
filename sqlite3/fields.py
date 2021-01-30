from enum import Enum
from typing import TypeVar


FIELD_TYPES = TypeVar('FIELD_TYPES', int, str, bytes)


class SQLType(Enum):
    NULL = 1
    INTEGER = 2
    REAL = 3
    TEXT = 4
    BLOB = 5


class BaseField:
    name: str
    value: FIELD_TYPES
    _type: SQLType
    default: FIELD_TYPES
    not_null: bool

    def __init__(self, name, not_null=False, default=None):
        self.name = name
        self.not_null = not_null
        self.default = default

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise Exception(f"Cannot change value of {name}.")
        self.__dict__[name] = value


class IntegerField(BaseField):
    primary_key: bool
    _type: SQLType = SQLType.INTEGER

    def __init__(self, name, not_null=False, default=None, primary_key=False):
        super(IntegerField, self).__init__(name=name, not_null=not_null, default=default)

        self.primary_key = primary_key

    def __setattr__(self, name, value):
        super(IntegerField, self).__setattr__(name, value)


class RealField(BaseField):
    _type: SQLType = SQLType.REAL

    def __init__(self, name, not_null=False, default=None):
        super(RealField, self).__init__(name=name, not_null=not_null, default=default)

    def __setattr__(self, name, value):
        super(RealField, self).__setattr__(name, value)


class TextField(BaseField):
    _type: SQLType = SQLType.TEXT

    def __init__(self, name, not_null=False, default=None):
        super(TextField, self).__init__(name=name, not_null=not_null, default=default)

    def __setattr__(self, name, value):
        super(TextField, self).__setattr__(name, value)


class BLOBField(BaseField):
    _type: SQLType = SQLType.BLOB

    def __init__(self, name, not_null=False, default=None):
        super(BLOBField, self).__init__(name=name, not_null=not_null, default=default)

    def __setattr__(self, name, value):
        super(BLOBField, self).__setattr__(name, value)
