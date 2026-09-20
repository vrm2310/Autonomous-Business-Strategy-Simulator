import pytest
from pydantic import ValidationError

from abss.core.models import CompanyState, MarketState, SimulationEvent
from abss.governance.scope_service import ScopeService


def test_build_scope_from_simulation_inputs() -> None:
    service = ScopeService()

    company_state = CompanyState(
        cash=100_000,
        inventory=5_000,
        employees=100,
    )
    market_state = MarketState(
        demand_index=1.1,
        inflation_rate=0.06,
        interest_rate=0.07,
        competitor_pressure=0.50,
        seasonality_index=1.0,
    )
    events = [
        SimulationEvent(
            event_id="high_inflation",
            event_type="HIGH_INFLATION",
            severity=0.8,
            description="Inflation is elevated.",
        ),
    ]

    scope = service.build_scope(
        cycle_id="cycle-1",
        company_state=company_state,
        market_state=market_state,
        events=events,
    )

    assert scope.cycle_id == "cycle-1"
    assert "Maintain financial stability" in scope.objectives
    assert scope.available_resources["cash"] == 100_000
    assert scope.available_resources["inventory"] == 5_000
    assert scope.available_resources["employees"] == 100.0
    assert scope.assumptions["demand_index"] == 1.1
    assert scope.assumptions["inflation_rate"] == 0.06
    assert scope.assumptions["active_events"] == ["HIGH_INFLATION"]


def test_scope_contains_company_constraints() -> None:
    service = ScopeService()

    company_state = CompanyState(
        cash=0,
        inventory=0,
        employees=50,
    )
    market_state = MarketState()

    scope = service.build_scope(
        cycle_id="cycle-2",
        company_state=company_state,
        market_state=market_state,
        events=[],
    )

    assert scope.hard_constraints["cash_constraint"] is True
    assert scope.hard_constraints["inventory_constraint"] is True


def test_scope_contains_market_constraints() -> None:
    service = ScopeService()

    company_state = CompanyState(
        cash=100_000,
        inventory=5_000,
        employees=100,
    )
    market_state = MarketState(
        competitor_pressure=0.80,
    )

    scope = service.build_scope(
        cycle_id="cycle-3",
        company_state=company_state,
        market_state=market_state,
        events=[],
    )

    assert scope.hard_constraints["high_competition"] is True


def test_scope_contains_allowed_decision_space() -> None:
    service = ScopeService()

    scope = service.build_scope(
        cycle_id="cycle-4",
        company_state=CompanyState(cash=100_000),
        market_state=MarketState(),
        events=[],
    )

    assert "pricing" in scope.allowed_decision_space
    assert "marketing" in scope.allowed_decision_space
    assert "inventory" in scope.allowed_decision_space
    assert "hiring" in scope.allowed_decision_space
    assert "cost_management" in scope.allowed_decision_space
    assert "capital_allocation" in scope.allowed_decision_space

def test_scope_is_immutable() -> None:
    service = ScopeService()

    scope = service.build_scope(
        cycle_id="cycle-5",
        company_state=CompanyState(cash=100_000),
        market_state=MarketState(),
        events=[],
    )

    with pytest.raises(ValidationError):
        scope.cycle_id = "modified-cycle"