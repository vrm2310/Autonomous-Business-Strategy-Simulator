from datetime import datetime

from pydantic import BaseModel

from abss.db.models.simulation_cycle import SimulationCycleStatus


class SimulationCycleCreate(BaseModel):
    company_id: int


class SimulationCycleStatusUpdate(BaseModel):
    status: SimulationCycleStatus


class SimulationCycleResponse(BaseModel):
    id: int
    company_id: int
    status: SimulationCycleStatus
    started_at: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}