from abss.db.models.company import Company
from abss.db.repositories.company import CompanyRepository


class CompanyService:
    def __init__(
        self,
        company_repository: CompanyRepository,
    ) -> None:
        self.company_repository = company_repository

    def create_company(
        self,
        name: str,
        industry: str,
    ) -> Company:
        return self.company_repository.create(
            name=name,
            industry=industry,
        )

    def get_company(
        self,
        company_id: int,
    ) -> Company | None:
        return self.company_repository.get_by_id(company_id)