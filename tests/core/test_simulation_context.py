from abss.core.models import (
    CompanyState,
    MarketState,
    SimulationContext,
    SimulationEvent,
)


def test_simulation_context_can_be_created() -> None:
    company_state = CompanyState(
        revenue=1_000_000,
        profit=100_000,
        cash=250_000,
        inventory=50_000,
        employees=100,
        market_share=0.10,
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

    context = SimulationContext(
        cycle_id=1,
        company_id=1,
        company_state=company_state,
        market_state=market_state,
        events=events,
    )

    assert context.cycle_id == 1
    assert context.company_id == 1
    assert context.company_state.revenue == 1_000_000
    assert context.market_state.demand_index == 1.0
    assert len(context.events) == 1