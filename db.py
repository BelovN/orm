from abc import ABC


class AbstractDB(ABC):
    def add(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass


class AbstractCommand(ABC):
    pass


class Postgre(AbstractDB):
    pass


class MySQL(AbstractDB):
    pass



class BaseModel:
    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
