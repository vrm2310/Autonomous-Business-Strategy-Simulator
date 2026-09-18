from sqlalchemy.orm import Session

from abss.db.models.simulation_cycle import SimulationCycleStatus
from abss.db.repositories.company import CompanyRepository
from abss.db.repositories.simulation_cycle import SimulationCycleRepository


def test_create_get_and_update_simulation_cycle(
    db_session: Session,
) -> None:
    company_repository = CompanyRepository(db_session)
    cycle_repository = SimulationCycleRepository(db_session)

    company = company_repository.create(
        name="Cycle Test Company",
        industry="Technology",
    )

    cycle = cycle_repository.create(company.id)

    assert cycle.id is not None
    assert cycle.company_id == company.id
    assert cycle.status == SimulationCycleStatus.CREATED
    assert cycle.started_at is not None
    assert cycle.completed_at is None

    fetched_cycle = cycle_repository.get_by_id(cycle.id)

    assert fetched_cycle is not None
    assert fetched_cycle.id == cycle.id

    updated_cycle = cycle_repository.update_status(
        cycle.id,
        SimulationCycleStatus.COMPLETED,
    )

    assert updated_cycle is not None
    assert updated_cycle.status == SimulationCycleStatus.COMPLETED
    assert updated_cycle.completed_at is not None