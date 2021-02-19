from sqlitedb.fields import IntegerField, TextField, DateField
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
    inst.create()
    inst.select(columns=['id', 'name'], where=Q(id__eq=1))

    # Для исполнения комманд в БД
    # inst.commit()


if __name__ == '__main__':
    main()
