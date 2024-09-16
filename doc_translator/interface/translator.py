import abc


class Translator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_settings(self, **kwargs):
        raise NotImplemented

    @abc.abstractmethod
    def translate_line(self, src: str) -> str:
        raise NotImplemented
