from typing import Optional
from app.domain.services.performance_service import PerformanceService


class GetPerformanceMetricsUseCase:

    def __init__(self, performance_service: PerformanceService):
        self._service = performance_service

    def execute(
        self,
        seller_id: str,
        branch:    Optional[str] = None,
        state:     Optional[str] = None,
        archived:  bool          = False,
    ) -> dict:
        return self._service.get_seller_performance(
            seller_id, branch=branch, state=state, archived=archived
        )
