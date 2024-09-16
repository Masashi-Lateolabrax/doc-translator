import abc


class Formatter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, **settings):
        raise NotImplemented

    @abc.abstractmethod
    def set_settings(self, **settings):
        raise NotImplemented

    @abc.abstractmethod
    def get_line(self) -> str:
        raise NotImplemented
