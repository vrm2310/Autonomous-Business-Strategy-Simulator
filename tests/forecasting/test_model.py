import torch

from abss.forecasting.model import ForecastMLP


def test_forecast_mlp_output_shape() -> None:
    model = ForecastMLP()

    features = torch.randn(16, 18)

    predictions = model(features)

    assert predictions.shape == (16, 5)


def test_forecast_mlp_single_prediction() -> None:
    model = ForecastMLP()

    features = torch.randn(1, 18)

    predictions = model(features)

    assert predictions.shape == (1, 5)