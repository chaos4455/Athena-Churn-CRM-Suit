from typing import Optional
from app.domain.services.dashboard_service import DashboardService


class GetDashboardIndicatorsUseCase:

    def __init__(self, dashboard_service: DashboardService):
        self._service = dashboard_service

    def execute(
        self,
        branch:    Optional[str] = None,
        state:     Optional[str] = None,
        seller_id: Optional[str] = None,
    ) -> dict:
        return self._service.get_indicators(branch=branch, state=state, seller_id=seller_id)
