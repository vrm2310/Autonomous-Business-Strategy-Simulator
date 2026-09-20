import pytest

from abss.core.models import CompanyState, MarketState
from abss.events.service import EventGeneratorService


def test_no_events_under_normal_conditions() -> None:
    service = EventGeneratorService()

    company_state = CompanyState(cash=100_000)
    market_state = MarketState(
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
    )

    events = service.generate_events(company_state, market_state)

    assert events == []


def test_high_inflation_event() -> None:
    service = EventGeneratorService()

    company_state = CompanyState(cash=100_000)
    market_state = MarketState(inflation_rate=0.08)

    events = service.generate_events(company_state, market_state)

    assert len(events) == 1
    assert events[0].event_type == "HIGH_INFLATION"
    assert events[0].severity == pytest.approx(0.8)


def test_high_competition_event() -> None:
    service = EventGeneratorService()

    company_state = CompanyState(cash=100_000)
    market_state = MarketState(competitor_pressure=0.80)

    events = service.generate_events(company_state, market_state)

    assert len(events) == 1
    assert events[0].event_type == "HIGH_COMPETITION"
    assert events[0].severity == pytest.approx(0.8)


def test_low_demand_event() -> None:
    service = EventGeneratorService()

    company_state = CompanyState(cash=100_000)
    market_state = MarketState(demand_index=0.60)

    events = service.generate_events(company_state, market_state)

    assert len(events) == 1
    assert events[0].event_type == "LOW_DEMAND"
    assert events[0].severity == pytest.approx(0.8)


def test_demand_surge_event() -> None:
    service = EventGeneratorService()

    company_state = CompanyState(cash=100_000)
    market_state = MarketState(demand_index=1.40)

    events = service.generate_events(company_state, market_state)

    assert len(events) == 1
    assert events[0].event_type == "DEMAND_SURGE"
    assert events[0].severity == pytest.approx(0.8)


def test_cash_constraint_event() -> None:
    service = EventGeneratorService()

    company_state = CompanyState(cash=0)
    market_state = MarketState()

    events = service.generate_events(company_state, market_state)

    assert len(events) == 1
    assert events[0].event_type == "CASH_CONSTRAINT"
    assert events[0].severity == 1.0


def test_multiple_events_can_be_generated() -> None:
    service = EventGeneratorService()

    company_state = CompanyState(cash=0)
    market_state = MarketState(
        demand_index=0.60,
        inflation_rate=0.08,
        competitor_pressure=0.80,
    )

    events = service.generate_events(company_state, market_state)

    event_types = {event.event_type for event in events}

    assert event_types == {
        "HIGH_INFLATION",
        "HIGH_COMPETITION",
        "LOW_DEMAND",
        "CASH_CONSTRAINT",
    }