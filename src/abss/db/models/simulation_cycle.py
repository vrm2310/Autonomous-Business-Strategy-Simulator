from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from abss.db.base import Base


class SimulationCycleStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SimulationCycle(Base):
    __tablename__ = "simulation_cycles"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )
    status: Mapped[SimulationCycleStatus] = mapped_column(
        SQLEnum(SimulationCycleStatus),
        nullable=False,
        default=SimulationCycleStatus.CREATED,
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    company = relationship("Company", back_populates="simulation_cycles")