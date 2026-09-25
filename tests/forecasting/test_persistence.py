from pathlib import Path

import torch

from abss.forecasting.model import ForecastMLP
from abss.forecasting.persistence import ForecastModelPersistence


def test_save_and_load_model(tmp_path: Path) -> None:
    model = ForecastMLP()

    model_path = tmp_path / "forecast_model.pt"

    ForecastModelPersistence.save(
        model=model,
        path=model_path,
    )

    assert model_path.exists()

    loaded_model = ForecastModelPersistence.load(
        path=model_path,
    )

    features = torch.randn(4, 18)

    model.eval()

    original_predictions = model(features)
    loaded_predictions = loaded_model(features)

    assert torch.allclose(
        original_predictions,
        loaded_predictions,
    )