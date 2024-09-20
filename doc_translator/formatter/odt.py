import lxml.etree as ET

from odfdo import Document, Element

from .. import interface as inf


class Chunk(inf.Chunk):
    def __init__(self, e: Element):
        self._e = e

    def read(self) -> str:
        return self._e.serialize(with_ns=True)

    def write(self, txt, recover=False):
        try:
            if recover:
                parser = ET.XMLParser(recover=True)
                recovered = ET.fromstring(txt, parser)
                txt = ET.tostring(recovered, encoding='unicode')
            else:
                recovered = ET.fromstring(txt)
                txt = ET.tostring(recovered, encoding='unicode')
            ET.fromstring(txt)
        except ET.ParseError as e:
            raise RuntimeError(f"{e}\n\n{txt}")
        except TypeError as e:
            raise RuntimeError(f"{e}\n\n{txt}")

        new = self._e.from_tag(txt)
        self._e.parent.replace_element(self._e, new)
        return txt


class OdtFormatter(inf.Formatter):
    def __init__(self, *, src_path, **settings):
        self.doc = Document(src_path)
        self.parent = self.doc.body
        self.ch_idx = [0]

    def __iter__(self):
        self.parent = self.doc.body
        self.idx = [0]
        return self

    def _next(self):
        while True:
            if self.ch_idx[-1] < len(self.parent.children):
                res: Element = self.parent.children[self.ch_idx[-1]]
                self.ch_idx[-1] += 1

                if len(res.children) > 0:
                    if res.get_draw_group() is None:
                        return res
                    elif len(res.text_recursive) > 0:
                        return res

                    self.parent = res
                    self.ch_idx.append(0)

                return res

            elif len(self.ch_idx) > 1:
                self.ch_idx.pop(-1)
                self.parent = self.parent.parent
                continue

            raise StopIteration

    def __next__(self) -> Chunk | None:

        res: Element | None = None
        while True:
            if self.idx[-1] >= len(self.parent.children):
                raise StopIteration

            elif isinstance(res, Element):
                if len(res.text_recursive) > 0:
                    break
                elif:
                    pass

            res = self.paragraphs[self.idx]
            self.idx += 1

        return Chunk(res)

    def set_settings(self, **settings):
        pass

    def save(self, dst_path):
        self.doc.save(dst_path)
