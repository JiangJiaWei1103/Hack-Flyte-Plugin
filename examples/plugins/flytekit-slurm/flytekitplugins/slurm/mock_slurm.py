"""
Mock slurm with extremely simple logic.

This can be unrealistic.

* [ ] Accurately define terms (e.g., task, job, slurm job)
"""
from collections import deque
from enum import Enum
from time import sleep, process_time
from typing import Any, Dict


# Define a global job queue
SLURMQ = deque()

# Define static time
JOB_SUB_TIME = 1
JOB_EXEC_TIME = 0.1


class SlurmJobState(Enum):
    """Slurm job state."""
    RUNNING = "running"
    DONE = "done"


class SlurmJob:
    """Slurm job."""

    # elapsed_time: float = 0.0

    def __init__(self, job_id: str) -> None:
        self.job_id = job_id

        # Init job status
        self.state = SlurmJobState.RUNNING.value
        self.start_time = process_time()


class SlurmCtl:
    """Slurm controller."""

    def __init__(self) -> None: 
        self._n_jobs = 0
        self._job_map = {}

    def sbatch(self, **kwargs) -> SlurmJob:
        """Submit a batch script to Slurm.

        Mimic a post request to submit a job.
        """
        # Mimic delay of job submission 
        sleep(JOB_SUB_TIME)

        # Create a job
        job = SlurmJob(
            job_id=self._n_jobs,
        )
        self._job_map[self._n_jobs] = job

        self._n_jobs += 1

        return self._get_job(self._n_jobs - 1) 

    def show_job(self, job_id: str) -> Dict[str, Any]:
        """Show detailed information about the slurm job.
        
        Mimic a get request to get the job info.
        """
        job = self._get_job(job_id)

        # Calculate elapsed time and update the job state 
        elapsed_time = process_time() - job.start_time
        if elapsed_time > JOB_EXEC_TIME:
            job.state = SlurmJobState.DONE.value

        # Generate response
        res = {
            "elapsed_time": elapsed_time,
            "state": job.state
        }

        return res

    @staticmethod
    def scancel(job_id: str) -> None:
        """Kill a slurm job."""
        pass
         

    def _get_job(self, job_id: int) -> SlurmJob:
        return self._job_map[job_id]
