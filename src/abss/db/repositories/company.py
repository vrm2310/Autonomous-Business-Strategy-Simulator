from sqlalchemy import select
from sqlalchemy.orm import Session

from abss.db.models.company import Company


class CompanyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        name: str,
        industry: str,
    ) -> Company:
        company = Company(
            name=name,
            industry=industry,
        )

        self.db.add(company)
        self.db.flush()

        return company

    def get_by_id(
        self,
        company_id: int,
    ) -> Company | None:
        statement = select(Company).where(Company.id == company_id)

        return self.db.scalar(statement)