from collections.abc import Mapping

from abss.db.models.state_transition import StateTransition
from abss.db.repositories.state_transition import StateTransitionRepository


class StateTransitionService:
    def __init__(
        self,
        state_transition_repository: StateTransitionRepository,
    ) -> None:
        self.state_transition_repository = state_transition_repository

    def record_transition(
        self,
        company_id: int,
        cycle_id: int,
        previous_state_id: int,
        resulting_state_id: int,
        strategy: Mapping[str, object],
    ) -> StateTransition:
        return self.state_transition_repository.create(
            company_id=company_id,
            cycle_id=cycle_id,
            previous_state_id=previous_state_id,
            resulting_state_id=resulting_state_id,
            strategy=strategy,
        )

    def get_cycle_transitions(
        self,
        cycle_id: int,
    ) -> list[StateTransition]:
        return self.state_transition_repository.get_by_cycle(cycle_id)