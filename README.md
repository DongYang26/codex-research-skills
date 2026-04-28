# Research Coding Skills

Research-focused skills for ML and AI experiment repositories, designed to work well in both Codex and Claude Code.

## Repository Layout

```text
skills/
  research-experiment-coding/
```

## Included Skills

### `research-experiment-coding`

An ML-engineer-grade research coding skill with a strong PyTorch bias.

This skill pushes the agent toward classic open-source paper-repo style instead of generic app or backend engineering style.

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

## Install In Codex

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

## Install In Claude Code

Clone the repository, then copy the same skill into Claude Code's default discovery path:

```bash
git clone git@github.com:DongYang26/codex-research-skills.git
cd codex-research-skills
mkdir -p ~/.claude/skills
cp -R skills/research-experiment-coding ~/.claude/skills/
```

If you already have the repository locally, the minimal install step is:

```bash
mkdir -p ~/.claude/skills
cp -R skills/research-experiment-coding ~/.claude/skills/
```

Claude Code can ignore Codex-specific UI metadata such as `agents/openai.yaml`; the main `SKILL.md`, `references/`, and `assets/` remain the important shared pieces.

## Update Workflow

1. Edit the skill inside this repository.
2. Validate the skill locally.
3. Commit and push.
4. Copy or sync the updated skill directory to `~/.codex/skills/` or `~/.claude/skills/` on each machine.

## Validate

If the system skill authoring tools are available locally, validate with:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/research-experiment-coding
```
