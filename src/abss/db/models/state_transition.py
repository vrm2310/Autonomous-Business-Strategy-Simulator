from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from abss.db.base import Base


class StateTransition(Base):
    __tablename__ = "state_transitions"

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    cycle_id: Mapped[int] = mapped_column(
        ForeignKey("simulation_cycles.id"),
        nullable=False,
    )

    previous_state_id: Mapped[int] = mapped_column(
        ForeignKey("company_states.id"),
        nullable=False,
    )

    resulting_state_id: Mapped[int] = mapped_column(
        ForeignKey("company_states.id"),
        nullable=False,
    )

    strategy: Mapped[dict[str, object]] = mapped_column(
        JSON,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    company = relationship("Company")
    cycle = relationship("SimulationCycle")
    previous_state = relationship(
        "CompanyState",
        foreign_keys=[previous_state_id],
    )
    resulting_state = relationship(
        "CompanyState",
        foreign_keys=[resulting_state_id],
    )