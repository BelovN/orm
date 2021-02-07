import re
import operator


class BaseComponent:

    def __init__(self, arg_name, arg_value):
        self.arg_name = arg_name
        self.arg_value = arg_value

    def check_intersection(self, other):
        if self.arg_name == other.arg_name:
            function = self.get_function()
            if function(other.arg_value, self.arg_value):
                return True

            return False


class Eq(BaseComponent):

    def get_function(self):
        return operator.eq


class Ne(BaseComponent):

    def get_function(self):
        return operator.eq

    def check_intersection(self, component):
        if isinstance(component, Ne):
            if self.arg_name == component.arg_name and \
                self.arg_value == component.arg_value:

                return True

            return False


class In_values(BaseComponent):

    def get_function(self):
        return lambda a, b: operator.contains(b, a)

    def check_intersection(self, component):
        if isinstance(component, In_values):
            if self.arg_name == component.arg_name and \
                self.arg_value == component.arg_value:

                return True

            return False


class Like(BaseComponent):

    @staticmethod
    def __like_function_builder(string, like_string):
        like_string = like_string.replace('%', '.*')
        like_string = like_string.replace('_', '.')
        like_string = '^' + like_string + '$'
        matcher = re.compile(like_string)
        return operator.truth(re.findall(matcher, string))

    def get_function(self):
        return Like.__like_function_builder


class Between(BaseComponent):

    @staticmethod
    def __between_function_builder(value, tuple_values):
        return tuple_values[0] <= value <= tuple_values[1]

    def get_function(self):
        return Between.__between_function_builder


class Lt(BaseComponent):

    def get_function(self):
        return operator.lt


class Gt(BaseComponent):

    def get_function(self):
        return operator.gt


class Le(BaseComponent):

    def get_function(self):
        return operator.le


class Ge(BaseComponent):

    def get_function(self):
        return operator.ge
