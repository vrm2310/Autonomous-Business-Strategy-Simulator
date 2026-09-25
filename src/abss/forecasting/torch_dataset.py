from torch import Tensor
from torch.utils.data import Dataset


class ForecastTorchDataset(Dataset[tuple[Tensor, Tensor]]):
    def __init__(
        self,
        features: list[list[float]],
        targets: list[list[float]],
    ) -> None:
        if len(features) != len(targets):
            raise ValueError(
                "features and targets must have the same length",
            )

        self.features = [
            Tensor(row)
            for row in features
        ]

        self.targets = [
            Tensor(row)
            for row in targets
        ]

    def __len__(self) -> int:
        return len(self.features)

    def __getitem__(
        self,
        index: int,
    ) -> tuple[Tensor, Tensor]:
        return self.features[index], self.targets[index]