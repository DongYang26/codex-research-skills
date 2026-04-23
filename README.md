# Codex Skills

Personal Codex skills for research and paper-writing workflows.

## Repository Layout

```text
skills/
  research-experiment-coding/
```

## Included Skills

### `research-experiment-coding`

A Codex skill for generating paper-style experiment code with a strong PyTorch bias.

It emphasizes:

- explicit `train.py` and `evaluate.py` entrypoints
- lightweight `models/`, `datasets/`, `utils/`, and `configs/` layout
- direct module calls instead of dependency injection or factory-heavy patterns
- reproducibility requirements such as `seed_everything`, saved configs, metrics logs, and best-checkpoint tracking
- tensor shape comments and short formula docstrings for math-heavy code

The skill folder lives at:

```text
skills/research-experiment-coding/
```

## Install On Another Codex Machine

Default Codex discovery path:

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
