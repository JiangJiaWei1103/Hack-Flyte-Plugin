# flytekit-slurm Agent
A protoypical example of `flytekit-slurm` agent.

Though this can be unrealistic, we would like to extend from the hello-world difficulty.

## Components
### Core
* `task.py`
    * `SlurmTask`
* `agent.py`
    * `SlurmJobMetadata`
    * `SlurmAgent`
### Utils
* `mock_slurm.py`
    * `SlurmJobState`
    * `SlurmJob`
    * `SlurmCtl`
        * Mimic `slurmctld` with 3 naive methods `sbatch`, `show_job`, and `scancel`
* `tiny_slurm.py`
    * Run a workflow containing a single `SlurmTask` which returns the elapsed time of a slurm job

## Setup
1. Put this codebase under your local `flytekit/plugins/` for dev purpose
2. `cd` into `flytekit-slurm` plugin dir and run `pip install -e .`
3. Put `tiny_slurm.py` right under `flytekit/build/`
4. `cd` into `flytekit/build/` and run `python3 tiny_slurm.py`

## Result
Following illustrates the workflow result, which is the elapsed time of the slurm job. We set the elapsed time to a constant of 0.1 sec.
![Screenshot 2024-12-13 at 12 06 07 AM](https://github.com/user-attachments/assets/b454e3d4-ea82-4921-9779-0320380f28ee)

