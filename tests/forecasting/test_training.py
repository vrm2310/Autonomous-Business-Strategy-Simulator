from typing import Any, cast

import torch
from torch.utils.data import DataLoader

from abss.forecasting.model import ForecastMLP
from abss.forecasting.torch_dataset import ForecastTorchDataset
from abss.forecasting.training import ForecastTrainer, TrainingConfig


def random_data(
    rows: int,
    columns: int,
) -> list[list[float]]:
    tensor = torch.randn(rows, columns)

    return cast(
        list[list[float]],
        cast(Any, tensor).tolist(),
    )


def test_training_config_defaults() -> None:
    config = TrainingConfig()

    assert config.learning_rate == 0.001
    assert config.epochs == 50


def test_train_epoch_returns_loss() -> None:
    features = random_data(32, 18)
    targets = random_data(32, 5)

    dataset = ForecastTorchDataset(
        features=features,
        targets=targets,
    )

    data_loader = DataLoader(
        dataset,
        batch_size=16,
        shuffle=True,
    )

    model = ForecastMLP()
    trainer = ForecastTrainer(model)

    loss = trainer.train_epoch(data_loader)

    assert isinstance(loss, float)
    assert loss >= 0.0

def test_train_returns_train_and_validation_history() -> None:
    features = random_data(32, 18)
    targets = random_data(32, 5)

    dataset = ForecastTorchDataset(
        features=features,
        targets=targets,
    )

    data_loader = DataLoader(
        dataset,
        batch_size=16,
        shuffle=True,
    )

    model = ForecastMLP()
    config = TrainingConfig(epochs=3)

    trainer = ForecastTrainer(
        model=model,
        config=config,
    )

    train_history, validation_history = trainer.train(
        train_loader=data_loader,
        validation_loader=data_loader,
    )

    assert len(train_history) == 3
    assert len(validation_history) == 3

    assert all(loss >= 0.0 for loss in train_history)
    assert all(loss >= 0.0 for loss in validation_history)

def test_validate_returns_loss() -> None:
    features = random_data(32, 18)
    targets = random_data(32, 5)

    dataset = ForecastTorchDataset(
        features=features,
        targets=targets,
    )

    data_loader = DataLoader(
        dataset,
        batch_size=16,
        shuffle=False,
    )

    model = ForecastMLP()
    trainer = ForecastTrainer(model)

    validation_loss = trainer.validate(data_loader)

    assert isinstance(validation_loss, float)
    assert validation_loss >= 0.0