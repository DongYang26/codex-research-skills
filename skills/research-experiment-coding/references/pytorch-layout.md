# PyTorch Paper Layout

Use this layout when the repository is a paper-facing PyTorch project and no stronger house style already exists.

## Preferred Tree

```text
project/
  train.py
  evaluate.py
  models/
  datasets/
  utils/
  configs/
  results/
  figures/
```

## Directory Contracts

- `train.py`: the main training entrypoint and the clearest place to read the training loop
- `evaluate.py`: standalone evaluation, test-time inference, and checkpoint loading
- `models/`: lightweight `nn.Module` definitions and close-by architecture helpers
- `datasets/`: dataset classes, transforms, collators, and dataloader construction
- `utils/`: small helper modules such as `seed.py`, `metrics.py`, `checkpoint.py`, and `distributed.py`
- `configs/`: YAML or Hydra configs for methods, baselines, and ablations

## Keep Calls Direct

Prefer:

- `train.py` imports `build_dataloaders` from `datasets/...`
- `train.py` imports `ModelName` from `models/...`
- `train.py` imports `save_checkpoint` or metric helpers from `utils/...`

Avoid:

- dependency injection containers
- model registries for a single method family
- factory layers that hide which class is being instantiated

## `main.py`

`main.py` is optional. Use it only when you need a unified command surface. If you keep it:

- parse action names such as `train` or `eval`
- dispatch into real entrypoints
- do not move the actual train loop out of `train.py`

## `utils/` Rule

Use a package, not a dumping ground.

Good:

- `utils/checkpoint.py`
- `utils/metrics.py`
- `utils/seed.py`

Bad:

- one giant `utils.py` with unrelated logic
