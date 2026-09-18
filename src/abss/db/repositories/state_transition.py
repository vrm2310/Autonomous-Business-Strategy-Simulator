from collections.abc import Mapping
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from abss.db.models.state_transition import StateTransition


class StateTransitionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
    self,
    company_id: int,
    cycle_id: int,
    previous_state_id: int,
    resulting_state_id: int,
    strategy: Mapping[str, object],
    ) -> StateTransition:
        transition = StateTransition(
            company_id=company_id,
            cycle_id=cycle_id,
            previous_state_id=previous_state_id,
            resulting_state_id=resulting_state_id,
            strategy=dict(strategy),
            created_at=datetime.now(UTC),
        )

        self.db.add(transition)
        self.db.flush()

        return transition

    def get_by_cycle(
        self,
        cycle_id: int,
    ) -> list[StateTransition]:
        statement = (
            select(StateTransition)
            .where(StateTransition.cycle_id == cycle_id)
            .order_by(StateTransition.created_at.asc())
        )

        return list(self.db.scalars(statement).all())