import torch
from torch.utils.data import DataLoader, Dataset


class RandomClassificationDataset(Dataset):
    def __init__(self, num_samples: int, input_dim: int, num_classes: int) -> None:
        self.features = torch.randn(num_samples, input_dim)  # [N, input_dim]
        self.labels = torch.randint(0, num_classes, (num_samples,))  # [N]

    def __len__(self) -> int:
        return self.features.size(0)

    def __getitem__(self, index: int):
        x = self.features[index]  # [input_dim]
        y = self.labels[index]  # []
        return x, y


def build_dataloaders(args):
    train_dataset = RandomClassificationDataset(
        num_samples=args.train_size,
        input_dim=args.input_dim,
        num_classes=args.num_classes,
    )
    val_dataset = RandomClassificationDataset(
        num_samples=args.val_size,
        input_dim=args.input_dim,
        num_classes=args.num_classes,
    )
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
    )
    return train_loader, val_loader


def build_eval_loader(args):
    dataset = RandomClassificationDataset(
        num_samples=args.eval_size,
        input_dim=args.input_dim,
        num_classes=args.num_classes,
    )
    return DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
    )
