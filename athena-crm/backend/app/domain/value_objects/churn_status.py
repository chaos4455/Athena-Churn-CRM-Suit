from enum import Enum


class ChurnStatus(str, Enum):
    DETECTED = "detected"       # Cliente detectado em risco
    IN_NEGOTIATION = "in_negotiation"
    CONVERTED = "converted"     # Churn revertido
    DECLINED = "declined"       # Perdido
    PENDING = "pending"         # Aguardando ação
