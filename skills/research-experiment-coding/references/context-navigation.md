# Focused Repository Reading

Use this guide when entering a new or large repository.

## Structure Before Source

Start with repository structure:

- `tree -L 2`
- `ls -la`
- `find` or `rg --files` when needed

Do not open large source files blindly.

## Symbol-First Search

Locate the exact target before reading:

- `rg -n "class Name"`
- `rg -n "def function_name"`
- `rg -n "train_one_epoch|evaluate|main"`

Use the search result to identify the right file and nearby line range.

## Read Narrowly

Prefer partial reads:

- `sed -n 'start,endp' file.py`
- `head`
- `tail`
- targeted editor jumps

Read the smallest relevant slice that explains the behavior you need to change.

## Expand Only When Necessary

Widen the read only when:

- the surrounding call chain is unclear
- the symbol depends on nearby helpers
- the file-level architecture matters for the change

The default is narrow context, not full-file scanning.

## Goal

Keep token usage focused and preserve a precise mental model of:

- where the target logic lives
- what calls it
- what it depends on
- which files actually need editing
