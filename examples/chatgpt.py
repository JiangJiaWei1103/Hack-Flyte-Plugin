"""
Test ChatGPT agent.

* [ ] Make it work
"""
from flytekitplugins.chatgpt import ChatGPTTask


chatgpt_task = ChatGPTTask(
    name="chatgpt",
    config={
        "openai_organization": "org-NayNG68kGnVXMJ8Ak4PMgQv7",
        "chatgpt_conf": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
        },
    },
)
