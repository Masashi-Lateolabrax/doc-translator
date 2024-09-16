import abc


class Translator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, **settings):
        raise NotImplemented

    @abc.abstractmethod
    def set_settings(self, **settings):
        raise NotImplemented

    @abc.abstractmethod
    def translate_line(self, src: str) -> str:
        raise NotImplemented
