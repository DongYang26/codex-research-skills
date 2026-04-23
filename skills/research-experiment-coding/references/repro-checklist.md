# Reproducibility Checklist

Use this checklist before calling an experiment pipeline paper-ready.

## Run Identity

- Record the resolved config.
- Record the random seed.
- Record the code version or git commit when practical.
- Record the dataset split or preprocessing variant.
- Record the validation metric used for best-checkpoint selection.

## Execution Artifacts

- Save scalar metrics in a parseable format.
- Save checkpoints or state clearly why they are omitted.
- Save predictions or intermediate outputs when needed for later analysis.
- Make sure output directories are uniquely named and stable.
- Persist logger outputs from TensorBoard or W&B consistently with the run directory.

## Command Surface

- Provide one direct command for each main result.
- Prefer versioned scripts for main paper numbers.
- Avoid hidden manual steps between training and figure generation.

## Comparability

- Log the same metrics for the method, baseline, and ablations.
- Keep evaluation code shared where possible.
- Make it obvious what changed between runs.

## Release Readiness

- Confirm the README points to the real commands.
- Confirm figures or tables can be rebuilt from saved outputs.
- Confirm notebook work has a script equivalent if it affects the paper.
- Confirm raw results exist behind any published plot.

## Failure Signals

Treat these as reproducibility failures:

- a result directory without its config
- a figure that cannot be regenerated from committed code and saved outputs
- a paper table assembled by hand from terminal logs
- an ablation whose only difference is not encoded in config or run metadata
- a "best" checkpoint whose monitored metric is not documented
