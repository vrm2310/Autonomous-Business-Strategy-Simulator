from pathlib import Path
from typing import Any, cast

import torch

from abss.forecasting.artifact import ForecastArtifact
from abss.forecasting.model import ForecastMLP
from abss.forecasting.preprocessing import ForecastPreprocessor


def test_forecast_artifact_save_and_load(
    tmp_path: Path,
) -> None:
    model = ForecastMLP()
    model.eval()

    preprocessor = ForecastPreprocessor()

    train_features = [
        [1.0, 10.0],
        [2.0, 20.0],
        [3.0, 30.0],
    ]

    train_targets = [
        [100.0, 10.0],
        [200.0, 20.0],
        [300.0, 30.0],
    ]

    preprocessor.fit_transform(
        train_features,
        train_targets,
        [[1.5, 15.0]],
        [[150.0, 15.0]],
    )

    path = tmp_path / "forecast_artifact.joblib"

    artifact = ForecastArtifact(
        model=model,
        preprocessor=preprocessor,
        model_version="1.0.0",
    )

    artifact.save(path)

    assert path.exists()

    loaded_artifact = ForecastArtifact.load(path)

    loaded_model = loaded_artifact.model
    loaded_preprocessor = loaded_artifact.preprocessor
    version = loaded_artifact.model_version
    
    features = torch.randn(4, 18)

    original_predictions = model(features)
    loaded_predictions = loaded_model(features)

    assert torch.allclose(
        original_predictions,
        loaded_predictions,
    )

    assert version == "1.0.0"

    feature_scaler = cast(
        Any,
        preprocessor.feature_scaler,
    )

    original_scaled = feature_scaler.transform(
        [[1.5, 15.0]],
    )

    loaded_feature_scaler = cast(
        Any,
        loaded_preprocessor.feature_scaler,
    )

    loaded_scaled = loaded_feature_scaler.transform(
        [[1.5, 15.0]],
    )

    assert loaded_scaled[0].tolist() == (
        original_scaled[0].tolist()
    )