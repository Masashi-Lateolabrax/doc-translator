import os
from time import sleep

from . import interface as inf
from .translator import ChatGPT


class Translator:
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Use the static methods. to instantiate this class.")

    def __init__(self, translator: inf.Translator, **settings):
        self._translator = translator

    @staticmethod
    def chatgpt(**settings):
        from .translator import ChatGPT

        translator = ChatGPT(**settings)

        this: Translator = object.__new__(Translator)
        this.__init__(translator, **settings)

        return this

    def translate(self, src_path, dst_path):
        _, ext = os.path.splitext(src_path)

        if ".docx" == ext:
            from .formatter import DocxFormatter
            fm = DocxFormatter(src_path=src_path)
        elif ".odt" == ext:
            from .formatter import OdtFormatter
            fm = OdtFormatter(src_path=src_path)
        else:
            raise RuntimeError("Not support")

        for chunk in fm:
            text = chunk.read()
            # translated = self._translator.translate_line(text)
            print(text)
            sleep(0.5)

            for i in range(5):
                # try:
                #     if i == 0:
                #         content = chunk.write(translated)
                #     else:
                #         content = chunk.write(translated, recover=True)
                #     print(content)
                # except RuntimeError as e:
                #     print(f"Error: {e}. [{translated}]")
                #     if isinstance(self._translator, ChatGPT):
                #         msg = f"Your answer, which is shown below, is invalid xml. [Error: {e}]\n\n{translated}\n\nPlease retry the translation. The source XML is as follows:\n\n{text}"
                #         translated = self._translator.translate_line(msg)
                #     continue

                break

        fm.save(dst_path)
