# Tensor Debugging Protocol

Use this guide when debugging tensor shape, dtype, broadcasting, or device errors.

## No Guesswork

Do not randomly apply:

- `.squeeze()`
- `.unsqueeze()`
- `.reshape()`
- `.view()`
- `.transpose()`
- `.permute()`

just to silence a runtime error.

## Minimum Diagnostic Pass

Before editing the failing math, log the exact properties of the tensors involved:

- `.shape`
- `.dtype`
- `.device`

If relevant, also log:

- batch size
- sequence length
- head count
- feature dimension
- target shape

Example:

```python
print("q", q.shape, q.dtype, q.device)
print("k", k.shape, k.dtype, k.device)
print("scores", scores.shape, scores.dtype, scores.device)
```

## Debug Against The Intended Math

After logging, explain the mismatch in mathematical terms:

- which dimensions are supposed to align
- which tensor is on the wrong device
- which dtype is incompatible with the operation
- whether the code violates the paper's formula

Only then make the minimal edit needed to restore the intended computation.

## Acceptable Fix Pattern

1. log tensor metadata
2. identify the expected tensor contract
3. state the mismatch explicitly
4. apply the smallest corrective change
5. rerun the failing path

## Avoid These Anti-Patterns

- adding shape hacks without explanation
- changing both math and data layout at once
- converting everything to `float()` or moving everything to `.cuda()` blindly
- removing dimensions until the code "works"
