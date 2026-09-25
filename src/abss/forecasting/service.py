import numpy as np
import torch
from typing import Any, cast

from abss.core.models import (
    ForecastFeatures,
    ForecastPoint,
    ForecastResult,
)
from abss.forecasting.artifact import ForecastArtifact
from abss.forecasting.dataset import ForecastDatasetBuilder


class ForecastService:
    def __init__(
        self,
        artifact: ForecastArtifact,
        forecast_horizon: int = 4,
    ) -> None:
        if forecast_horizon <= 0:
            raise ValueError(
                "forecast_horizon must be greater than zero",
            )

        self.artifact = artifact
        self.forecast_horizon = forecast_horizon

    @staticmethod
    def update_features_from_forecast(
        features: ForecastFeatures,
        forecast: ForecastPoint,
    ) -> ForecastFeatures:
        return features.model_copy(
            update={
                "revenue": forecast.revenue,
                "profit": forecast.profit,
                "cash": forecast.cash,
                "inventory": forecast.inventory,
                "market_share": forecast.market_share,
            },
        )

    def predict(
        self,
        cycle_id: int,
        features: ForecastFeatures,
    ) -> ForecastResult:
        current_features = features
        points: list[ForecastPoint] = []
    
        for horizon in range(1, self.forecast_horizon + 1):
            feature_vector = (
                ForecastDatasetBuilder.features_to_vector_from_features(
                    current_features,
                )
            )

            feature_scaler = cast(
                Any,
                self.artifact.preprocessor.feature_scaler,
            )

            scaled_features = feature_scaler.transform(
                [feature_vector],
            )
            input_tensor = torch.tensor(
                scaled_features,
                dtype=torch.float32,
            )
    
            with torch.no_grad():
                scaled_prediction = self.artifact.model(
                    input_tensor,
                ).numpy()
    
            target_scaler = cast(
                Any,
                self.artifact.preprocessor.target_scaler,
            )
            
            prediction = target_scaler.inverse_transform(
                scaled_prediction,
            )[0]
            
            prediction = cast(
                np.ndarray,
                prediction,
            )
    
            point = ForecastPoint(
                horizon=horizon,
                revenue=float(prediction[0]),
                profit=float(prediction[1]),
                cash=float(prediction[2]),
                inventory=float(prediction[3]),
                market_share=float(prediction[4]),
            )

            points.append(point)
    
            current_features = self.update_features_from_forecast(
                current_features,
                point,
            )

        return ForecastResult(
            cycle_id=cycle_id,
            horizon=self.forecast_horizon,
            points=points,
            model_version=self.artifact.model_version,
        )