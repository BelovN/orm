from abc import ABC
from enum import Enum
from typing import Any


class AbstractDB(ABC):
    def execute(self, command, *args, **kwargs):
        pass


class DataBase(AbstractDB):
    def execute(self, command, *args, **kwargs):
        pass


class SQLite3(DataBase):
    cursor: Any

    def execute(self, command, *args, **kwargs):
        pass
