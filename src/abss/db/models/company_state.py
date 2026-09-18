from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from abss.db.base import Base


class CompanyState(Base):
    __tablename__ = "company_states"

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    cycle_id: Mapped[int] = mapped_column(
        ForeignKey("simulation_cycles.id"),
        nullable=False,
    )

    revenue: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    profit: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    cash: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    inventory: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    employees: Mapped[int] = mapped_column(
        nullable=False,
    )

    market_share: Mapped[float] = mapped_column(
        Numeric(5, 4),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    company = relationship("Company")
    cycle = relationship("SimulationCycle")