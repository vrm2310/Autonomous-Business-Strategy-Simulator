from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from abss.db.models.company_state import CompanyState


class CompanyStateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        company_id: int,
        cycle_id: int,
        revenue: float,
        profit: float,
        cash: float,
        inventory: float,
        employees: int,
        market_share: float,
    ) -> CompanyState:
        state = CompanyState(
            company_id=company_id,
            cycle_id=cycle_id,
            revenue=revenue,
            profit=profit,
            cash=cash,
            inventory=inventory,
            employees=employees,
            market_share=market_share,
            created_at=datetime.now(UTC),
        )

        self.db.add(state)
        self.db.flush()

        return state

    def get_by_id(
        self,
        state_id: int,
    ) -> CompanyState | None:
        statement = select(CompanyState).where(
            CompanyState.id == state_id,
        )

        return self.db.scalar(statement)

    def get_by_cycle(
        self,
        cycle_id: int,
    ) -> CompanyState | None:
        statement = (
            select(CompanyState)
            .where(CompanyState.cycle_id == cycle_id)
            .order_by(CompanyState.created_at.desc())
        )

        return self.db.scalars(statement).first()

    def get_latest(
        self,
        company_id: int,
    ) -> CompanyState | None:
        statement = (
            select(CompanyState)
            .where(CompanyState.company_id == company_id)
            .order_by(CompanyState.created_at.desc())
        )

        return self.db.scalars(statement).first()