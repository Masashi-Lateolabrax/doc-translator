import lxml.etree as ET

from odfdo import Document, Element

from .. import interface as inf


class Chunk(inf.Chunk):
    def __init__(self, e: Element):
        self._e = e

    def read(self) -> str:
        return self._e.serialize(with_ns=True)

    def write(self, txt):
        try:
            ET.fromstring(txt)
        except ET.ParseError as e:
            raise RuntimeError(f"{e}\n\n{txt}")

        new = self._e.from_tag(txt)
        self._e.parent.replace_element(self._e, new)


class OdtFormatter(inf.Formatter):
    def __init__(self, *, src_path, **settings):
        self.doc = Document(src_path)
        self.paragraphs = self.doc.body.paragraphs
        self.idx = 0

    def __iter__(self):
        self.paragraphs = self.doc.body.paragraphs
        self.idx = 0
        return self

    def __next__(self) -> Chunk | None:
        if self.idx >= len(self.paragraphs):
            raise StopIteration

        res = self.paragraphs[self.idx]
        self.idx += 1
        while len(res.text_recursive) == 0:
            res = self.paragraphs[self.idx]
            self.idx += 1
            if self.idx >= len(self.paragraphs):
                raise StopIteration

        return Chunk(res)

    def set_settings(self, **settings):
        pass

    def save(self, dst_path):
        self.doc.save(dst_path)
