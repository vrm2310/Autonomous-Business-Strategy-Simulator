from torch.utils.data import DataLoader

from abss.forecasting.dataset import ForecastDatasetBuilder
from abss.forecasting.evaluation import ForecastEvaluator
from abss.forecasting.model import ForecastMLP
from abss.forecasting.preprocessing import ForecastPreprocessor
from abss.forecasting.synthetic_data import SyntheticDataGenerator
from abss.forecasting.torch_dataset import ForecastTorchDataset
from abss.forecasting.training import ForecastTrainer, TrainingConfig


def test_trained_forecast_model_can_be_evaluated() -> None:
    generator = SyntheticDataGenerator(seed=42)

    samples = generator.generate_dataset(100)

    features, targets = ForecastDatasetBuilder.build_dataset(
        samples,
    )

    preprocessor = ForecastPreprocessor()

    (
        train_features,
        validation_features,
        train_targets,
        validation_targets,
    ) = preprocessor.split_data(
        features,
        targets,
        validation_size=0.2,
        random_state=42,
    )

    (
        scaled_train_features,
        scaled_validation_features,
        scaled_train_targets,
        scaled_validation_targets,
    ) = preprocessor.fit_transform(
        train_features,
        train_targets,
        validation_features,
        validation_targets,
    )

    train_dataset = ForecastTorchDataset(
        scaled_train_features,
        scaled_train_targets,
    )

    validation_dataset = ForecastTorchDataset(
        scaled_validation_features,
        scaled_validation_targets,
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
        model,
        TrainingConfig(
            learning_rate=0.001,
            epochs=10,
        ),
    )

    initial_validation_loss = trainer.validate(
        validation_loader,
    )

    train_history, validation_history = trainer.train(
        train_loader,
        validation_loader,
    )

    evaluator = ForecastEvaluator(
        model=model,
        preprocessor=preprocessor,
    )

    result = evaluator.evaluate(
        validation_features,
        validation_targets,
    )

    assert len(train_history) == 10
    assert len(validation_history) == 10

    final_validation_loss = validation_history[-1]

    assert final_validation_loss < initial_validation_loss

    assert result.mse >= 0
    assert result.mae >= 0