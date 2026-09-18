from sqlalchemy.orm import Session

from abss.db.repositories.company import CompanyRepository


def test_create_and_get_company(db_session: Session) -> None:
    repository = CompanyRepository(db_session)

    company = repository.create(
        name="Test Company",
        industry="Technology",
    )

    assert company.id is not None
    assert company.name == "Test Company"
    assert company.industry == "Technology"
    assert company.created_at is not None

    db_session.commit()

    fetched_company = repository.get_by_id(company.id)

    assert fetched_company is not None
    assert fetched_company.id == company.id
    assert fetched_company.name == "Test Company"
    assert fetched_company.industry == "Technology"