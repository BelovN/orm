# orm
Небольшая ORM для управления простой базой sqlite3. 
#### Создание класса-модели

```python
from sqlitedb.fields import IntegerField, TextField, DateField
from sqlitedb.models import BaseModel
from sqlitedb.utils import Singleton


class PersonDbTemplates(BaseModel, metaclass=Singleton):
    id = IntegerField(name='id', primary_key=True)
    name = TextField(name='name')
    birth_date = DateField(name='birth_date')

    class Meta:
        table_name = "person"
```

Пример описания таблицы в базе данных `person`. 
Обязательно необходимо указать `metaclass=Singleton` для синхронной работы и исключения конфликтов.

### Комманды

Здесь описаны основные команды базы данных [sqlite3](https://sqlite.org/docs.html):
#### 1. Create
```python
PersonDbTemplates().create()
```
#### 2. Add
```python
from datetime import datetime

PersonDbTemplates().add(inst.add(id=2, birth_date=datetime(1999, 11, 12), name="Petr"))
```
#### 3. Update
```python
from sqlitedb.query import Q

PersonDbTemplates().update(name='Sanya', where=Q(id__between=[1, 2]))
```
#### 4. Delete
```python
from sqlitedb.query import Q

PersonDbTemplates().delete(where=Q(id__in_values=[1, 2, 3]) & Q(name__like="Ivan"))
```
#### 5. Select

```python
from sqlitedb.query import Q

PersonDbTemplates().select(columns=['id', 'name'], where=Q(id__eq=1))
```

### Зачем?
Да по фану. Решил добить тестовое задание до чего-то рабочего (Раз уж потратил столько времени).
