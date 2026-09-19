from fastapi import APIRouter, Depends, HTTPException

from abss.api.dependencies import (
    get_simulation_cycle_repository,
    get_unit_of_work,
)
from abss.api.schemas.simulation import (
    SimulationCycleCreate,
    SimulationCycleResponse,
    SimulationCycleStatusUpdate,
)
from abss.db.repositories.simulation_cycle import SimulationCycleRepository
from abss.db.unit_of_work import UnitOfWork
from abss.simulation.service import SimulationCycleService

router = APIRouter(prefix="/simulations", tags=["simulations"])


@router.post(
    "/cycles",
    response_model=SimulationCycleResponse,
    status_code=201,
)
def create_cycle(
    payload: SimulationCycleCreate,
    repository: SimulationCycleRepository = Depends(
        get_simulation_cycle_repository,
    ),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> SimulationCycleResponse:
    service = SimulationCycleService(repository)

    cycle = service.create_cycle(payload.company_id)

    unit_of_work.commit()

    return SimulationCycleResponse.model_validate(cycle)


@router.get(
    "/cycles/{cycle_id}",
    response_model=SimulationCycleResponse,
)
def get_cycle(
    cycle_id: int,
    repository: SimulationCycleRepository = Depends(
        get_simulation_cycle_repository,
    ),
) -> SimulationCycleResponse:
    service = SimulationCycleService(repository)

    cycle = service.get_cycle(cycle_id)

    if cycle is None:
        raise HTTPException(
            status_code=404,
            detail="Simulation cycle not found",
        )

    return SimulationCycleResponse.model_validate(cycle)


@router.patch(
    "/cycles/{cycle_id}/status",
    response_model=SimulationCycleResponse,
)
def update_cycle_status(
    cycle_id: int,
    payload: SimulationCycleStatusUpdate,
    repository: SimulationCycleRepository = Depends(
        get_simulation_cycle_repository,
    ),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> SimulationCycleResponse:
    service = SimulationCycleService(repository)

    cycle = service.update_status(
        cycle_id=cycle_id,
        status=payload.status,
    )

    if cycle is None:
        raise HTTPException(
            status_code=404,
            detail="Simulation cycle not found",
        )

    unit_of_work.commit()

    return SimulationCycleResponse.model_validate(cycle)