import random

from abss.core.models import (
    CompanyState,
    ForecastPoint,
    ForecastTrainingSample,
    MarketState,
    SimulationEvent,
)
from abss.events.service import EventGeneratorService
from abss.features.service import FeatureEngineeringService


class SyntheticDataGenerator:
    def __init__(
        self,
        seed: int = 42,
    ) -> None:
        self.random = random.Random(seed)
        self.event_generator = EventGeneratorService()
        self.feature_engineering = FeatureEngineeringService()

    def generate_company_state(self) -> CompanyState:
        return CompanyState(
            revenue=self.random.uniform(80_000, 150_000),
            profit=self.random.uniform(10_000, 35_000),
            cash=self.random.uniform(30_000, 100_000),
            inventory=self.random.uniform(5_000, 20_000),
            employees=self.random.randint(50, 200),
            market_share=self.random.uniform(0.08, 0.25),
        )

    def generate_market_state(self) -> MarketState:
        return MarketState(
            demand_index=self.random.uniform(0.70, 1.30),
            inflation_rate=self.random.uniform(0.02, 0.10),
            interest_rate=self.random.uniform(0.03, 0.10),
            competitor_pressure=self.random.uniform(0.20, 0.90),
            seasonality_index=self.random.uniform(0.80, 1.20),
        )

    def generate_sample_inputs(
        self,
    ) -> tuple[CompanyState, MarketState, list[SimulationEvent]]:
        company_state = self.generate_company_state()
        market_state = self.generate_market_state()

        events = self.event_generator.generate_events(
            company_state=company_state,
            market_state=market_state,
        )

        return company_state, market_state, events

    def generate_future_state(
        self,
        company_state: CompanyState,
        market_state: MarketState,
        events: list[SimulationEvent],
    ) -> ForecastPoint:
        demand_effect = market_state.demand_index
        seasonality_effect = market_state.seasonality_index

        competition_effect = 1.0 - (
            0.20 * market_state.competitor_pressure
        )

        inflation_cost = (
            company_state.revenue * market_state.inflation_rate * 0.25
        )

        interest_cost = (
            company_state.cash * market_state.interest_rate * 0.05
        )

        event_penalty = sum(
            event.severity for event in events
        ) * 0.02

        revenue_growth = (
            0.10 * (demand_effect - 1.0)
            + 0.05 * (seasonality_effect - 1.0)
            - event_penalty
        )

        future_revenue = (
            company_state.revenue
            * (1.0 + revenue_growth)
            * competition_effect
        )

        future_profit = (
            company_state.profit
            + (future_revenue - company_state.revenue) * 0.20
            - inflation_cost
            - interest_cost
        )

        future_cash = (
            company_state.cash
            + future_profit
        )

        inventory_consumption = (
            future_revenue * 0.02
        )

        future_inventory = max(
            0.0,
            company_state.inventory - inventory_consumption,
        )

        market_share_change = (
            0.02 * (demand_effect - 1.0)
            - 0.03 * market_state.competitor_pressure
        )

        future_market_share = min(
            1.0,
            max(
                0.0,
                company_state.market_share + market_share_change,
            ),
        )

        noise = self.random.uniform(-0.01, 0.01)

        future_revenue *= 1.0 + noise
        future_profit *= 1.0 + noise

        return ForecastPoint(
            horizon=1,
            revenue=future_revenue,
            profit=future_profit,
            cash=future_cash,
            inventory=future_inventory,
            market_share=future_market_share,
        )

    def generate_sample(self) -> ForecastTrainingSample:
        company_state, market_state, events = (
            self.generate_sample_inputs()
        )

        features = self.feature_engineering.build_features(
            company_state=company_state,
            market_state=market_state,
            events=events,
        )

        target = self.generate_future_state(
            company_state=company_state,
            market_state=market_state,
            events=events,
        )

        return ForecastTrainingSample(
            features=features,
            target=target,
        )

    def generate_dataset(
        self,
        num_samples: int,
    ) -> list[ForecastTrainingSample]:
        if num_samples <= 0:
            raise ValueError("num_samples must be greater than zero")
    
        return [
            self.generate_sample()
            for _ in range(num_samples)
        ]