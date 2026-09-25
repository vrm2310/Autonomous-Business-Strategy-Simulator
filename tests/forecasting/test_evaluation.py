import math

from abss.forecasting.evaluation import (
    ForecastEvaluationResult,
    ForecastEvaluator,
)
from abss.forecasting.model import ForecastMLP
from abss.forecasting.preprocessing import ForecastPreprocessor


def create_test_evaluator() -> ForecastEvaluator:
    model = ForecastMLP()
    preprocessor = ForecastPreprocessor()

    train_features = [
        [1.0] * 18,
        [2.0] * 18,
        [3.0] * 18,
    ]

    train_targets = [
        [100.0, 20.0, 50.0, 10.0, 0.10],
        [200.0, 40.0, 100.0, 20.0, 0.20],
        [300.0, 60.0, 150.0, 30.0, 0.30],
    ]

    preprocessor.fit_transform(
        train_features,
        train_targets,
        [[1.5] * 18],
        [[150.0, 30.0, 75.0, 15.0, 0.15]],
    )

    return ForecastEvaluator(
        model=model,
        preprocessor=preprocessor,
    )


def test_forecast_evaluator_returns_result() -> None:
    evaluator = create_test_evaluator()

    result = evaluator.evaluate(
        features=[
            [1.5] * 18,
            [2.0] * 18,
        ],
        targets=[
            [150.0, 30.0, 75.0, 15.0, 0.15],
            [200.0, 40.0, 100.0, 20.0, 0.20],
        ],
    )

    assert isinstance(result, ForecastEvaluationResult)
    assert isinstance(result.mse, float)
    assert isinstance(result.mae, float)


def test_forecast_evaluator_returns_finite_metrics() -> None:
    evaluator = create_test_evaluator()

    result = evaluator.evaluate(
        features=[
            [1.5] * 18,
            [2.0] * 18,
        ],
        targets=[
            [150.0, 30.0, 75.0, 15.0, 0.15],
            [200.0, 40.0, 100.0, 20.0, 0.20],
        ],
    )

    assert math.isfinite(result.mse)
    assert math.isfinite(result.mae)
    assert result.mse >= 0
    assert result.mae >= 0