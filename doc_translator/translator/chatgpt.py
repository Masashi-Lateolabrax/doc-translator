import warnings
import time

import openai

from .. import interface as inf

if "_client" not in globals():
    _client = None


class ChatGPT(inf.Translator):
    def __init__(self, **settings):
        global _client

        for k in ["organization", "project", "api_key"]:
            if k not in settings:
                raise RuntimeError(f"Need the '{k}' argument.")

        if _client is None:
            _client = openai.OpenAI(
                organization=settings["organization"],
                project=settings["project"],
                api_key=settings["api_key"],
            )
        self._client = _client

        self._instructions = settings.get("prompt", "Please translate a sentence into Japanese.")
        self._model = settings.get("model", "gpt-4o-mini")

        self.assistant = self._client.beta.assistants.create(
            model=self._model,
        )

        self._messages = []

        self.set_settings(**settings)

    def __del__(self):
        response = self._client.beta.assistants.delete(self.assistant.id)

    def set_settings(self, **settings):
        self._instructions = settings.get("prompt", self._instructions)
        self._model = settings.get("model", self._model)

        self._client.beta.assistants.update(
            self.assistant.id,
            model=self._model,
        )

    def translate_line(self, src: str) -> str:
        if all(not c.isspace() for c in src):
            return src

        self._messages.append({"role": "user", "content": src})

        res = self.chat(self._messages, self._instructions)

        self._messages.append({"role": "assistant", "content": res})

        while len(self._messages) > 6:
            self._messages.pop(0)

        return res

    def chat(self, msg, prompt: str):
        run = self._client.beta.threads.create_and_run(
            assistant_id=self.assistant.id,
            instructions=prompt,
            thread={"messages": msg},
            temperature=0.2
        )

        timeout = 3
        start_time = time.time()
        while True:
            run = self._client.beta.threads.runs.retrieve(thread_id=run.thread_id, run_id=run.id)

            if run.status == "completed":
                break
            elif run.status == "cancelled":
                warnings.warn(f"Cancelled RUN{run.id}.")
                break
            elif run.status == "failed" or run.status == "incomplete" or run.status == "expired":
                warnings.warn(f"Failed to run. [RUN:{run.id}, STATUS:{run.status}].")
                break
            elif time.time() - start_time > timeout * 60:
                warnings.warn(f"Timeout: {timeout} minutes have passed, force stopping the process.")
                break

        msgs = self._client.beta.threads.messages.list(thread_id=run.thread_id, run_id=run.id)
        msg = msgs.data[-1].content[0].text.value

        return msg
