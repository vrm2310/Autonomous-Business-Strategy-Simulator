from pathlib import Path

import torch

from abss.forecasting.model import ForecastMLP


class ForecastModelPersistence:
    @staticmethod
    def save(
        model: ForecastMLP,
        path: Path,
    ) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        torch.save(
            model.state_dict(),
            path,
        )

    @staticmethod
    def load(
        path: Path,
    ) -> ForecastMLP:
        model = ForecastMLP()

        state_dict = torch.load(
            path,
            map_location="cpu",
        )

        model.load_state_dict(state_dict)
        model.eval()

        return model