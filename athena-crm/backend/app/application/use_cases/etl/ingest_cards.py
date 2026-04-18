import uuid
from datetime import datetime
from app.domain.entities.card import Card
from app.domain.entities.history import History
from app.domain.repositories.card_repository import CardRepository
from app.domain.repositories.client_repository import ClientRepository
from app.domain.repositories.history_repository import HistoryRepository
from app.application.dtos.etl_dto import ETLCardRecord, ETLIngestResult


class IngestCardsUseCase:
    """
    ETL de cards — lógica de ciclo:
    1. Arquiva todos os cards ativos do ciclo anterior (não do cycle_id atual).
    2. Cria novos cards para o cycle_id informado.
    O histórico do cliente é preservado com registro de arquivamento.
    """

    def __init__(
        self,
        card_repo: CardRepository,
        client_repo: ClientRepository,
        history_repo: HistoryRepository,
    ):
        self._cards    = card_repo
        self._clients  = client_repo
        self._histories = history_repo

    def execute(self, records: list[ETLCardRecord]) -> ETLIngestResult:
        result = ETLIngestResult()

        # Determina o cycle_id do lote (usa o primeiro registro como referência)
        cycle_id = records[0].cycle_id if records else None

        # ── Arquiva cards ativos de ciclos anteriores ──────────────
        if cycle_id:
            archived = self._cards.archive_old_cycles(cycle_id)
            result.archived = archived
            # Registra no histórico de cada cliente afetado
            for card in self._cards.find_archived_in_cycle_transition(cycle_id):
                history = History(
                    id=str(uuid.uuid4()),
                    client_id=card.client_id,
                    card_id=card.id,
                    seller_id=card.seller_id,
                    content=f"Card arquivado ao final do ciclo {card.cycle_id}. Último estágio: {card.stage.value}.",
                    history_type="card_archived",
                    card_stage=card.stage.value,
                    cycle_id=card.cycle_id,
                )
                self._histories.save(history)

        # ── Cria novos cards ───────────────────────────────────────
        for rec in records:
            try:
                client = self._clients.find_by_external_id(rec.client_external_id)
                if not client:
                    result.errors.append(f"Client external_id={rec.client_external_id} not found")
                    continue

                card = Card(
                    id=str(uuid.uuid4()),
                    client_id=client.id,
                    client_name=client.name,
                    seller_id=rec.seller_id,
                    title=rec.title,
                    description=rec.description,
                    ltv=client.ltv,
                    avg_ticket=client.avg_ticket,
                    last_purchase_date=client.last_purchase_date,
                    value_at_risk=rec.value_at_risk,
                    branch=rec.branch or client.branch,
                    state=rec.state or client.state,
                    cycle_id=rec.cycle_id,
                )
                self._cards.save(card)

                # Registra criação no histórico do cliente
                history = History(
                    id=str(uuid.uuid4()),
                    client_id=client.id,
                    card_id=card.id,
                    seller_id=rec.seller_id,
                    content=f"Card criado no ciclo {rec.cycle_id or '—'}. Valor em risco: R$ {rec.value_at_risk:,.2f}.",
                    history_type="card_created",
                    card_stage="backlog",
                    cycle_id=rec.cycle_id,
                )
                self._histories.save(history)
                result.created += 1

            except Exception as e:
                result.errors.append(f"{rec.client_external_id}: {str(e)}")

        return result
