from datetime import datetime

from sqlitedb.fields import (BaseField, IntegerField, RealField,
                             TextField, DateField)
from sqlitedb.models import BaseModel
from sqlitedb.query import Q
from sqlitedb.utils import Singleton


class PersonDbTemplates(BaseModel, metaclass=Singleton):
    id = IntegerField(name='id', primary_key=True)
    name = TextField(name='name')
    birth_date = DateField(name='birth_date')

    class Meta:
        table_name = "person"


def main():
    inst = PersonDbTemplates()
    inst.delete(where=Q(id__in_values=[1, 2, 3]) & Q(name__like="Ivan"))
    inst.add(id=1, birth_date=datetime(1999, 11, 12), name="San123ya")
    inst.add(id=1, birth_date=datetime(1999, 11, 12), name="Petr")

    inst.update(name='Sanya', where=Q(id__between=[1, 2]))

    sql = inst.get_sql_statements()
    print(sql)

    # Для исполнения комманд в БД
    # inst.commit()


if __name__ == '__main__':
    main()
