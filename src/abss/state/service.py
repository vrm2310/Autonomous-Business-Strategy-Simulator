from abss.db.models.company_state import CompanyState
from abss.db.repositories.company_state import CompanyStateRepository


class StateService:
    def __init__(
        self,
        company_state_repository: CompanyStateRepository,
    ) -> None:
        self.company_state_repository = company_state_repository

    def get_current_state(
        self,
        company_id: int,
    ) -> CompanyState | None:
        return self.company_state_repository.get_latest(company_id)