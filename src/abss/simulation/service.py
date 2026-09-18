from abss.db.models.simulation_cycle import (
    SimulationCycle,
    SimulationCycleStatus,
)
from abss.db.repositories.simulation_cycle import SimulationCycleRepository


class SimulationCycleService:
    def __init__(
        self,
        simulation_cycle_repository: SimulationCycleRepository,
    ) -> None:
        self.simulation_cycle_repository = simulation_cycle_repository

    def create_cycle(
        self,
        company_id: int,
    ) -> SimulationCycle:
        return self.simulation_cycle_repository.create(
            company_id=company_id,
        )

    def get_cycle(
        self,
        cycle_id: int,
    ) -> SimulationCycle | None:
        return self.simulation_cycle_repository.get_by_id(cycle_id)

    def update_status(
        self,
        cycle_id: int,
        status: SimulationCycleStatus,
    ) -> SimulationCycle | None:
        return self.simulation_cycle_repository.update_status(
            cycle_id=cycle_id,
            status=status,
        )