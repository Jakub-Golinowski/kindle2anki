from abc import abstractmethod, ABCMeta


class DictBase(metaclass=ABCMeta):
    @abstractmethod
    def look_up(self, word):
        pass
