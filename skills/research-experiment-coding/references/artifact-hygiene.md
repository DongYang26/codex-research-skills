# Ephemeral Artifact Hygiene

Use this guide when creating temporary files for smoke tests, diagnostics, or mocked-data validation.

## Use Scratch Locations

Prefer a dedicated scratch location such as:

- `.agent_tmp/`
- `tmp/agent/`
- `artifacts/debug/`

Do not scatter temporary files through source directories unless there is a strong reason.

## Promote Or Discard Intentionally

If a helper is reusable:

- move it into `scripts/`
- or another stable project location

If it is a one-off debug artifact:

- clean it up before declaring the task complete

## Never Delete Canonical Outputs Blindly

Do not remove:

- real datasets
- real checkpoints
- final evaluation metrics
- user-authored scripts
- meaningful experiment outputs

Clean up only files the agent created and can confidently classify as throwaway.

## `.gitignore` Hygiene

If transient paths need to remain locally but should not be tracked, add clear ignore rules such as:

- `.agent_tmp/`
- `tmp/agent/`
- `wandb/`
- `lightning_logs/`
- `__pycache__/`
- `core.*`

Prefer repository-local ignore rules that make scratch artifacts predictable and easy to manage.

## Non-Destructive Default

If ownership or usefulness is ambiguous, keep the file and ask before deleting it.
