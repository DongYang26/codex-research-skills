# Codex Research Skills

Research-focused Codex skills for ML and AI experiment repositories.

## Repository Layout

```text
skills/
  research-experiment-coding/
```

## Included Skills

### `research-experiment-coding`

A Codex skill for ML-engineer-grade research coding with a strong PyTorch bias.

This skill pushes Codex toward classic open-source paper-repo style instead of generic app or backend engineering style.

It emphasizes:

- explicit `train.py` and `evaluate.py` entrypoints
- lightweight `models/`, `datasets/`, `utils/`, and `configs/` layout
- direct module calls instead of dependency injection or factory-heavy patterns
- reproducibility requirements such as `seed_everything`, saved configs, metrics logs, and best-checkpoint tracking
- disciplined environment and GPU execution conventions
- tensor shape comments and short formula docstrings for math-heavy code
- no-guesswork tensor debugging with explicit shape, dtype, and device inspection
- data profiling before writing non-trivial `Dataset` or preprocessing code
- non-destructive git checkpointing for risky experiment work
- cleanup rules for temporary debug artifacts and scratch outputs

The skill folder lives at:

```text
skills/research-experiment-coding/
```

## Why This Skill Exists

Many general coding skills optimize for product or application engineering. This skill instead optimizes for research repositories where the priorities are:

- readable training and evaluation paths
- faithful implementation of paper math
- reproducibility and auditability
- cautious debugging and environment handling
- outputs that are easy to turn into tables, figures, and release artifacts

## Install On Another Codex Machine

Clone the repository, then copy the skill into Codex's default discovery path:

```bash
git clone git@github.com:DongYang26/codex-research-skills.git
cd codex-research-skills
mkdir -p ~/.codex/skills
cp -R skills/research-experiment-coding ~/.codex/skills/
```

If you already have the repository locally, the minimal install step is:

```bash
mkdir -p ~/.codex/skills
cp -R skills/research-experiment-coding ~/.codex/skills/
```

Then restart Codex so it can discover the new skill.

## Update Workflow

1. Edit the skill inside this repository.
2. Validate the skill locally.
3. Commit and push.
4. Copy or sync the updated skill directory to `~/.codex/skills/` on each machine.

## Validate

If the system skill authoring tools are available locally, validate with:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/research-experiment-coding
```
