# Research Code Style Guide

Use this guide when deciding how the code should feel to a reader opening an academic repository for the first time.

## Goal

A strong paper repo should feel easy to audit:

- a reader can find the training loop quickly
- a reviewer can map paper claims to saved outputs
- a reproducer can rerun the experiment without reverse-engineering the codebase

Optimize for those properties before optimizing for extensibility.

## Preferred Style

- Prefer short, direct modules over deep package trees.
- Prefer explicit data flow over magic registration.
- Prefer one obvious entrypoint per task.
- Prefer readable scripts over clever indirection.
- Prefer stable output artifacts over terminal-only logging.
- Prefer the classic PyTorch paper layout over framework-heavy application structure.

## Naming

- Name files after the research task: `train.py`, `evaluate.py`, `metrics.py`, `plot_results.py`.
- Name configs after the experiment family or dataset: `cifar10_baseline.yaml`, `ablate_loss.yaml`.
- Name run directories so a human can infer what changed.
- Avoid generic names such as `manager.py`, `engine.py`, or `processor.py` unless they are truly specific and established in the repo.

## Module Boundaries

Good boundaries in research repos are usually:

- `train.py`: optimization loop, validation calls, checkpoint policy
- `evaluate.py`: checkpoint loading, inference, and metric aggregation
- `models/`: architecture definitions
- `datasets/`: dataset classes, transforms, dataloader builders
- `utils/`: focused helpers such as seed, metrics, checkpoint, and distributed utilities
- `configs/`: experiment settings
- `plot`: figure generation from saved results

Bad boundaries are usually abstract layers imported from application engineering:

- services
- controllers
- repositories
- event buses
- dependency injection containers

## Abstraction Rule

Add an abstraction only when one of these is true:

- the same logic already exists in two call sites
- the same concept must support multiple experiment families
- the abstraction makes the paper-critical path easier to read

Do not abstract preemptively.

## Logging And Outputs

- Save the resolved config for every run.
- Save scalar metrics in `jsonl`, `csv`, or `tsv`.
- Save checkpoints with enough metadata to identify dataset, seed, and step or epoch.
- Save artifacts in a stable layout that plotting code can read later.
- Make the best-validation checkpoint criterion explicit in code and logs.
- Log core training curves to TensorBoard or W&B rather than to stdout alone.

## Comments

Comment:

- unusual math
- evaluation protocol details
- dataset quirks
- paper-specific implementation decisions
- tensor shapes when they change or would be unclear to a reader

Do not comment obvious Python.

## Review Test

Before accepting the code style, ask:

- Can a new reader find the main loop in under two minutes?
- Can someone regenerate a figure from saved outputs without rerunning training?
- Can someone tell which config produced a result directory?
- Can someone identify what changed between the main method and an ablation?

If any answer is no, simplify the code or make the artifact trail more explicit.
