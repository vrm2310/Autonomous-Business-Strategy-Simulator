from abss.core.models import MarketState


class MarketEnvironmentService:
    def __init__(
        self,
        demand_index: float = 1.0,
        inflation_rate: float = 0.04,
        interest_rate: float = 0.06,
        competitor_pressure: float = 0.50,
        seasonality_index: float = 1.0,
    ) -> None:
        self.demand_index = demand_index
        self.inflation_rate = inflation_rate
        self.interest_rate = interest_rate
        self.competitor_pressure = competitor_pressure
        self.seasonality_index = seasonality_index

    def get_current_market_state(self) -> MarketState:
        return MarketState(
            demand_index=self.demand_index,
            inflation_rate=self.inflation_rate,
            interest_rate=self.interest_rate,
            competitor_pressure=self.competitor_pressure,
            seasonality_index=self.seasonality_index,
        )