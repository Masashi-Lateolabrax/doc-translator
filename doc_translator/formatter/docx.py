from docx import Document
from docx.text.paragraph import Paragraph

from .. import interface as inf


class Chunk:
    def __init__(self, paragraph: Paragraph):
        self._p = paragraph

    def read(self) -> str:
        return self._p.text

    def write(self, txt):
        self._p.text = txt


class DocxFormatter(inf.Formatter):
    def __init__(self, *, src_path, **settings):
        self._doc = Document(src_path)
        self._index = 0

    def set_settings(self, **settings):
        pass

    def get_line(self) -> Chunk:
        res = self._doc.paragraphs[self._index]
        self._index += 1
        return Chunk(res)

    def save(self, dst_path):
        self._doc.save(dst_path)
