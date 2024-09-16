from . import interface as inf


class Translator:
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Use the static methods. to instantiate this class.")

    def __init__(self, translator: inf.Translator, **settings):
        self._translator = translator

    @staticmethod
    def chatgpt(**settings):
        from .translator import ChatGPT

        translator = ChatGPT(**settings)

        this = object.__new__(Translator)
        this.__init__(translator, **settings)

    def translate(self, src_path, dst_path):
        raise NotImplemented
