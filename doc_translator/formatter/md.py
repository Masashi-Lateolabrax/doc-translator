import markdown

from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md

from .. import interface as inf


class Chunk(inf.Chunk):
    def __init__(self, element):
        self.element = element

    def read(self) -> str:
        return self.element.get_text()

    def write(self, txt: str):
        self.element.string = txt
        return txt


class MDFormatter(inf.Formatter):
    def __init__(self, *, src_path, **settings):
        with open(src_path, 'r', encoding='utf-8') as f:
            text = f.read()
        html = markdown.markdown(text, extensions=['tables'])

        self.index = 0
        self.soup = BeautifulSoup(html, 'html.parser')
        self.elements = self.soup.contents

        self.exception = settings.get(
            "except",
            ["code", "pre", "blockquote", "table", "img"]
        )

    def set_settings(self, **settings):
        self.exception = settings.get("except", self.exception)

    def __iter__(self):
        self.index = 0
        self.elements = self.soup.contents
        return self

    def __next__(self) -> Chunk:
        while self.index < len(self.elements):
            element = self.elements[self.index]
            self.index += 1
            if element.name in self.exception:
                continue
            elif element.next_element.name in self.exception:
                continue
            if len(element.text.strip()) == 0:
                continue
            return Chunk(element)
        raise StopIteration

    def save(self, dst_path):
        markdown_text = md(str(self.soup), escape_asterisks=False, escape_underscores=False, escape_misc=False)
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
