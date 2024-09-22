import os.path

import yaml
from doc_translator import Translator


def main():
    cd = os.path.dirname(__file__)

    with open(os.path.join(cd, "settings.yaml"), "r", encoding="utf8") as f:
        settings = yaml.safe_load(f)
    translator = Translator.chatgpt(**settings)
    translator.translate(
        os.path.join(cd, "sample.md"),
        os.path.join(cd, "answer.md"),
    )


if __name__ == '__main__':
    main()
