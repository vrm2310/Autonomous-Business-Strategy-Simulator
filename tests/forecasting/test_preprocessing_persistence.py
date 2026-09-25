from pathlib import Path
from typing import Any, cast

import pytest

from abss.forecasting.preprocessing import ForecastPreprocessor


def test_preprocessor_save_and_load(tmp_path: Path) -> None:
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

    validation_features = [
        [1.5, 15.0],
    ]

    validation_targets = [
        [150.0, 15.0],
    ]

    (
        scaled_train_features,
        _,
        scaled_train_targets,
        _,
    ) = preprocessor.fit_transform(
        train_features,
        train_targets,
        validation_features,
        validation_targets,
    )

    path = tmp_path / "preprocessor.joblib"

    preprocessor.save(path)

    loaded = ForecastPreprocessor.load(path)

    loaded_feature_scaler = cast(
        Any,
        loaded.feature_scaler,
    )
    
    loaded_target_scaler = cast(
        Any,
        loaded.target_scaler,
    )
    
    original_feature_scaler = cast(
        Any,
        preprocessor.feature_scaler,
    )
    
    original_target_scaler = cast(
        Any,
        preprocessor.target_scaler,
    )
    
    loaded_features = loaded_feature_scaler.transform(
        validation_features,
    ).tolist()
    
    loaded_targets = loaded_target_scaler.transform(
        validation_targets,
    ).tolist()
    
    original_features = original_feature_scaler.transform(
        validation_features,
    ).tolist()
    
    original_targets = original_target_scaler.transform(
        validation_targets,
    ).tolist()

    assert scaled_train_features
    assert scaled_train_targets

    assert loaded_features[0] == pytest.approx(
        original_features[0],
    )
    
    assert loaded_targets[0] == pytest.approx(
        original_targets[0],
    )