from datetime import datetime
from enum import Enum
from typing import TypeVar


FIELD_TYPES = TypeVar('FIELD_TYPES', int, str, bytes)


class SQLType(Enum):
    NULL = 1
    INTEGER = 2
    REAL = 3
    TEXT = 4
    BLOB = 5
    DATE = 6

    @classmethod
    def convert(cls, value):
        if isinstance(value, str):
            converted = '\"' + value + '\"'

        elif value is None:
            converted = cls.NULL.name

        elif isinstance(value, int):
            converted = str(value)

        elif isinstance(value, tuple):
            converted = []
            for i, v in enumerate(value):
                converted.append(SQLType.convert(v))
            converted = tuple(converted)

        elif isinstance(value, list):
            converted = []
            for i, v in enumerate(value):
                converted.append(SQLType.convert(v))

        elif isinstance(value, datetime):
            converted = '\"' + value.strftime('%Y-%m-%d %H:%M:%S') + '\"'

        else:
            raise ValueError(f"Unknown type {type(value)} to convert")

        return converted


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
        super(IntegerField, self).__init__(name=name,
                                           not_null=not_null,
                                           default=default)

        self.primary_key = primary_key

    def check_type_value(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Value of {self._type.name} field must be instance of {int}")

    def __setattr__(self, name, value):
        super(IntegerField, self).__setattr__(name, value)


class RealField(BaseField):
    _type: SQLType = SQLType.REAL

    def __init__(self, name, not_null=False, default=None):
        self.primary_key = False
        super(RealField, self).__init__(name=name,
                                        not_null=not_null,
                                        default=default)

    def check_type_value(self, value):
        if not isinstance(value, float):
            raise TypeError(f"Value of {self._type.name} field must be instance of {float}")

    def __setattr__(self, name, value):
        super(RealField, self).__setattr__(name, value)


class TextField(BaseField):
    _type: SQLType = SQLType.TEXT

    def __init__(self, name, not_null=False, default=None):
        self.primary_key = False
        super(TextField, self).__init__(name=name,
                                        not_null=not_null,
                                        default=default)

    def check_type_value(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Value of {self._type.name} field must be instance of {str}")

    def __setattr__(self, name, value):
        super(TextField, self).__setattr__(name, value)


class BLOBField(BaseField):
    _type: SQLType = SQLType.BLOB

    def __init__(self, name, not_null=False, default=None):
        self.primary_key = False
        super(BLOBField, self).__init__(name=name,
                                        not_null=not_null,
                                        default=default)

    def check_type_value(self, value):
        if not isinstance(value, bytes):
            raise TypeError(f"Value of {self._type.name} field must be instance of {bytes}")

    def __setattr__(self, name, value):
        super(BLOBField, self).__setattr__(name, value)


class DateField(BaseField):
    _type: SQLType = SQLType.DATE

    def __init__(self, name, not_null=False, default=None):
        self.primary_key = False
        super(DateField, self).__init__(name=name,
                                        not_null=not_null,
                                        default=default)

    def check_type_value(self, value):
        if not isinstance(value, datetime):
            raise TypeError(f"Value of {self._type.name} field must be instance of {datetime}")

    def __setattr__(self, name, value):
        super(DateField, self).__setattr__(name, value)
