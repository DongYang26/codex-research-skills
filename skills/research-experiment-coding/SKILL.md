---
name: research-experiment-coding
description: Use when implementing, debugging, running, or reproducing ML/AI paper experiments in a research repository, especially PyTorch training or evaluation pipelines, baselines, ablations, dataset pipelines, environment or GPU setup, tensor-shape debugging, results export, or experiment cleanup.
---

# Research Experiment Coding

## Overview

Treat the task as research code, not product code. Default to a classic open-source paper repository style: explicit entrypoints, lightweight `nn.Module` definitions, direct module calls, saved run artifacts, and training or evaluation paths a reviewer can audit quickly.

Keep the main skill lean. Read only the referenced file that matches the current task.

## Fast Path

1. Classify the task as one of: training pipeline, eval-only work, baseline or ablation, results export, reproduction, or cleanup.
2. Default to PyTorch unless the user or repository clearly uses another framework.
3. Keep the main path explicit:
   - config -> data -> model -> loss -> loop -> metrics -> checkpoint -> reportable artifacts
4. Leave one direct command or script for the exact experiment.
5. Before running code, inspect repository-local instructions and decide whether the task needs environment setup, GPU selection, data profiling, or debug-only scratch artifacts.

## Core Repository Defaults

For a new PyTorch paper repo, prefer:

```text
train.py
evaluate.py
models/
datasets/
utils/
configs/
results/
figures/
```

- Use `train.py` and `evaluate.py` as the direct entrypoints.
- Use `main.py` only as a thin wrapper when a unified CLI is clearly helpful.
- Keep `models/`, `datasets/`, and `utils/` small and direct.
- Keep module interaction direct; do not introduce dependency injection, registries, or factory layers for a small paper repo.

Read [references/pytorch-layout.md](references/pytorch-layout.md) for the default file tree and [references/style-guide.md](references/style-guide.md) for overall paper-repo coding taste.

## Entrypoints And Config

When writing `train.py` or other paper-critical entrypoints:

- Provide a complete `seed_everything(seed)` that fixes `random`, `numpy`, `torch`, `torch.cuda`, and `torch.backends.cudnn.deterministic`.
- Set `torch.backends.cudnn.benchmark = False` unless the user explicitly accepts nondeterministic behavior.
- Manage tunable hyperparameters through `argparse` or Hydra.
- Give every CLI argument a clear `help` string that includes default behavior.
- Do not hardcode paper-facing magic numbers for width, depth, learning rate, batch size, or epoch count in the main code path.
- Write the resolved configuration into the run directory before the main loop starts.

Read [references/pytorch-training-loop.md](references/pytorch-training-loop.md) for loop structure and logger expectations.

## Execution Discipline

Before running Python, tests, smoke checks, or training jobs:

- Check repository-local instructions such as `CLAUDE.md`, `AGENTS.md`, `AGENT.md`, `README.md`, `environment.yml`, `requirements.txt`, or `pyproject.toml`.
- Reuse the repository's existing environment strategy when it exists; otherwise create and document a project-specific environment only when the task clearly needs one.
- Inspect available GPUs before launching GPU work. Do not blindly assume `cuda:0`.
- Prefer explicit GPU selection through environment variables such as `CUDA_VISIBLE_DEVICES`.
- Do not silently fall back to CPU when the task is supposed to validate GPU execution.
- Inspect real data before writing a non-trivial `Dataset` or preprocessing pipeline.
- Keep one-off diagnostics and smoke-test artifacts in a dedicated scratch location.

Read [references/environment-and-gpu.md](references/environment-and-gpu.md), [references/data-profiling.md](references/data-profiling.md), and [references/artifact-hygiene.md](references/artifact-hygiene.md) when the task touches execution, data, or temporary artifacts.

## Tensor Discipline

When writing `forward`, data processing, losses, attention blocks, or other dense tensor logic:

- Add inline shape comments for shape-changing or broadcasting-sensitive steps.
- Add a short formula docstring when a function implements a paper formula or objective.
- Keep comments mathematical and brief.

When a runtime failure involves shape, dtype, broadcasting, or device placement:

- Do not guess with random `squeeze`, `unsqueeze`, `reshape`, `transpose`, or similar edits.
- Log the exact `.shape`, `.dtype`, and `.device` of the tensors involved.
- Compare the logged tensors against the intended math, state the mismatch explicitly, then make the smallest correction.

Read [references/tensor-comments.md](references/tensor-comments.md) and [references/tensor-debugging.md](references/tensor-debugging.md) before editing shape-sensitive code.

## Training And Evaluation Loop

When writing `train`, `validate`, or `evaluate`:

- Wrap dataloaders with `tqdm`.
- Use `model.train()` for training and `model.eval()` for validation or evaluation.
- Use `with torch.no_grad():` in evaluation code.
- Return metrics as a dictionary, not ad hoc tuples or print-only side effects.
- Log core metrics such as loss and accuracy to W&B or TensorBoard. If the repo has no established logger, default to TensorBoard.
- Save checkpoints based on an explicit best validation metric.
- Keep the main training loop readable in one place unless there is real duplication pressure.

Read [references/pytorch-training-loop.md](references/pytorch-training-loop.md) for the full loop pattern.

## Navigation And Safety

When entering a large repository or making risky changes:

- Start with directory structure, not full-file reads.
- Use targeted search to find the exact class, function, config, or script you need.
- Read only the relevant regions unless a wider pass is clearly necessary.
- Prefer small, intentional git checkpoints when a concrete sub-task is known to work.
- Stage explicit file paths instead of blindly staging the full worktree.
- Preserve a reversible state before high-risk refactors or speculative fixes.
- Never use destructive reset behavior as an automatic fallback.

Read [references/context-navigation.md](references/context-navigation.md) and [references/safe-checkpointing.md](references/safe-checkpointing.md) when navigating or debugging an existing repo.

## Required Deliverables

Every paper-facing experiment should leave behind:

- one runnable command
- one stable output directory or naming scheme
- one saved resolved config
- one recorded seed
- one metrics file such as `jsonl`, `csv`, or `tsv`
- checkpoint files or an explicit reason they are unnecessary
- enough saved raw results and scripting to regenerate tables or figures

Read [references/repro-checklist.md](references/repro-checklist.md) before claiming the work is reproducible. Use [assets/pytorch-paper-template/](assets/pytorch-paper-template) when starting from scratch.

## Task Patterns

- New method: add the method with the minimum new surface area, keep shared train and eval logic shared, and prefer config switches over parallel codepaths.
- Baseline or ablation: reuse the same data, evaluation, and logging path whenever possible; change one factor at a time.
- Eval-only work: separate checkpoint loading, inference, and metric aggregation cleanly, and persist per-example outputs when they matter.
- Results and figures: persist raw numeric outputs first and keep plotting code separate from model code.

## Anti-Patterns

- Do not drift into `Controller`, `Manager`, `Service`, or `Repository` layers for a small experiment repo.
- Do not add registries, plugin systems, or factories before there are multiple real variants to support.
- Do not hide paper-critical hyperparameters in globals or unrelated environment variables.
- Do not put the only copy of training or evaluation logic in notebooks.
- Do not funnel unrelated helpers into a giant `utils.py`; prefer a small `utils/` package with focused modules.
- Do not save only final PNG or PDF outputs without the raw numbers behind them.
