from .fields import SQLType
from .sql import SQL, WHERE

from types import FunctionType


class BaseOperation:

    def __init__(self, first_operand, second_operand):
        self.first_operand = first_operand
        self.second_operand = second_operand

    def _build_operand(self, operand):
        if isinstance(operand, str):
            value = operand
        else:
            value = operand.build()

        return value

    def _build_operand_values(self):
        first_value = self._build_operand(self.first_operand)
        second_value = self._build_operand(self.second_operand)

        return first_value, second_value

    def __add__(self, other):
        return OR(self, other)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            if (self.first_operand == other.first_operand and self.second_operand == other.second_operand) or \
               (self.first_operand == other.second_operand and self.second_operand == other.first_operand):

                return True

        return False


class AND(BaseOperation):

    def __init__(self, first_operand, second_operand):
        super(AND, self).__init__(first_operand, second_operand)

    def build(self):
        first_value, second_value = self._build_operand_values()

        return WHERE._and(first_value, second_value)


class OR(BaseOperation):

    def __init__(self, first_operand, second_operand):
        super(OR, self).__init__(first_operand, second_operand)

    def build(self):
        first_value, second_value = self._build_operand_values()

        return WHERE._or(first_value, second_value)


class Q:

    def __check_valid_count_kwargs(self, **kwargs):
        if len(kwargs) != 1:
            raise AttributeError(f"Class {SQL.WHERE.__name__} takes one key word argument. \
                                    Received {len(kwargs)} arguments {kwargs}")

    def __check_valid_method_name(self):
        if self.arg_method_name not in WHERE.__dict__.keys():
            raise AttributeError(f"Unknown condition method '{self.arg_method_name}'")

    def __set_condition_method(self):
        self.__check_valid_method_name()
        self.condition_method = WHERE.__dict__[self.arg_method_name]

    def __get_arg_name(self, **kwargs):
        keys = kwargs.keys()
        keys_iterator = iter(keys)
        arg_name = next(keys_iterator)
        return arg_name

    def __set_args(self, **kwargs):
        self.__check_valid_count_kwargs(**kwargs)

        _arg_name = self.__get_arg_name(**kwargs)
        self.arg_value = kwargs[_arg_name]

        if _arg_name.find('__') != -1:
            self.arg_name, method_name = _arg_name.split('__')
            self.arg_method_name = f'_{method_name}_value'
        else:
            self.arg_name = _arg_name
            self.arg_method_name = WHERE._eq_value.__name__

    def __init__(self, **kwargs):
        self.__set_args(**kwargs)
        self.__set_condition_method()
        self.command = None

    def build(self):
        function = getattr(WHERE, self.arg_method_name)
        return function(column_name=self.arg_name,
                        value=SQLType.convert(self.arg_value))

    def __or__(self, other):
        return OR(self, other)

    def __and__(self, other):
        return AND(self, other)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            if (self.arg_name == other.arg_name and
               self.arg_value == other.arg_value and
               self.arg_method_name == other.arg_method_name):

                return True

        return False
