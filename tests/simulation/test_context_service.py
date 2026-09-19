from datetime import UTC, datetime

import pytest

from abss.core.models import MarketState, SimulationEvent
from abss.db.models.company import Company
from abss.db.models.company_state import CompanyState
from abss.db.models.simulation_cycle import SimulationCycle
from abss.simulation.context_service import SimulationContextService


def test_build_context() -> None:
    company = Company(
        id=1,
        name="Context Test Company",
        industry="Technology",
    )
    
    cycle = SimulationCycle(
        id=1,
        company_id=1,
        company=company,
    )

    state = CompanyState(
        company=company,
        cycle=cycle,
        revenue=1_000_000,
        profit=100_000,
        cash=250_000,
        inventory=50_000,
        employees=100,
        market_share=0.10,
        created_at=datetime.now(UTC),
    )

    class FakeCycleRepository:
        def get_by_id(self, cycle_id: int) -> SimulationCycle | None:
            return cycle if cycle_id == 1 else None

    class FakeStateRepository:
        def get_latest(self, company_id: int) -> CompanyState | None:
            return state if company_id == company.id else None

    service = SimulationContextService(
        simulation_cycle_repository=FakeCycleRepository(),
        company_state_repository=FakeStateRepository(),
    )

    market_state = MarketState(
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
    )

    events = [
        SimulationEvent(
            event_id="event-001",
            event_type="supplier_disruption",
            severity=0.7,
            description="Major supplier disruption",
        ),
    ]

    context = service.build_context(
        cycle_id=1,
        market_state=market_state,
        events=events,
    )

    assert context.cycle_id == cycle.id
    assert context.company_id == company.id
    assert context.company_state.revenue == 1_000_000
    assert context.company_state.profit == 100_000
    assert context.company_state.market_share == 0.10
    assert context.market_state.demand_index == 1.0
    assert len(context.events) == 1
    assert context.events[0].event_type == "supplier_disruption"


def test_build_context_raises_for_missing_cycle() -> None:
    class FakeCycleRepository:
        def get_by_id(self, cycle_id: int) -> None:
            return None

    class FakeStateRepository:
        def get_latest(self, company_id: int) -> None:
            return None

    service = SimulationContextService(
        simulation_cycle_repository=FakeCycleRepository(),
        company_state_repository=FakeStateRepository(),
    )

    market_state = MarketState(
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
    )

    with pytest.raises(ValueError, match="Simulation cycle 999 not found"):
        service.build_context(
            cycle_id=999,
            market_state=market_state,
            events=[],
        )


def test_build_context_raises_for_missing_company_state() -> None:
    company = Company(
        name="Missing State Company",
        industry="Technology",
    )

    cycle = SimulationCycle(
        id=1,
        company=company,
    )

    class FakeCycleRepository:
        def get_by_id(self, cycle_id: int) -> SimulationCycle | None:
            return cycle

    class FakeStateRepository:
        def get_latest(self, company_id: int) -> None:
            return None

    service = SimulationContextService(
        simulation_cycle_repository=FakeCycleRepository(),
        company_state_repository=FakeStateRepository(),
    )

    market_state = MarketState(
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
    )

    with pytest.raises(
        ValueError,
        match="No company state found for company",
    ):
        service.build_context(
            cycle_id=1,
            market_state=market_state,
            events=[],
        )