# Safe Experiment Checkpointing

Use this guide to preserve progress without destructive git behavior.

## Small, Intentional Checkpoints

When a concrete sub-task is known to work, prefer a small checkpoint:

- verified dataloader
- shape-safe forward pass
- stable training loop
- working evaluation path

Stage explicit file paths when the worktree may contain unrelated changes.

Avoid defaulting to:

```bash
git add .
```

unless the entire repository state is clearly in scope.

## Before High-Risk Changes

Before sweeping refactors or speculative debugging:

- consider a temporary branch
- or save a stash or patch
- or make a small checkpoint commit first

Choose the least disruptive reversible state.

## No Automatic Destructive Reset

Do not automatically use:

- `git reset --hard`
- broad `git checkout --`
- destructive history rewrites

If a fix path fails repeatedly, step back and choose a different strategy. Revert only changes you own and only when the ownership is clear.

## Goal

The purpose of checkpointing is:

- preserve working milestones
- reduce fear of experimentation
- avoid losing user work
- keep debugging reversible
