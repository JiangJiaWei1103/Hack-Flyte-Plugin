"""
Test ChatGPT agent.

Just use a very simple use case to see how an agent works.

* [ ] Survey a potential bug of `get_agent_secret`
"""
import os

from flytekit import workflow
from flytekitplugins.openai import ChatGPTTask


class CFG:
    run_remote = False


chatgpt_small_job = ChatGPTTask(
    name="demo-3.5-turbo",
    openai_organization=os.environ.get("OPENAI_ORG"),
    chatgpt_config={
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
    },
)


@workflow
def hi_chatgpt(msg: str) -> str:
    res = chatgpt_small_job(message=msg)

    return res


if __name__ == "__main__":
    from flytekit.clis.sdk_in_container import pyflyte
    from click.testing import CliRunner

    runner = CliRunner()
    path = os.path.realpath(__file__)

    # Local run
    result = runner.invoke(pyflyte.main, ["run", path, "hi_chatgpt", "--msg", "hi"])
    print("Local Execution: ", result.output)

    # Remote run
    if CFG.run_remote:
        result = runner.invoke(pyflyte.main, ["run", "--remote", path, "hi_chatgpt", "--msg", "hi"])
        print("Remote Execution: ", result.output)

