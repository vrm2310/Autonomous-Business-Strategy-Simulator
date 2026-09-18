from sqlalchemy.orm import Session

from abss.company.service import CompanyService
from abss.db.repositories.company import CompanyRepository


def test_create_company(db_session: Session) -> None:
    repository = CompanyRepository(db_session)
    service = CompanyService(repository)

    company = service.create_company(
        name="Acme Corporation",
        industry="Retail",
    )

    assert company.id is not None
    assert company.name == "Acme Corporation"
    assert company.industry == "Retail"


def test_get_company(db_session: Session) -> None:
    repository = CompanyRepository(db_session)
    service = CompanyService(repository)

    created_company = service.create_company(
        name="Acme Corporation",
        industry="Retail",
    )

    company = service.get_company(created_company.id)

    assert company is not None
    assert company.id == created_company.id
    assert company.name == "Acme Corporation"
    assert company.industry == "Retail"