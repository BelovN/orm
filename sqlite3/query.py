from types import FunctionType

class Q:

    def __check_valid_count_kwargs(self, **kwargs):
        if len(kwargs) != 1:
            raise AttributeError(f"Class {self.__class__.__name__} takes one key word argument. \
                                    Received {len(kwargs)} arguments {kwargs}")

    def __check_valid_method_name(self):
        if self.arg_method_name not in self.__class__.__dict__.keys():
            raise AttributeError(f"Unknown condition method '{self.arg_method_name}'")

    def __set_condition_method(self):
        self.__check_valid_method_name()
        self.condition_method = self.__class__.__dict__[self.arg_method_name]

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
            self.arg_name = arg_name
            self.arg_method_name = self._eq_value.__name__

    def __init__(self, **kwargs):
        self.__set_args(**kwargs)
        self.__set_condition_method()

    def _in_value(self):
        pass

    def _like_value(self):
        pass

    def _between_value(self):
        pass

    def _eq_value(self):
        pass

    def _neq_value(self):
        pass

    def _lt_value(self):
        pass

    def _gt_value(self):
        pass

    def _lte_value(self):
        pass

    def _gte_value(self):
        pass

    def __or__(self, other):
        pass

    def __and__(self, other):
        pass

    def get_sql(self):
        pass
