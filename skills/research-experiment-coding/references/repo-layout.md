# Minimal Research Repository Layout

Use this guide when creating a repo from scratch or reorganizing an experiment codebase.

## Default Layout

```text
project/
  README.md
  train.py
  evaluate.py
  models/
    simple_model.py
  datasets/
    example_dataset.py
  utils/
    checkpoint.py
    metrics.py
    seed.py
  configs/
    default.yaml
  scripts/
    reproduce_main_results.sh
    run_ablation.sh
    make_figures.sh
  results/
  figures/
```

This is enough for many PyTorch papers. Expand only when the repo has real pressure to do so.

## What Each Directory Owns

- `configs/`: declarative experiment settings
- `train.py`: primary training entrypoint
- `evaluate.py`: primary evaluation entrypoint
- `models/`: network definitions
- `datasets/`: datasets, transforms, and dataloader builders
- `utils/`: focused helper modules
- `scripts/`: direct user-facing commands for reproduction and paper outputs
- `results/`: raw run outputs, metrics, checkpoints, predictions
- `figures/`: generated plots and tables derived from `results/`

## When To Add More Structure

Add subpackages only when the repo has multiple concrete families such as:

- multiple datasets with distinct processing pipelines
- multiple model families with little shared logic
- multiple evaluation suites with distinct outputs

Reasonable expansions:

```text
models/backbones/
models/heads/
datasets/transforms/
utils/distributed.py
plotting/
```

Still keep entrypoints obvious.

## Entrypoint Pattern

Keep one direct entrypoint per action. Examples:

- `python train.py --config configs/default.yaml`
- `python evaluate.py --config configs/default.yaml --ckpt results/run_x/best.pt`
- `bash scripts/reproduce_main_results.sh`

Avoid making users discover the right invocation from scattered notebook cells or hidden shell history.

## `main.py` Guidance

`main.py` is optional. If it exists, keep it thin:

- parse the top-level action
- dispatch to `train.py` or `evaluate.py`
- avoid duplicating the actual loop logic there

## Result Layout

A practical layout is:

```text
results/
  method_a_seed0/
    config.yaml
    metrics.jsonl
    best.pt
    predictions.jsonl
  method_a_seed1/
  ablate_dropout_seed0/
```

The exact names can vary, but the layout should make comparisons obvious.

## Tables And Figures

Treat tables and figures as derived artifacts.

- read from `results/`
- write into `figures/`
- keep the generation script versioned
- avoid hand-edited spreadsheet-only pipelines for final paper numbers
