"""
Slurm agent.

Start from a hello-world async agent. 

* [ ] Explore difference btw a job and a task.
"""
from dataclasses import dataclass
from typing import Optional

from flyteidl.core.execution_pb2 import TaskExecution
from flytekit import FlyteContextManager, lazy_module
from flytekit.core.type_engine import TypeEngine
from flytekit.extend.backend.base_agent import AgentRegistry, AsyncAgentBase, Resource, ResourceMeta
from flytekit.extend.backend.utils import convert_to_flyte_phase, get_agent_secret
from flytekit.models.literals import LiteralMap
from flytekit.models.task import TaskTemplate, TaskExecutionMetadata

from .mock_slurm import SlurmCtl


sctl = SlurmCtl()


@dataclass
class SlurmJobMetadata(ResourceMeta):
    """Dummy metadata for the slurm job."""

    sjob_id: str


class SlurmAgent(AsyncAgentBase):
    """Slurm agent."""

    name = "Slurm Agent"

    def __init__(self):
        super(SlurmAgent, self).__init__(task_type_name="slurm", metadata_type=SlurmJobMetadata)
        # task_type_version

    def create(
        self,
        task_template: TaskTemplate,
        # output_prefix: str,
        inputs: Optional[LiteralMap] = None,
        # task_execution_metadata: Optional[TaskExecutionMetadata],
        **kwargs,
    ) -> SlurmJobMetadata:
        """
        Return a resource meta that can be used to get the status of the task.
        """
        # task_template.custom[]
        res = sctl.sbatch(dummy={})

        return SlurmJobMetadata(sjob_id=res.job_id)

    def get(self, resource_meta: SlurmJobMetadata, **kwargs) -> Resource:
        """
        Return the status of the task, and return the outputs in some cases. For example, bigquery job
        can't write the structured dataset to the output location, so it returns the output literals to the propeller,
        and the propeller will write the structured dataset to the blob store.
        """
        sjob_id = resource_meta.sjob_id
        
        res = sctl.show_job(job_id=sjob_id)

        # Determine the task status and convert to flyte phase (a flyteidl entity? not sure now)
        state = res.get("state")
        cur_phase = convert_to_flyte_phase(state)

        # Handle custom info
        elapsed_time = res.get("elapsed_time")
        custom_info = {
            "elapsed_time": elapsed_time,
        }
        outputs = {"o0": elapsed_time}

        return Resource(phase=cur_phase, custom_info=custom_info, outputs=outputs)

    async def delete(self, resource_meta: SlurmJobMetadata, **kwargs):
        """
        Delete the task. This call should be idempotent. It should raise an error if fails to delete the task.
        """
        # Mock a post req to cancel the task
        # Just pop the fromt of the queue and res (wait 3 sec to delete) 
        # await??
        pass


AgentRegistry.register(SlurmAgent())