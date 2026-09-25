from torch import Tensor, nn


class ForecastMLP(nn.Module):
    def __init__(
        self,
        input_size: int = 18,
        hidden_size: int = 64,
        second_hidden_size: int = 32,
        output_size: int = 5,
        dropout: float = 0.10,
    ) -> None:
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, second_hidden_size),
            nn.ReLU(),
            nn.Linear(second_hidden_size, output_size),
        )

    def forward(self, features: Tensor) -> Tensor:
        return self.network(features)