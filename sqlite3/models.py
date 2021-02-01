from collections import namedtuple
from commands import Builder
from fields import BaseField, IntegerField, RealField, TextField


class BaseModel:
    # TODO: Singleton
    fields = None
    builder = None
    instance_class = None
    table_name = None

    def __set_fields(self):
        self.fields = {}
        for attr_name in self.__class__.__dict__.keys():
            attr = self.__class__.__dict__[attr_name]

            if isinstance(attr, BaseField):
                self.fields[attr_name] = attr

    def __set_instance_class(self):
        self.instance_class = namedtuple(self.table_name, self.fields.keys(), defaults=(None,) * len(self.fields.keys()))

    def __init__(self):
        self.table_name = type(self).__name__
        self.__set_fields()

        self.__set_instance_class()
        self.builder = Builder(table_name=self.table_name, fields=list(self.fields.keys()))

    def execute(self):
        sql = self.builder.build()
        print(sql)

    def add(self, **kwargs):
        instance = self.instance_class(**kwargs)

        self.builder.add(values=tuple(instance))

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Person(BaseModel):
    id = IntegerField(name='id', not_null=True)
    first_name = TextField(name='first_name', not_null=True)
    age = TextField(name='age', not_null=True)


person = Person()
person.add(id="id", first_name="first_name", age="age")
# person.add(id="id2", age="age2")
person.add(age=2, first_name="first_name3", id="id2")
# person.add(id="id2", first_name="first_name3", age="age2")
person.execute()
