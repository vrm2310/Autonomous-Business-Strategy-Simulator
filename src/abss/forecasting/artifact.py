from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import joblib

from abss.forecasting.model import ForecastMLP
from abss.forecasting.preprocessing import ForecastPreprocessor


@dataclass
class ForecastArtifact:
    model: ForecastMLP
    preprocessor: ForecastPreprocessor
    model_version: str

    def save(
        self,
        path: Path,
    ) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        artifact: dict[str, Any] = {
            "model_state_dict": self.model.state_dict(),
            "feature_scaler": self.preprocessor.feature_scaler,
            "target_scaler": self.preprocessor.target_scaler,
            "model_version": self.model_version,
        }

        joblib_module = cast(Any, joblib)
        joblib_module.dump(artifact, path)

    @staticmethod
    def load(
        path: Path,
    ) -> "ForecastArtifact":
        joblib_module = cast(Any, joblib)
        artifact = cast(
            dict[str, Any],
            joblib_module.load(path),
        )

        model = ForecastMLP()
        model.load_state_dict(
            artifact["model_state_dict"],
        )
        model.eval()

        preprocessor = ForecastPreprocessor()
        preprocessor.feature_scaler = artifact["feature_scaler"]
        preprocessor.target_scaler = artifact["target_scaler"]

        return ForecastArtifact(
            model=model,
            preprocessor=preprocessor,
            model_version=artifact["model_version"],
        )