from enum import Enum


class ActionType(str, Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    WHATSAPP = "whatsapp"
    NOTE = "note"
    PROPOSAL = "proposal"
