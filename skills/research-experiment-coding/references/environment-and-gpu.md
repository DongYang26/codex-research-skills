# Execution Environment And GPU Management

Use this guide before running Python, launching training, or validating CUDA behavior.

## Repository-Local Instructions First

Check for repository-local instructions before choosing how to execute code:

- `CLAUDE.md`
- `AGENTS.md`
- `AGENT.md`
- `README.md`
- `environment.yml` or `conda.yaml`
- `requirements.txt`
- `pyproject.toml`
- existing project scripts such as `scripts/train.sh`

If `CLAUDE.md`, `AGENTS.md`, or `AGENT.md` exists, read the repository-specific instruction file first and treat it as the local execution contract.

## Environment Selection Order

Use this order:

1. Reuse the repository's existing environment instructions if they already exist.
2. If the repository clearly uses Conda, keep using Conda.
3. If no environment is defined and the work is a research-style Python project, prefer creating a project-specific Conda environment.

When creating a new environment:

- choose a project-specific name
- document the name and activation instructions in the repository instruction file, such as `CLAUDE.md`, `AGENTS.md`, or `AGENT.md`
- prefer running future commands through `conda run -n <env_name> ...` for reproducibility

Do not create multiple ad hoc environments for the same repository.

## Environment Persistence

If you create or adopt a project-specific environment, record:

- environment name
- activation command
- installation command
- any execution-specific variables required by the repo

Keep this in the repository instruction file so future sessions can resume without rediscovery.

## GPU Discovery

Never assume `cuda:0` is safe.

Before launching a GPU-capable command:

- run `nvidia-smi`
- inspect free memory and current utilization
- choose an idle or low-load GPU, usually the one with the most free memory

If `nvidia-smi` is unavailable, do not pretend GPU state is known.

## GPU Execution Convention

Prefer explicit process isolation:

```bash
CUDA_VISIBLE_DEVICES=<gpu_id> python train.py ...
```

If the repository requires project-specific execution variables, set them explicitly. Example:

```bash
CUDA_VISIBLE_DEVICES=<gpu_id> RME_USE_CUDA=1 python train.py ...
```

Do not add project-specific variables like `RME_USE_CUDA=1` to unrelated repositories unless the repo's local instructions require them.

## No Silent CPU Fallback

If the task is supposed to validate or exercise GPU execution:

- do not silently fall back to CPU
- either choose another GPU
- wait for resources
- or report the constraint to the user

CPU fallback is acceptable only when the user explicitly approves it or the task is clearly CPU-only.
