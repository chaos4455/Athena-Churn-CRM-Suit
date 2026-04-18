from enum import Enum


class CardStage(str, Enum):
    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    IN_NEGOTIATION = "in_negotiation"
    CONVERTED = "converted"
    DECLINED = "declined"
