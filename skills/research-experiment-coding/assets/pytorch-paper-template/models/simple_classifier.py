import torch
from torch import nn


class SimpleClassifier(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, num_classes: int) -> None:
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
        )
        self.classifier = nn.Linear(hidden_dim, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        r"""Compute logits z = W_2 sigma(W_1 x + b_1) + b_2."""
        hidden = self.encoder(x)  # [B, input_dim] -> [B, hidden_dim]
        logits = self.classifier(hidden)  # [B, hidden_dim] -> [B, num_classes]
        return logits
