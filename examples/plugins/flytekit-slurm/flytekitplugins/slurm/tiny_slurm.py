"""
Test slurm agent.

Just use a very simple use case to see how an agent works.
"""
import os

from flytekit import workflow
from flytekitplugins.slurm import SlurmTask


class CFG:
    run_remote = False


slurm_tiny_job = SlurmTask(
    name="demo-naive-slurm",
    slurm_config={},
)


@workflow
def hi_slurm(dummy: str) -> float:
    """Return the elapsed time of a naive slurm job."""
    res = slurm_tiny_job(dummy=dummy)

    return res


if __name__ == "__main__":
    from flytekit.clis.sdk_in_container import pyflyte
    from click.testing import CliRunner

    runner = CliRunner()
    path = os.path.realpath(__file__)

    # Local run
    result = runner.invoke(pyflyte.main, ["run", path, "hi_slurm", "--dummy", "hi"])
    print("Local Execution: ", result.output)

    # Remote run
    if CFG.run_remote:
        result = runner.invoke(pyflyte.main, ["run", "--remote", path, "hi_slurm"])
        print("Remote Execution: ", result.output)

