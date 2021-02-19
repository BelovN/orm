from abc import ABC, abstractmethod

from .fields import SQLType
from .sql import WHERE


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

    def get_args(self):
        return self.first_operand.get_args() + self.second_operand.get_args()

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

    def __get_arg_name(self):
        keys = self.kwargs.keys()
        keys_iterator = iter(keys)
        arg_name = next(keys_iterator)
        return arg_name

    def __set_args(self):
        _arg_name = self.__get_arg_name()
        self.arg_value = self.kwargs[_arg_name]

        if _arg_name.find('__') != -1:
            self.arg_name, method_name = _arg_name.split('__')
            self.arg_method_name = method_name
        else:
            self.arg_name = _arg_name
            self.arg_method_name = WHERE.eq.__name__

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        QValidator.validate(QValidatorCountKwargs, self)

        self.__set_args()
        QValidator.validate(QValidatorMethodName, self)

    def build(self):
        function = getattr(WHERE, self.arg_method_name)
        return function(column_name=self.arg_name,
                        value=SQLType.convert(self.arg_value))

    def get_args(self):
        return [{'arg_name': self.arg_name, 'arg_value': self.arg_value, 'method': self.arg_method_name}]

    def __or__(self, other):
        if other is None:
            return self
        return OR(self, other)

    def __and__(self, other):
        if other is None:
            return self
        return AND(self, other)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            if (self.arg_name == other.arg_name and
               self.arg_value == other.arg_value and
               self.arg_method_name == other.arg_method_name):

                return True

        return False


class QBaseValidator(ABC):

    @staticmethod
    @abstractmethod
    def validate(query: Q):
        pass


class QValidatorCountKwargs(QBaseValidator):

    @staticmethod
    @abstractmethod
    def validate(query: Q):
        if len(query.kwargs) != 1:
            raise AttributeError(f"Class {WHERE.__name__} takes one key word argument. " \
                                 f"Received {len(query.kwargs)} arguments {query.kwargs}")


class QValidatorMethodName(QBaseValidator):

    @staticmethod
    @abstractmethod
    def validate(query: Q):
        if query.arg_method_name not in WHERE.__dict__.keys():
            raise AttributeError(f"Unknown condition method '{query.arg_method_name}'")


class QValidator:

    @staticmethod
    def validate(validator: QBaseValidator, query: Q):
        validator.validate(query)
