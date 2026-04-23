import torch


def compute_accuracy(logits: torch.Tensor, targets: torch.Tensor) -> float:
    predictions = logits.argmax(dim=-1)  # [B, num_classes] -> [B]
    correct = (predictions == targets).float()  # [B]
    return correct.mean().item()
