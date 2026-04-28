# Defensive Data Profiling

Use this guide before writing a non-trivial dataset class or preprocessing pipeline.

## Inspect First

Do not build the final dataset pipeline from assumptions alone.

Write a minimal inspection script such as `inspect_data.py` when the dataset format is non-trivial or unfamiliar.

## Required Checks

For tabular or structured records:

- inspect the first few samples
- check for missing values or `NaN`
- verify numeric versus string types
- inspect label ranges and class IDs

For images:

- inspect at least 3 real samples
- log resolution
- log channel count
- confirm color space assumptions when relevant

For audio:

- inspect at least 3 real samples
- log duration
- log sample rate
- log channel count

For sequence or token data:

- inspect representative lengths
- verify padding or truncation assumptions
- check for malformed or empty records

## Minimal Output Goal

The inspection step should leave you able to answer:

- what one sample looks like
- what the true schema is
- what edge cases exist
- whether the dataset contract matches the planned model input

Only after that should you write the final `Dataset` and `DataLoader` logic.

## Promote Useful Inspectors

If the inspection script is generally useful, keep it under `scripts/` instead of treating it as disposable.
