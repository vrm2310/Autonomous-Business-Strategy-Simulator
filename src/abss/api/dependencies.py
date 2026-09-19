from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from abss.db.repositories.company import CompanyRepository
from abss.db.repositories.simulation_cycle import SimulationCycleRepository
from abss.db.session import SessionLocal
from abss.db.unit_of_work import UnitOfWork


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_unit_of_work(
    db: Session = Depends(get_db),
) -> UnitOfWork:
    return UnitOfWork(db)


def get_company_repository(
    db: Session = Depends(get_db),
) -> CompanyRepository:
    return CompanyRepository(db)


def get_simulation_cycle_repository(
    db: Session = Depends(get_db),
) -> SimulationCycleRepository:
    return SimulationCycleRepository(db)