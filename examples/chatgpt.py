"""
Test ChatGPT agent.

---
Executor: SyncAgentExecutorMixin
Parent task: PythonTask
---

## Some tmp notes
* For OpenAI org, see https://platform.openai.com/settings/organization/general
* For model selection, see https://platform.openai.com/docs/models
* For chatgpt_config, see https://platform.openai.com/docs/api-reference/chat/create
* Remember to set env var FLYTE_OPENAI_API_KEY, for generating api key, see
    https://platform.openai.com/settings/organization/general
"""
import os

from flytekit import task, workflow
from flytekitplugins.openai import ChatGPTTask


MODEL = "gpt-3.5-turbo"
TEMP = 0.1


chatgpt_chat = ChatGPTTask(
    name="tiny-chat",
    openai_organization=os.environ["OPENAI_ORG"],
    chatgpt_config={
        "model": MODEL,
        "temperature": TEMP
    }
)


@task
def add_role(model: str, msg: str) -> str:
    return f"{model}: {msg}"
    


@workflow
def chat(message: str) -> str:
    res = chatgpt_chat(message=message)
    res = add_role(model=MODEL, msg=res)

    return res


if __name__ == "__main__":
    print(f"Test ChatGPTTask...\n")

    msg = "Hi there!"
    print(f"User: {msg}")
    print(chat(message=msg))
