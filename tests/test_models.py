from abss.core.models import CompanyState, MarketState, Scope, SimulationCycle


def test_scope_is_separate_from_agent_memory() -> None:
    cycle = SimulationCycle(
        cycle_id="cycle-001",
        company_state=CompanyState(),
        market_state=MarketState(),
    )

    cycle.scope = Scope(
        cycle_id="cycle-001",
        objectives=["Maximise profitable growth"],
        hard_constraints={"max_marketing_spend": 100000},
    )

    assert cycle.scope is not None
    assert cycle.scope.cycle_id == cycle.cycle_id
