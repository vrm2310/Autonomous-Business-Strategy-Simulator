import torch
from torch.utils.data import DataLoader

from abss.forecasting.dataset import ForecastDatasetBuilder
from abss.forecasting.model import ForecastMLP
from abss.forecasting.preprocessing import ForecastPreprocessor
from abss.forecasting.synthetic_data import SyntheticDataGenerator
from abss.forecasting.torch_dataset import ForecastTorchDataset
from abss.forecasting.training import ForecastTrainer, TrainingConfig


def test_end_to_end_forecast_training() -> None:
    generator = SyntheticDataGenerator(seed=42)
    samples = generator.generate_dataset(100)

    features, targets = ForecastDatasetBuilder.build_dataset(samples)

    preprocessor = ForecastPreprocessor()

    (
        train_features,
        validation_features,
        train_targets,
        validation_targets,
    ) = preprocessor.split_data(
        features,
        targets,
    )

    (
        train_features,
        validation_features,
        train_targets,
        validation_targets,
    ) = preprocessor.fit_transform(
        train_features,
        train_targets,
        validation_features,
        validation_targets,
    )

    train_dataset = ForecastTorchDataset(
        features=train_features,
        targets=train_targets,
    )

    validation_dataset = ForecastTorchDataset(
        features=validation_features,
        targets=validation_targets,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=16,
        shuffle=True,
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=16,
        shuffle=False,
    )

    model = ForecastMLP()

    trainer = ForecastTrainer(
        model=model,
        config=TrainingConfig(epochs=3),
    )

    train_history, validation_history = trainer.train(
        train_loader=train_loader,
        validation_loader=validation_loader,
    )

    assert len(train_history) == 3
    assert len(validation_history) == 3

    assert all(torch.isfinite(torch.tensor(train_history)))
    assert all(torch.isfinite(torch.tensor(validation_history)))

    assert train_history[-1] < train_history[0]