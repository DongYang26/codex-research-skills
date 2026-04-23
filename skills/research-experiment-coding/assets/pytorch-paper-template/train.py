import argparse
import json
import random
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.optim import Adam
from tqdm import tqdm

from datasets.random_dataset import build_dataloaders
from models.simple_classifier import SimpleClassifier
from utils.checkpoint import save_checkpoint
from utils.metrics import compute_accuracy

try:
    from torch.utils.tensorboard import SummaryWriter
except Exception:  # pragma: no cover - template fallback
    SummaryWriter = None


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a PyTorch paper experiment.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed to use. Default: 42.")
    parser.add_argument(
        "--train-size",
        type=int,
        default=1024,
        help="Number of synthetic training examples. Default: 1024.",
    )
    parser.add_argument(
        "--val-size",
        type=int,
        default=256,
        help="Number of synthetic validation examples. Default: 256.",
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
        help="Mini-batch size for training and validation. Default: 64.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Number of training epochs. Default: 10.",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=1e-3,
        help="Learning rate for Adam. Default: 1e-3.",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=0,
        help="Number of dataloader workers. Default: 0.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/template-run"),
        help="Directory used to save configs, logs, and checkpoints. Default: results/template-run.",
    )
    return parser.parse_args()


def build_writer(log_dir: Path):
    if SummaryWriter is None:
        return None
    return SummaryWriter(log_dir=str(log_dir))


def train_one_epoch(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
) -> dict[str, float]:
    model.train()
    running_loss = 0.0
    running_correct = 0
    running_examples = 0

    progress = tqdm(loader, desc="train", leave=False)
    for inputs, targets in progress:
        inputs = inputs.to(device)  # [B, input_dim]
        targets = targets.to(device)  # [B]

        optimizer.zero_grad(set_to_none=True)
        logits = model(inputs)  # [B, input_dim] -> [B, num_classes]
        loss = criterion(logits, targets)
        loss.backward()
        optimizer.step()

        batch_size = targets.size(0)
        running_loss += loss.item() * batch_size
        running_correct += (logits.argmax(dim=-1) == targets).sum().item()
        running_examples += batch_size
        progress.set_postfix(loss=loss.item())

    metrics = {
        "loss": running_loss / running_examples,
        "accuracy": running_correct / running_examples,
    }
    return metrics


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
        progress = tqdm(loader, desc="eval", leave=False)
        for inputs, targets in progress:
            inputs = inputs.to(device)  # [B, input_dim]
            targets = targets.to(device)  # [B]

            logits = model(inputs)  # [B, input_dim] -> [B, num_classes]
            loss = criterion(logits, targets)

            batch_size = targets.size(0)
            running_loss += loss.item() * batch_size
            running_correct += compute_accuracy(logits, targets) * batch_size
            running_examples += batch_size

    metrics = {
        "loss": running_loss / running_examples,
        "accuracy": running_correct / running_examples,
    }
    return metrics


def save_resolved_config(args: argparse.Namespace, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = output_dir / "config.json"
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(vars(args), f, indent=2, default=str)


def main() -> None:
    args = parse_args()
    seed_everything(args.seed)
    save_resolved_config(args, args.output_dir)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader, val_loader = build_dataloaders(args)
    model = SimpleClassifier(
        input_dim=args.input_dim,
        hidden_dim=args.hidden_dim,
        num_classes=args.num_classes,
    ).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=args.lr)
    writer = build_writer(args.output_dir / "tb")

    best_val_acc = float("-inf")
    for epoch in range(args.epochs):
        train_metrics = train_one_epoch(model, train_loader, optimizer, criterion, device)
        val_metrics = evaluate(model, val_loader, criterion, device)

        if writer is not None:
            writer.add_scalar("train/loss", train_metrics["loss"], epoch)
            writer.add_scalar("train/accuracy", train_metrics["accuracy"], epoch)
            writer.add_scalar("val/loss", val_metrics["loss"], epoch)
            writer.add_scalar("val/accuracy", val_metrics["accuracy"], epoch)

        if val_metrics["accuracy"] > best_val_acc:
            best_val_acc = val_metrics["accuracy"]
            save_checkpoint(
                path=args.output_dir / "best.pt",
                model=model,
                optimizer=optimizer,
                epoch=epoch,
                metrics=val_metrics,
            )

        print(
            f"epoch={epoch:03d} "
            f"train_loss={train_metrics['loss']:.4f} "
            f"train_acc={train_metrics['accuracy']:.4f} "
            f"val_loss={val_metrics['loss']:.4f} "
            f"val_acc={val_metrics['accuracy']:.4f}"
        )

    if writer is not None:
        writer.close()


if __name__ == "__main__":
    main()
