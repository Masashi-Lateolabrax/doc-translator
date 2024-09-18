from odfdo import Document, Element

from .. import interface as inf


class Chunk(inf.Chunk):
    def __init__(self, paragraph: Element):
        self._p = paragraph

    def read(self) -> str:
        return self._p.text

    def write(self, txt):
        self._p.text = txt


class OdtFormatter(inf.Formatter):

    def __init__(self, *, src_path, **settings):
        self.doc = Document(src_path)
        self.paragraphs = self.doc.body.paragraphs
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self) -> Chunk | None:
        if self.index >= len(self.paragraphs):
            return None

        res = self.paragraphs[self.index]
        self.index += 1
        return Chunk(res)

    def set_settings(self, **settings):
        pass

    def save(self, dst_path):
        self.doc.save(dst_path)
