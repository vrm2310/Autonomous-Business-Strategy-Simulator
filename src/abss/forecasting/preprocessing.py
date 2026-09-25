from pathlib import Path
from typing import Any, cast

import joblib
from sklearn.model_selection import train_test_split # pyright: ignore[reportUnknownVariableType]
from sklearn.preprocessing import StandardScaler


class ForecastPreprocessor:
    def __init__(self) -> None:
        self.feature_scaler = StandardScaler()
        self.target_scaler = StandardScaler()

    def split_data(
        self,
        features: list[list[float]],
        targets: list[list[float]],
        validation_size: float = 0.2,
        random_state: int = 42,
    ) -> tuple[
        list[list[float]],
        list[list[float]],
        list[list[float]],
        list[list[float]],
    ]:
        split_function = cast(Any, train_test_split)

        split_data = split_function(
            features,
            targets,
            test_size=validation_size,
            random_state=random_state,
        )

        train_features = cast(list[list[float]], split_data[0])
        validation_features = cast(list[list[float]], split_data[1])
        train_targets = cast(list[list[float]], split_data[2])
        validation_targets = cast(list[list[float]], split_data[3])

        return (
            train_features,
            validation_features,
            train_targets,
            validation_targets,
        )

    def fit_transform(
        self,
        train_features: list[list[float]],
        train_targets: list[list[float]],
        validation_features: list[list[float]],
        validation_targets: list[list[float]],
    ) -> tuple[
        list[list[float]],
        list[list[float]],
        list[list[float]],
        list[list[float]],
    ]:
        feature_scaler = cast(Any, self.feature_scaler)
        target_scaler = cast(Any, self.target_scaler)

        scaled_train_features = feature_scaler.fit_transform(
            train_features,
        )

        scaled_validation_features = feature_scaler.transform(
            validation_features,
        )

        scaled_train_targets = target_scaler.fit_transform(
            train_targets,
        )

        scaled_validation_targets = target_scaler.transform(
            validation_targets,
        )

        return (
            scaled_train_features.tolist(),
            scaled_validation_features.tolist(),
            scaled_train_targets.tolist(),
            scaled_validation_targets.tolist(),
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        joblib_module = cast(Any, joblib)

        joblib_module.dump(
            {
                "feature_scaler": self.feature_scaler,
                "target_scaler": self.target_scaler,
            },
            path,
        )

    @staticmethod
    def load(path: Path) -> "ForecastPreprocessor":
        joblib_module = cast(Any, joblib)
        artifact = cast(
            dict[str, Any],
            joblib_module.load(path),
        )

        preprocessor = ForecastPreprocessor()
        preprocessor.feature_scaler = artifact["feature_scaler"]
        preprocessor.target_scaler = artifact["target_scaler"]

        return preprocessor