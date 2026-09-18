from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from abss.db.models.simulation_cycle import (
    SimulationCycle,
    SimulationCycleStatus,
)


class SimulationCycleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        company_id: int,
    ) -> SimulationCycle:
        cycle = SimulationCycle(
            company_id=company_id,
            status=SimulationCycleStatus.CREATED,
            started_at=datetime.now(UTC),
        )

        self.db.add(cycle)
        self.db.flush()

        return cycle

    def get_by_id(
        self,
        cycle_id: int,
    ) -> SimulationCycle | None:
        statement = select(SimulationCycle).where(
            SimulationCycle.id == cycle_id,
        )

        return self.db.scalar(statement)

    def update_status(
        self,
        cycle_id: int,
        status: SimulationCycleStatus,
    ) -> SimulationCycle | None:
        cycle = self.get_by_id(cycle_id)

        if cycle is None:
            return None

        cycle.status = status

        if status in {
            SimulationCycleStatus.COMPLETED,
            SimulationCycleStatus.FAILED,
        }:
            cycle.completed_at = datetime.now(UTC)

        self.db.flush()

        return cycle