import uuid
from app.domain.entities.client import Client
from app.domain.repositories.client_repository import ClientRepository
from app.application.dtos.etl_dto import ETLClientRecord, ETLIngestResult


class IngestClientsUseCase:
    """Upsert de clientes via ETL. Preserva histórico."""

    def __init__(self, client_repo: ClientRepository):
        self._clients = client_repo

    def execute(self, records: list[ETLClientRecord]) -> ETLIngestResult:
        result = ETLIngestResult()
        for rec in records:
            try:
                existing = self._clients.find_by_external_id(rec.external_id)
                if existing:
                    existing.name               = rec.name
                    existing.ltv                = rec.ltv
                    existing.avg_ticket         = rec.avg_ticket
                    existing.last_purchase_date = rec.last_purchase_date
                    existing.seller_id          = rec.seller_id
                    existing.branch             = rec.branch
                    existing.state              = rec.state
                    existing.mark_at_risk(rec.churn_risk_score)
                    self._clients.save(existing)
                    result.updated += 1
                else:
                    client = Client(
                        id=str(uuid.uuid4()),
                        name=rec.name,
                        external_id=rec.external_id,
                        ltv=rec.ltv,
                        avg_ticket=rec.avg_ticket,
                        last_purchase_date=rec.last_purchase_date,
                        seller_id=rec.seller_id,
                        branch=rec.branch,
                        state=rec.state,
                    )
                    client.mark_at_risk(rec.churn_risk_score)
                    self._clients.save(client)
                    result.created += 1
            except Exception as e:
                result.errors.append(f"{rec.external_id}: {str(e)}")
        return result
