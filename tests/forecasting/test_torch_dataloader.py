from torch.utils.data import DataLoader

from abss.forecasting.dataset import ForecastDatasetBuilder
from abss.forecasting.preprocessing import ForecastPreprocessor
from abss.forecasting.synthetic_data import SyntheticDataGenerator
from abss.forecasting.torch_dataset import ForecastTorchDataset


def test_forecast_dataloader() -> None:
    generator = SyntheticDataGenerator(seed=42)
    samples = generator.generate_dataset(num_samples=100)

    features, targets = ForecastDatasetBuilder.build_dataset(samples)

    preprocessor = ForecastPreprocessor()

    (
        train_features,
        validation_features,
        train_targets,
        validation_targets,
    ) = preprocessor.split_data(
        features=features,
        targets=targets,
    )

    (
        scaled_train_features,
        _scaled_validation_features,
        scaled_train_targets,
        _scaled_validation_targets,
    ) = preprocessor.fit_transform(
        train_features=train_features,
        train_targets=train_targets,
        validation_features=validation_features,
        validation_targets=validation_targets,
    )

    train_dataset = ForecastTorchDataset(
        features=scaled_train_features,
        targets=scaled_train_targets,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=16,
        shuffle=True,
    )

    feature_batch, target_batch = next(iter(train_loader))

    assert feature_batch.shape == (16, 18)
    assert target_batch.shape == (16, 5)