import abc


class Formatter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_settings(self, **kwargs):
        raise NotImplemented

    @abc.abstractmethod
    def get_line(self) -> str:
        raise NotImplemented
