from sqlalchemy.orm import Session

from abss.db.repositories.company import CompanyRepository
from abss.db.repositories.company_state import CompanyStateRepository
from abss.db.repositories.simulation_cycle import SimulationCycleRepository
from abss.state.service import StateService


def test_get_current_state(
    db_session: Session,
) -> None:
    company_repository = CompanyRepository(db_session)
    cycle_repository = SimulationCycleRepository(db_session)
    state_repository = CompanyStateRepository(db_session)

    company = company_repository.create(
        name="State Service Test Company",
        industry="Technology",
    )

    cycle = cycle_repository.create(company.id)

    state_repository.create(
        company_id=company.id,
        cycle_id=cycle.id,
        revenue=2_000_000.0,
        profit=250_000.0,
        cash=500_000.0,
        inventory=150_000.0,
        employees=300,
        market_share=0.15,
    )

    state_service = StateService(state_repository)

    current_state = state_service.get_current_state(company.id)

    assert current_state is not None
    assert current_state.company_id == company.id
    assert current_state.cycle_id == cycle.id
    assert current_state.revenue == 2_000_000.0
    assert current_state.profit == 250_000.0
    assert float(current_state.market_share) == 0.15

def test_get_current_state_returns_none_when_no_state_exists(
    db_session: Session,
) -> None:
    company_repository = CompanyRepository(db_session)
    state_repository = CompanyStateRepository(db_session)

    company = company_repository.create(
        name="No State Company",
        industry="Finance",
    )

    state_service = StateService(state_repository)

    current_state = state_service.get_current_state(company.id)

    assert current_state is None