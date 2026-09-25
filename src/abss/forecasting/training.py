from dataclasses import dataclass

import torch
from torch import Tensor, nn
from torch.optim import Adam
from torch.utils.data import DataLoader

from abss.forecasting.model import ForecastMLP


@dataclass(frozen=True)
class TrainingConfig:
    learning_rate: float = 0.001
    epochs: int = 50


class ForecastTrainer:
    def __init__(
        self,
        model: ForecastMLP,
        config: TrainingConfig | None = None,
    ) -> None:
        self.model = model
        self.config = config or TrainingConfig()

        self.loss_function = nn.MSELoss()
        self.optimizer = Adam(
            self.model.parameters(),
            lr=self.config.learning_rate,
        )

    def train_epoch(
        self,
        data_loader: DataLoader[tuple[Tensor, Tensor]],
    ) -> float:
        self.model.train()

        total_loss = 0.0
        batch_count = 0

        for features, targets in data_loader:
            self.optimizer.zero_grad()

            predictions = self.model(features)

            loss = self.loss_function(
                predictions,
                targets,
            )

            loss.backward()
            self.optimizer.step() # pyright: ignore[reportUnknownMemberType]

            total_loss += loss.item()
            batch_count += 1

        return total_loss / batch_count

    def train(
        self,
        train_loader: DataLoader[tuple[Tensor, Tensor]],
        validation_loader: DataLoader[tuple[Tensor, Tensor]],
    ) -> tuple[list[float], list[float]]:
        train_history: list[float] = []
        validation_history: list[float] = []
    
        for _ in range(self.config.epochs):
            train_loss = self.train_epoch(train_loader)
            validation_loss = self.validate(validation_loader)
    
            train_history.append(train_loss)
            validation_history.append(validation_loss)
    
        return train_history, validation_history

    def validate(
        self,
        data_loader: DataLoader[tuple[Tensor, Tensor]],
    ) -> float:
        self.model.eval()

        total_loss = 0.0
        batch_count = 0

        with torch.no_grad():
            for features, targets in data_loader:
                predictions = self.model(features)

                loss = self.loss_function(
                    predictions,
                    targets,
                )

                total_loss += loss.item()
                batch_count += 1

        return total_loss / batch_count