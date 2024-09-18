import abc


class Chunk(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def write(self, txt):
        raise NotImplemented


class Formatter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, **settings):
        raise NotImplemented

    @abc.abstractmethod
    def set_settings(self, **settings):
        raise NotImplemented

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplemented

    @abc.abstractmethod
    def __next__(self) -> Chunk | None:
        raise NotImplemented
