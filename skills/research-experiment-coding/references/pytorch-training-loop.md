# PyTorch Training Loop Rules

Use this guide when writing `train.py`, `evaluate.py`, `train_one_epoch`, `validate`, or `evaluate`.

## Entrypoint Requirements

- Provide a visible `seed_everything(seed)` implementation in the training entrypoint or make it trivially discoverable from there.
- Centralize hyperparameters in `argparse` or Hydra.
- Give every user-facing argument a clear `help` string.
- Avoid hardcoded paper-facing hyperparameters in the body of the training loop.

## `seed_everything`

The implementation should set at least:

- `random.seed(seed)`
- `numpy.random.seed(seed)`
- `torch.manual_seed(seed)`
- `torch.cuda.manual_seed(seed)`
- `torch.cuda.manual_seed_all(seed)`
- `torch.backends.cudnn.deterministic = True`
- `torch.backends.cudnn.benchmark = False`

## Loop Structure

Training code should usually look like:

1. build config and output directory
2. seed everything
3. build datasets and dataloaders
4. build model, optimizer, scheduler, criterion
5. run `train_one_epoch`
6. run validation with `model.eval()` and `torch.no_grad()`
7. log metrics
8. save best checkpoint

## Metrics Contract

Both training and evaluation helpers should return dictionaries such as:

```python
{"loss": 0.4312, "accuracy": 0.8875}
```

This makes logging, checkpoint selection, and table generation easier.

## Progress And Logging

- Wrap dataloaders with `tqdm`.
- Log loss and core metrics to TensorBoard or W&B.
- If the repo has no established logger, default to TensorBoard.
- Keep stdout readable; progress bars should supplement logs, not replace saved metrics.

## Checkpointing

- Monitor one explicit validation metric such as `accuracy` or negative `loss`.
- Save the best checkpoint when that metric improves.
- Write the checkpoint path and monitored score into logs.
- Keep the selection rule identical across the main method and ablations unless the paper justifies a different one.
