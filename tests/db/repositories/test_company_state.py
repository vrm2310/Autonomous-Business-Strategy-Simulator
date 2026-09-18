from sqlalchemy.orm import Session

from abss.db.repositories.company import CompanyRepository
from abss.db.repositories.company_state import CompanyStateRepository
from abss.db.repositories.simulation_cycle import SimulationCycleRepository


def test_create_and_retrieve_company_state(
    db_session: Session,
) -> None:
    company_repository = CompanyRepository(db_session)
    cycle_repository = SimulationCycleRepository(db_session)
    state_repository = CompanyStateRepository(db_session)

    company = company_repository.create(
        name="State Test Company",
        industry="Retail",
    )

    cycle = cycle_repository.create(company.id)

    state = state_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        revenue=1_000_000.0,
        profit=150_000.0,
        cash=300_000.0,
        inventory=100_000.0,
        employees=250,
        market_share=0.125,
    )

    assert state.id is not None
    assert state.company_id == company.id
    assert state.cycle_id == cycle.id
    assert state.revenue == 1_000_000.0
    assert state.profit == 150_000.0
    assert state.employees == 250
    assert state.market_share == 0.125
    assert state.created_at is not None

    fetched_state = state_repository.get_by_id(state.id)

    assert fetched_state is not None
    assert fetched_state.id == state.id


def test_get_latest_company_state(
    db_session: Session,
) -> None:
    company_repository = CompanyRepository(db_session)
    cycle_repository = SimulationCycleRepository(db_session)
    state_repository = CompanyStateRepository(db_session)

    company = company_repository.create(
        name="Latest State Company",
        industry="Technology",
    )

    first_cycle = cycle_repository.create(company.id)

    first_state = state_repository.create(
        company_id=company.id,
        cycle_id=first_cycle.id,
        revenue=1_000_000.0,
        profit=100_000.0,
        cash=250_000.0,
        inventory=90_000.0,
        employees=200,
        market_share=0.10,
    )

    second_cycle = cycle_repository.create(company.id)

    second_state = state_repository.create(
        company_id=company.id,
        cycle_id=second_cycle.id,
        revenue=1_200_000.0,
        profit=140_000.0,
        cash=320_000.0,
        inventory=80_000.0,
        employees=210,
        market_share=0.12,
    )

    latest_state = state_repository.get_latest(company.id)

    assert latest_state is not None
    assert latest_state.id == second_state.id
    assert latest_state.id != first_state.id