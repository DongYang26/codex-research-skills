---
name: research-experiment-coding
description: Use when implementing ML/AI paper experiment code, especially PyTorch training or evaluation pipelines, baselines, ablations, reproduction scripts, results exporters, or figure-generating utilities in a research repository.
---

# Research Experiment Coding

## Overview

Treat the task as research code, not product code. Default to a classic open-source paper repository style: explicit entrypoints, lightweight `nn.Module` definitions, direct module calls, saved run artifacts, and a training loop a reviewer can audit quickly.

## Quick Start

1. Classify the request as one of:
   - new training pipeline
   - eval-only pipeline
   - baseline or ablation
   - results export or plotting
   - reproduction or cleanup for release
2. Default to PyTorch unless the user or repository clearly uses another framework.
3. Keep the main path explicit:
   - config -> data -> model -> loss -> loop -> metrics -> checkpoint -> reportable outputs
4. Choose the smallest file layout that keeps `train`, `evaluate`, and `reproduce` obvious.
5. Add reproducibility artifacts before abstraction:
   - resolved config
   - seed
   - output directory
   - metrics log
   - checkpoint policy
   - commit hash when practical
6. Leave a direct command or script for the exact experiment.

## Default PyTorch Repository Shape

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
- Use `main.py` only as a thin wrapper if a single unified CLI is truly helpful.
- Keep `models/` limited to lightweight `nn.Module` definitions and small architecture helpers.
- Keep `datasets/` focused on dataset classes, transforms, collators, and dataloader builders.
- Keep `utils/` as small focused modules such as `seed.py`, `metrics.py`, `checkpoint.py`, and `distributed.py`.
- Keep `configs/` as the source of truth for hyperparameters and experiment variants.
- Keep module interaction direct; do not introduce dependency injection, registries, or factory layers for a small paper repo.

Read [references/pytorch-layout.md](references/pytorch-layout.md) when deciding the file tree or package boundaries.

## Entrypoint Rules

When writing `train.py` or other paper-critical entrypoints:

- Provide a complete `seed_everything(seed)` implementation that fixes `random`, `numpy`, `torch`, `torch.cuda`, and `torch.backends.cudnn.deterministic`.
- Set `torch.backends.cudnn.benchmark = False` unless the user explicitly accepts nondeterministic behavior.
- Manage all tunable hyperparameters in one place through `argparse` or Hydra.
- Give every CLI argument a clear `help` string that includes the default behavior.
- Do not hardcode magic numbers for model width, depth, learning rate, batch size, epoch count, or similar paper-facing hyperparameters in the main code path.
- Write the resolved configuration into the run directory before the main loop starts.

Read [references/pytorch-training-loop.md](references/pytorch-training-loop.md) for the expected loop structure and logging behavior.

## Tensor And Formula Comment Rules

When writing `forward`, data processing, attention blocks, losses, or any dense tensor logic:

- Add inline shape comments for each shape-changing or broadcasting-sensitive tensor step.
- In dense mathematical blocks, annotate every semantically meaningful tensor transform until the shape story is obvious.
- If a function implements a paper formula, include a short docstring with LaTeX or plain-text math describing the formula or objective.
- Keep comments brief and mathematical; explain what the tensor means, not what Python syntax does.

Read [references/tensor-comments.md](references/tensor-comments.md) for concrete examples.

## Train And Evaluate Rules

When writing `train`, `train_one_epoch`, `validate`, or `evaluate`:

- Wrap dataloaders with `tqdm`.
- Use `model.train()` for training and `model.eval()` for validation or evaluation.
- Use `with torch.no_grad():` in evaluation code.
- Return metrics as a dictionary, not as ad hoc tuples or print-only side effects.
- Log core metrics such as loss and accuracy to W&B or TensorBoard. If the repo has no established logger, default to TensorBoard.
- Save checkpoints based on the best validation metric and make the monitored metric explicit.
- Keep the training loop readable in one place unless there is real duplication pressure.

## Required Deliverables Per Experiment

Every new paper-facing experiment should leave behind:

- one runnable command
- one stable output directory or naming scheme
- one saved resolved config file
- one recorded seed
- one metrics file such as `jsonl`, `csv`, or `tsv`
- checkpoint files or an explicit reason they are unnecessary
- enough scripting to regenerate tables or figures from saved raw results

Read [references/repro-checklist.md](references/repro-checklist.md) before claiming the work is reproducible.
Use [assets/pytorch-paper-template/](assets/pytorch-paper-template) as the default scaffold for new repos or when the user asks to start from scratch.

## Task Guidance

### New Method

- Add the method with the minimum new surface area.
- Keep shared train and eval logic shared; isolate only the method-specific pieces.
- Prefer config switches and small module additions over parallel codepaths.
- Preserve the same entrypoint and logging conventions as the baseline code.

### Baseline Or Ablation

- Reuse the exact same data loading, evaluation, and logging path as the main method whenever possible.
- Change one factor at a time.
- Make the ablation visible in the run name, saved config, and results filename.
- Do not fork the whole repository layout just to test one variation.

### Eval-Only Work

- Separate checkpoint loading, inference, and metric aggregation cleanly.
- Save per-example outputs when they are needed for error analysis or paper tables.
- Make metric computation auditable from persisted artifacts.
- Keep evaluation callable both from `evaluate.py` and from the training loop for validation.

### Results And Figures

- Persist raw numeric outputs first.
- Generate figures and tables from saved artifacts, not transient in-memory results.
- Keep plotting code separate from model code.

## Anti-Patterns

Do not drift into application-framework code unless the repository truly needs it.

- Do not introduce `Controller`, `Manager`, `Service`, or `Repository` layers for a small experiment repo.
- Do not add registries, plugin systems, or factories before there are multiple real variants to support.
- Do not hide paper-critical hyperparameters in globals or environment variables.
- Do not bury model or dataloader construction behind dependency injection.
- Do not put the only copy of training or evaluation logic in notebooks.
- Do not funnel unrelated helpers into a giant `utils.py`; prefer a small `utils/` package with focused modules.
- Do not save only final PNG or PDF outputs without the raw numbers behind them.
- Do not leave shape-sensitive tensor code uncommented when a reader would have to infer the dimensions mentally.

## Example Requests

- "Implement the training and evaluation code for this new method from the paper draft."
- "Add two ablations and make sure they reuse the same evaluation path."
- "Clean this repo up so reviewers can reproduce Table 1 and Figure 3."
- "Turn this notebook-only experiment into a proper train/eval/results pipeline."
- "Scaffold a PyTorch paper repo with `train.py`, `evaluate.py`, `models/`, `datasets/`, `utils/`, and `configs/`."
