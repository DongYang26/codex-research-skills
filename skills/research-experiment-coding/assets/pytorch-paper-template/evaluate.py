import argparse
from pathlib import Path

import torch
from torch import nn
from tqdm import tqdm

from datasets.random_dataset import build_eval_loader
from models.simple_classifier import SimpleClassifier
from utils.metrics import compute_accuracy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a PyTorch paper experiment.")
    parser.add_argument(
        "--ckpt",
        type=Path,
        required=True,
        help="Checkpoint path to evaluate.",
    )
    parser.add_argument(
        "--eval-size",
        type=int,
        default=256,
        help="Number of synthetic evaluation examples. Default: 256.",
    )
    parser.add_argument(
        "--input-dim",
        type=int,
        default=128,
        help="Input feature dimension. Default: 128.",
    )
    parser.add_argument(
        "--hidden-dim",
        type=int,
        default=256,
        help="Hidden feature dimension for the MLP encoder. Default: 256.",
    )
    parser.add_argument(
        "--num-classes",
        type=int,
        default=10,
        help="Number of classification labels. Default: 10.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Mini-batch size for evaluation. Default: 64.",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=0,
        help="Number of dataloader workers. Default: 0.",
    )
    return parser.parse_args()


def evaluate(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict[str, float]:
    model.eval()
    running_loss = 0.0
    running_correct = 0
    running_examples = 0

    with torch.no_grad():
        progress = tqdm(loader, desc="test", leave=False)
        for inputs, targets in progress:
            inputs = inputs.to(device)  # [B, input_dim]
            targets = targets.to(device)  # [B]

            logits = model(inputs)  # [B, input_dim] -> [B, num_classes]
            loss = criterion(logits, targets)

            batch_size = targets.size(0)
            running_loss += loss.item() * batch_size
            running_correct += compute_accuracy(logits, targets) * batch_size
            running_examples += batch_size

    return {
        "loss": running_loss / running_examples,
        "accuracy": running_correct / running_examples,
    }


def main() -> None:
    args = parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loader = build_eval_loader(args)
    model = SimpleClassifier(
        input_dim=args.input_dim,
        hidden_dim=args.hidden_dim,
        num_classes=args.num_classes,
    ).to(device)
    checkpoint = torch.load(args.ckpt, map_location=device)
    model.load_state_dict(checkpoint["model"])
    metrics = evaluate(model, loader, nn.CrossEntropyLoss(), device)
    print(metrics)


if __name__ == "__main__":
    main()
