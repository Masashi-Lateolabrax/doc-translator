import os

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
        _, ext = os.path.splitext(src_path)

        if ".docx" == ext:
            from .formatter import DocxFormatter
            fm = DocxFormatter(src_path=src_path)
        else:
            raise RuntimeError("Not support")

        while True:
            chunk = fm.get_chunk()
            if chunk is None:
                break

            translated = self._translator.translate_line(chunk.read())
            chunk.write(translated)

        fm.save(dst_path)
