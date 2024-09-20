import copy

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

        self.messages = []

        self.set_settings(**settings)

    def set_settings(self, **settings):
        self._prompt = settings.get("prompt", self._prompt)
        self._model = settings.get("model", self._model)

    def translate_line(self, src: str) -> str:
        if all(not c.isspace() for c in src):
            return src

        self.messages.append({"role": "user", "content": src})
        res = self.chat(self.messages, self._prompt)
        self.messages.append({"role": "assistant", "content": res})

        while len(self.messages) > 6:
            self.messages.pop(0)

        return res

    def chat(self, messages, prompt: str | None = ""):
        msg = copy.copy(messages)
        if prompt is not None and len(prompt) > 0:
            msg.insert(-1, {"role": "system", "content": prompt})
        response = self._client.chat.completions.create(
            model=self._model, messages=msg
        )
        return response.choices[0].message.content
