from sqlalchemy.orm import Session

from abss.db.models.simulation_cycle import SimulationCycleStatus
from abss.db.repositories.company import CompanyRepository
from abss.db.repositories.simulation_cycle import SimulationCycleRepository
from abss.simulation.service import SimulationCycleService


def test_create_cycle(db_session: Session) -> None:
    company_repository = CompanyRepository(db_session)
    company = company_repository.create(
        name="Acme Corporation",
        industry="Retail",
    )

    repository = SimulationCycleRepository(db_session)
    service = SimulationCycleService(repository)

    cycle = service.create_cycle(company.id)

    assert cycle.id is not None
    assert cycle.company_id == company.id
    assert cycle.status == SimulationCycleStatus.CREATED
    assert cycle.started_at is not None


def test_get_cycle(db_session: Session) -> None:
    company_repository = CompanyRepository(db_session)
    company = company_repository.create(
        name="Acme Corporation",
        industry="Retail",
    )

    repository = SimulationCycleRepository(db_session)
    service = SimulationCycleService(repository)

    created_cycle = service.create_cycle(company.id)

    cycle = service.get_cycle(created_cycle.id)

    assert cycle is not None
    assert cycle.id == created_cycle.id
    assert cycle.company_id == company.id


def test_update_cycle_status(db_session: Session) -> None:
    company_repository = CompanyRepository(db_session)
    company = company_repository.create(
        name="Acme Corporation",
        industry="Retail",
    )

    repository = SimulationCycleRepository(db_session)
    service = SimulationCycleService(repository)

    cycle = service.create_cycle(company.id)

    updated_cycle = service.update_status(
        cycle.id,
        SimulationCycleStatus.RUNNING,
    )

    assert updated_cycle is not None
    assert updated_cycle.status == SimulationCycleStatus.RUNNING
    assert updated_cycle.completed_at is None


def test_complete_cycle_sets_completed_at(
    db_session: Session,
) -> None:
    company_repository = CompanyRepository(db_session)
    company = company_repository.create(
        name="Acme Corporation",
        industry="Retail",
    )

    repository = SimulationCycleRepository(db_session)
    service = SimulationCycleService(repository)

    cycle = service.create_cycle(company.id)

    completed_cycle = service.update_status(
        cycle.id,
        SimulationCycleStatus.COMPLETED,
    )

    assert completed_cycle is not None
    assert completed_cycle.status == SimulationCycleStatus.COMPLETED
    assert completed_cycle.completed_at is not None