# Tensor Shape And Formula Comments

Use this guide when writing `forward`, attention code, loss functions, sequence packing, reshaping, or non-trivial tensor math.

## Shape Comments

Add inline comments when:

- a tensor changes shape
- broadcasting is non-obvious
- a reshape, flatten, transpose, or gather would force the reader to reason mentally about dimensions

Examples:

```python
x = self.patch_embed(images)  # [B, 3, H, W] -> [B, N, D]
attn = torch.softmax(scores, dim=-1)  # [B, heads, N, N]
context = attn @ values  # [B, heads, N, N] @ [B, heads, N, Dh] -> [B, heads, N, Dh]
```

If several consecutive operations preserve shape, one concise comment for the block is enough.

## Formula Docstrings

If a method implements a paper formula, say so briefly in the docstring.

Examples:

```python
def forward(self, x: torch.Tensor) -> torch.Tensor:
    r"""Compute logits z = W_2 sigma(W_1 x + b_1) + b_2."""
```

```python
def contrastive_loss(q: torch.Tensor, k: torch.Tensor) -> torch.Tensor:
    r"""Compute InfoNCE: L = -log exp(q·k+/tau) / sum_j exp(q·k_j/tau)."""
```

## Comment Style

- Explain mathematical meaning, not Python syntax.
- Prefer short comments over prose paragraphs.
- Use comments to reduce ambiguity, not to narrate every line.
