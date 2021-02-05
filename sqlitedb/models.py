from datetime import datetime
from collections import namedtuple

from .db import Connection
from .fields import BaseField
from .commands import Builder
from .query import Q


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
        self.instance_class = namedtuple(self.table_name, self.fields.keys(),
                                         defaults=(None,) * len(self.fields.keys()))

    def __init__(self):
        if hasattr(self, 'Meta'):
            self.table_name = self.Meta.table_name
        else:
            self.table_name = type(self).__name__
        self.__set_fields()

        self.__set_instance_class()
        self.builder = Builder(table_name=self.table_name,
                               fields=list(self.fields.keys()))

    def __check_value_types(self, **kwargs):
        for key, value in kwargs.items():
            self.fields[key].check_type_value(value)

    def get_sql_statements(self):
        sql = self.builder.build()
        return sql

    def add(self, **kwargs):
        self.__check_value_types(**kwargs)
        instance = self.instance_class(**kwargs)

        self.builder.add(values=list(instance))

    def update(self, where, limit=None, order_by=None, **kwargs):
        self.__check_value_types(**kwargs)
        instance = self.instance_class(**kwargs)

        self.builder.update(values=list(instance), where=where,
                            order_by=order_by, limit=limit)

    def delete(self, where, limit=None, offset=None):
        self.builder.delete(where=where, limit=limit, offset=offset)

    def commit(self):
        result = []
        for command in self.builder.builded:
            result.append(self.connection.execute(command))

        return result
