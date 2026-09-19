from fastapi import APIRouter, Depends, status

from abss.api.dependencies import get_company_repository, get_unit_of_work
from abss.api.schemas.company import CompanyCreate, CompanyResponse
from abss.company.service import CompanyService
from abss.db.repositories.company import CompanyRepository
from abss.db.unit_of_work import UnitOfWork

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    payload: CompanyCreate,
    repository: CompanyRepository = Depends(get_company_repository),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> CompanyResponse:
    service = CompanyService(repository)

    company = service.create_company(
        name=payload.name,
        industry=payload.industry,
    )

    unit_of_work.commit()

    return CompanyResponse.model_validate(company)


@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
)
def get_company(
    company_id: int,
    repository: CompanyRepository = Depends(get_company_repository),
) -> CompanyResponse:
    service = CompanyService(repository)

    company = service.get_company(company_id)

    if company is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return CompanyResponse.model_validate(company)