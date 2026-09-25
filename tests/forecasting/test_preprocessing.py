from abss.forecasting.dataset import ForecastDatasetBuilder
from abss.forecasting.preprocessing import ForecastPreprocessor
from abss.forecasting.synthetic_data import SyntheticDataGenerator


def test_split_data() -> None:
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

    assert len(train_features) == 80
    assert len(validation_features) == 20
    assert len(train_targets) == 80
    assert len(validation_targets) == 20

    assert all(len(row) == 18 for row in train_features)
    assert all(len(row) == 5 for row in train_targets)

def test_fit_transform_scales_data() -> None:
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
        scaled_validation_features,
        scaled_train_targets,
        scaled_validation_targets,
    ) = preprocessor.fit_transform(
        train_features=train_features,
        train_targets=train_targets,
        validation_features=validation_features,
        validation_targets=validation_targets,
    )

    assert len(scaled_train_features) == 80
    assert len(scaled_validation_features) == 20
    assert len(scaled_train_targets) == 80
    assert len(scaled_validation_targets) == 20

    assert len(scaled_train_features[0]) == 18
    assert len(scaled_train_targets[0]) == 5

def test_scaled_training_data_is_standardized() -> None:
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

    feature_means = [
        sum(row[i] for row in scaled_train_features)
        / len(scaled_train_features)
        for i in range(18)
    ]

    target_means = [
        sum(row[i] for row in scaled_train_targets)
        / len(scaled_train_targets)
        for i in range(5)
    ]

    assert all(abs(mean) < 1e-6 for mean in feature_means)
    assert all(abs(mean) < 1e-6 for mean in target_means)