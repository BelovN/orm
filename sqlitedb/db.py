import sqlite3

from abc import ABC
from enum import Enum
from typing import Any

from .settings import DB_NAME
from .utils import Singleton


class Connection(metaclass=Singleton):

    def __init__(self):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()

    def execute(self, command):
        self.cursor.execute(command)
        self.connection.commit()
        result = self.cursor.fetchall()
        return result

    def __del__(self):
        self.connection.close()
