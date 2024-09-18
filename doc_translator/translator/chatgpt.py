import openai

from ..interface import *


class ChatGPT(Translator):
    def __init__(self, **settings):
        for k in ["organization", "project", "api_key"]:
            if k not in settings:
                raise RuntimeError(f"Need the '{k}' argument.")

        self._client = openai.OpenAI(
            organization=settings["organization"],
            project=settings["project"],
            api_key=settings["api_key"],
        )

        self._prompt = settings.get(
            "prompt",
            "Please translate a sentence into Japanese."
        )
        self._model = settings.get("model", "gpt-4o-mini")

        self.set_settings(**settings)

    def set_settings(self, **settings):
        self._prompt = settings.get("prompt", self._prompt)
        self._model = settings.get("model", self._model)

    def translate_line(self, src: str) -> str:
        if all(not c.isspace() for c in src):
            return src

        messages = [
            {"role": "system", "content": self._prompt},
            {"role": "user", "content": src}
        ]
        response = self._client.chat.completions.create(
            model=self._model, messages=messages
        )
        return response.choices[0].message.content
