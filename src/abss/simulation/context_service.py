from typing import Protocol

from abss.core.models import (
    CompanyState as CoreCompanyState,
)
from abss.core.models import (
    MarketState,
    SimulationContext,
    SimulationEvent,
)
from abss.db.models.company_state import CompanyState as DbCompanyState
from abss.db.models.simulation_cycle import SimulationCycle


class SimulationCycleReader(Protocol):
    def get_by_id(self, cycle_id: int) -> SimulationCycle | None:
        ...


class CompanyStateReader(Protocol):
    def get_latest(self, company_id: int) -> DbCompanyState | None:
        ...


class SimulationContextService:
    def __init__(
    self,
    simulation_cycle_repository: SimulationCycleReader,
    company_state_repository: CompanyStateReader,
    ) -> None:
        self.simulation_cycle_repository = simulation_cycle_repository
        self.company_state_repository = company_state_repository

    @staticmethod
    def _to_domain_company_state(
        state: DbCompanyState,
    ) -> CoreCompanyState:
        return CoreCompanyState(
            revenue=float(state.revenue),
            profit=float(state.profit),
            cash=float(state.cash),
            inventory=float(state.inventory),
            employees=state.employees,
            market_share=float(state.market_share),
        )

    def build_context(
        self,
        cycle_id: int,
        market_state: MarketState,
        events: list[SimulationEvent],
    ) -> SimulationContext:
        cycle = self.simulation_cycle_repository.get_by_id(cycle_id)

        if cycle is None:
            raise ValueError(f"Simulation cycle {cycle_id} not found")

        company_state = self.company_state_repository.get_latest(
            cycle.company_id,
        )

        if company_state is None:
            raise ValueError(
                f"No company state found for company {cycle.company_id}",
            )

        return SimulationContext(
            cycle_id=cycle.id,
            company_id=cycle.company_id,
            company_state=self._to_domain_company_state(company_state),
            market_state=market_state,
            events=events,
        )