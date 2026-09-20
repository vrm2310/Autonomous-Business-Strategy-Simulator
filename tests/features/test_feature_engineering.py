import pytest

from abss.core.models import CompanyState, MarketState, SimulationEvent
from abss.features.service import FeatureEngineeringService


def test_build_features_without_events() -> None:
    service = FeatureEngineeringService()

    company_state = CompanyState(
        revenue=100_000,
        profit=20_000,
        cash=50_000,
        inventory=10_000,
        employees=100,
        market_share=0.15,
    )
    market_state = MarketState(
        demand_index=1.1,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
    )

    features = service.build_features(
        company_state,
        market_state,
        [],
    )

    assert features.revenue == 100_000
    assert features.profit == 20_000
    assert features.employees == 100.0
    assert features.market_share == 0.15

    assert features.demand_index == 1.1
    assert features.inflation_rate == 0.04
    assert features.competitor_pressure == 0.50

    assert features.event_count == 0.0
    assert features.total_event_severity == 0.0
    assert features.high_inflation_event == 0.0
    assert features.low_demand_event == 0.0


def test_build_features_with_events() -> None:
    service = FeatureEngineeringService()

    company_state = CompanyState(
        revenue=100_000,
        profit=20_000,
        cash=50_000,
        inventory=10_000,
        employees=100,
        market_share=0.15,
    )
    market_state = MarketState(
        demand_index=0.60,
        inflation_rate=0.08,
        competitor_pressure=0.80,
    )

    events = [
        SimulationEvent(
            event_id="high_inflation",
            event_type="HIGH_INFLATION",
            severity=0.8,
            description="Inflation is elevated.",
        ),
        SimulationEvent(
            event_id="high_competition",
            event_type="HIGH_COMPETITION",
            severity=0.8,
            description="Competitive pressure is elevated.",
        ),
        SimulationEvent(
            event_id="low_demand",
            event_type="LOW_DEMAND",
            severity=0.8,
            description="Demand is low.",
        ),
    ]

    features = service.build_features(
        company_state,
        market_state,
        events,
    )

    assert features.event_count == 3.0
    assert features.total_event_severity == pytest.approx(2.4)

    assert features.high_inflation_event == 1.0
    assert features.high_competition_event == 1.0
    assert features.low_demand_event == 1.0
    assert features.demand_surge_event == 0.0
    assert features.cash_constraint_event == 0.0


def test_cash_constraint_event_is_encoded() -> None:
    service = FeatureEngineeringService()

    event = SimulationEvent(
        event_id="cash_constraint",
        event_type="CASH_CONSTRAINT",
        severity=1.0,
        description="The company has no available cash.",
    )

    features = service.build_features(
        CompanyState(cash=0),
        MarketState(),
        [event],
    )

    assert features.cash_constraint_event == 1.0
    assert features.event_count == 1.0
    assert features.total_event_severity == 1.0