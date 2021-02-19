from collections import namedtuple

from .commands import Builder
from .db import Connection
from .fields import BaseField


class BaseModel:
    fields = None
    builder = None
    instance_class = None
    table_name = None

    def __set_fields(self):
        self.fields = {}
        self.connection = Connection()
        for attr_name in self.__class__.__dict__.keys():
            attr = self.__class__.__dict__[attr_name]

            if isinstance(attr, BaseField):
                self.fields[attr_name] = attr

    def __set_instance_class(self):
        self.instance_class = namedtuple(
            self.table_name, self.fields.keys(), defaults=(None,) * len(self.fields.keys())
        )

    def __init__(self):
        if hasattr(self, 'Meta'):
            self.table_name = self.Meta.table_name
        else:
            self.table_name = type(self).__name__
        self.__set_fields()

        self.__set_instance_class()
        self.builder = Builder(table_name=self.table_name, fields=self.fields)

    def get_sql_statements(self):
        sql = self.builder.build()
        return sql

    def add(self, **kwargs):
        ArgsValidator.validate(self.fields, **kwargs)
        ArgsTypesValidator.validate(self.fields, **kwargs)

        instance = self.instance_class(**kwargs)

        self.builder.add(values=list(instance))

    def update(self, where, limit=None, order_by=None, **kwargs):
        ArgsValidator.validate(self.fields, **kwargs)
        ArgsTypesValidator.validate(self.fields, **kwargs)

        query_args = where.get_args()
        QueryValidator.validate(self.fields, query_args)

        instance = self.instance_class(**kwargs)

        self.builder.update(values=list(instance), where=where,
                            order_by=order_by, limit=limit)

    def delete(self, where, limit=None, offset=None):
        query_args = where.get_args()
        QueryValidator.validate(self.fields, query_args)

        self.builder.delete(where=where, limit=limit, offset=offset)

    def create(self, if_not_exists=True, without_rowid=False):
        self.builder.create(if_not_exists=if_not_exists, without_rowid=without_rowid)

    def select(self, columns, where, order_by, distinct=False):
        query_args = where.get_args()
        QueryValidator.validate(self.fields, query_args)

        command = self.builder.select(
            distinct, columns, self.table_name, where, order_by
        )
        return self.connection.execute(command)

    def commit(self):
        result = []
        for command in self.builder.builded:
            result.append(self.connection.execute(command))

        return result


class ArgsTypesValidator:

    @staticmethod
    def validate(fields, **kwargs):
        for key, value in kwargs.items():
            fields[key].check_type_value(value)


class ArgsValidator:

    @staticmethod
    def validate(fields, **kwargs):
        if not set(fields.keys()).issuperset(set(kwargs.keys())):
            raise AttributeError(f'Unknown attributes {list(set(kwargs.keys())-set(fields.keys()))}')


class QueryValidator:
    methods_with_iterable_args = ['between', 'in_values']

    @staticmethod
    def __check_same_types(iterable):
        value_type = type(iterable[0])

        for val in iterable:
            if not isinstance(val, value_type):
                raise ValueError(f'Different type values in {iterable}')

    @staticmethod
    def validate(fields, query_args):
        kwargs = {}
        for query in query_args:
            if query['method'] in QueryValidator.methods_with_iterable_args:
                QueryValidator.__check_same_types(query['method'])
                if query['arg_name'] not in kwargs:
                    kwargs[query['arg_name']] = query['arg_value'][0]
            else:
                if query['arg_name'] not in kwargs:
                    kwargs[query['arg_name']] = query['arg_value']

        ArgsTypesValidator.validate(fields, **kwargs)
        ArgsValidator.validate(fields, **kwargs)
