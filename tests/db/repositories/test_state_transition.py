from sqlalchemy.orm import Session

from abss.db.repositories.company import CompanyRepository
from abss.db.repositories.company_state import CompanyStateRepository
from abss.db.repositories.simulation_cycle import SimulationCycleRepository
from abss.db.repositories.state_transition import StateTransitionRepository


def test_create_and_get_state_transition(
    db_session: Session,
) -> None:
    company_repository = CompanyRepository(db_session)
    cycle_repository = SimulationCycleRepository(db_session)
    state_repository = CompanyStateRepository(db_session)
    transition_repository = StateTransitionRepository(db_session)

    company = company_repository.create(
        name="Transition Test Company",
        industry="Manufacturing",
    )

    cycle = cycle_repository.create(company.id)

    previous_state = state_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        revenue=1_000_000.0,
        profit=100_000.0,
        cash=250_000.0,
        inventory=100_000.0,
        employees=200,
        market_share=0.10,
    )

    resulting_state = state_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        revenue=1_100_000.0,
        profit=120_000.0,
        cash=280_000.0,
        inventory=90_000.0,
        employees=205,
        market_share=0.11,
    )

    strategy = {
        "pricing_change": 0.05,
        "marketing_budget_change": 0.10,
        "inventory_target": 85000,
    }

    transition = transition_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        previous_state_id=previous_state.id,
        resulting_state_id=resulting_state.id,
        strategy=strategy,
    )

    assert transition.id is not None
    assert transition.company_id == company.id
    assert transition.cycle_id == cycle.id
    assert transition.previous_state_id == previous_state.id
    assert transition.resulting_state_id == resulting_state.id
    assert transition.strategy == strategy
    assert transition.created_at is not None

    transitions = transition_repository.get_by_cycle(cycle.id)

    assert len(transitions) == 1
    assert transitions[0].id == transition.id