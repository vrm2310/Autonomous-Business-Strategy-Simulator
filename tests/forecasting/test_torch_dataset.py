from typing import Any, cast

import pytest
from torch import Tensor

from abss.forecasting.torch_dataset import ForecastTorchDataset


def test_torch_dataset() -> None:
    features = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    targets = [
        [0.7, 0.8],
        [0.9, 1.0],
    ]

    dataset = ForecastTorchDataset(
        features=features,
        targets=targets,
    )

    assert len(dataset) == 2

    feature_tensor, target_tensor = dataset[0]

    assert isinstance(feature_tensor, Tensor)
    assert isinstance(target_tensor, Tensor)

    assert feature_tensor.shape == (3,)
    assert target_tensor.shape == (2,)

    feature_values = cast(
        list[float],
        cast(Any, feature_tensor).tolist(),
    )

    target_values = cast(
        list[float],
        cast(Any, target_tensor).tolist(),
    )

    assert feature_values == pytest.approx(features[0])
    assert target_values == pytest.approx(targets[0])


def test_torch_dataset_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError, match="same length"):
        ForecastTorchDataset(
            features=[[1.0], [2.0]],
            targets=[[1.0]],
        )