from sqlalchemy.orm import Session

from abss.db.repositories.company import CompanyRepository
from abss.db.repositories.company_state import CompanyStateRepository
from abss.db.repositories.simulation_cycle import SimulationCycleRepository
from abss.db.repositories.state_transition import StateTransitionRepository
from abss.state.transition_service import StateTransitionService


def test_record_transition(db_session: Session) -> None:
    company_repository = CompanyRepository(db_session)
    company = company_repository.create(
        name="Acme Corporation",
        industry="Retail",
    )

    cycle_repository = SimulationCycleRepository(db_session)
    cycle = cycle_repository.create(company.id)

    state_repository = CompanyStateRepository(db_session)

    previous_state = state_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        revenue=10_000_000,
        profit=1_000_000,
        cash=5_000_000,
        inventory=1000,
        employees=500,
        market_share=0.15,
    )

    resulting_state = state_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        revenue=12_000_000,
        profit=1_100_000,
        cash=5_500_000,
        inventory=900,
        employees=520,
        market_share=0.17,
    )

    repository = StateTransitionRepository(db_session)
    service = StateTransitionService(repository)

    transition = service.record_transition(
        company_id=company.id,
        cycle_id=cycle.id,
        previous_state_id=previous_state.id,
        resulting_state_id=resulting_state.id,
        strategy={
            "decision": "increase_marketing",
            "budget": 500_000,
        },
    )

    assert transition.id is not None
    assert transition.company_id == company.id
    assert transition.cycle_id == cycle.id
    assert transition.previous_state_id == previous_state.id
    assert transition.resulting_state_id == resulting_state.id
    assert transition.strategy["decision"] == "increase_marketing"
    assert transition.strategy["budget"] == 500_000


def test_get_cycle_transitions(db_session: Session) -> None:
    company_repository = CompanyRepository(db_session)
    company = company_repository.create(
        name="Acme Corporation",
        industry="Retail",
    )

    cycle_repository = SimulationCycleRepository(db_session)
    cycle = cycle_repository.create(company.id)

    state_repository = CompanyStateRepository(db_session)

    first_state = state_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        revenue=10_000_000,
        profit=1_000_000,
        cash=5_000_000,
        inventory=1000,
        employees=500,
        market_share=0.15,
    )

    second_state = state_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        revenue=11_000_000,
        profit=1_050_000,
        cash=5_200_000,
        inventory=950,
        employees=510,
        market_share=0.16,
    )

    third_state = state_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        revenue=12_000_000,
        profit=1_100_000,
        cash=5_500_000,
        inventory=900,
        employees=520,
        market_share=0.17,
    )

    repository = StateTransitionRepository(db_session)
    service = StateTransitionService(repository)

    service.record_transition(
        company_id=company.id,
        cycle_id=cycle.id,
        previous_state_id=first_state.id,
        resulting_state_id=second_state.id,
        strategy={"decision": "increase_marketing"},
    )

    service.record_transition(
        company_id=company.id,
        cycle_id=cycle.id,
        previous_state_id=second_state.id,
        resulting_state_id=third_state.id,
        strategy={"decision": "expand_capacity"},
    )

    transitions = service.get_cycle_transitions(cycle.id)

    assert len(transitions) == 2
    assert transitions[0].previous_state_id == first_state.id
    assert transitions[0].resulting_state_id == second_state.id
    assert transitions[1].previous_state_id == second_state.id
    assert transitions[1].resulting_state_id == third_state.id