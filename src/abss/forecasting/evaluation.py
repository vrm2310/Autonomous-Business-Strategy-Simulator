from dataclasses import dataclass
from typing import Any, cast

import numpy as np
import torch

from abss.forecasting.model import ForecastMLP
from abss.forecasting.preprocessing import ForecastPreprocessor


@dataclass(frozen=True)
class ForecastEvaluationResult:
    mse: float
    mae: float


class ForecastEvaluator:
    def __init__(
        self,
        model: ForecastMLP,
        preprocessor: ForecastPreprocessor,
    ) -> None:
        self.model = model
        self.preprocessor = preprocessor

    def evaluate(
        self,
        features: list[list[float]],
        targets: list[list[float]],
    ) -> ForecastEvaluationResult:
        feature_scaler = cast(Any, self.preprocessor.feature_scaler)
        target_scaler = cast(Any, self.preprocessor.target_scaler)

        scaled_features = feature_scaler.transform(
            features,
        )

        scaled_targets = target_scaler.transform(
            targets,
        )

        scaled_targets = cast(np.ndarray, scaled_targets)

        input_tensor = torch.tensor(
            scaled_features,
            dtype=torch.float32,
        )

        self.model.eval()

        with torch.no_grad():
            predictions = self.model(input_tensor).numpy()

        predictions = cast(np.ndarray, predictions)

        mse = float(
            np.mean(
                np.square(
                    scaled_targets - predictions,
                ),
            ),
        )

        mae = float(
            np.mean(
                np.abs(
                    scaled_targets - predictions,
                ),
            ),
        )

        return ForecastEvaluationResult(
            mse=mse,
            mae=mae,
        )