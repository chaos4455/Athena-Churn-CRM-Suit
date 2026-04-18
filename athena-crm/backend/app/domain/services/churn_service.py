from ..repositories.card_repository import CardRepository
from ..repositories.client_repository import ClientRepository
from ..value_objects.card_stage import CardStage


class ChurnService:
    """Domain service: regras de negócio de churn."""

    def __init__(
        self,
        card_repo: CardRepository,
        client_repo: ClientRepository,
    ):
        self._cards = card_repo
        self._clients = client_repo

    def get_total_value_at_risk(self) -> float:
        return self._cards.total_value_at_risk()

    def get_stage_summary(self) -> dict:
        return self._cards.count_by_stage()

    def get_conversion_rate(self) -> float:
        counts = self._cards.count_by_stage()
        total = sum(counts.values())
        if total == 0:
            return 0.0
        converted = counts.get(CardStage.CONVERTED, 0)
        return round((converted / total) * 100, 2)
