import yaml
from doc_translator import Translator


def main():
    with open("settings.yaml", "r", encoding="utf8") as f:
        settings = yaml.safe_load(f)
    translator = Translator.chatgpt(**settings)
    translator.translate("./sample.odt", "answer.odt")


if __name__ == '__main__':
    main()
