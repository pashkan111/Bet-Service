import enum


class EventState(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    WIN = "WIN"
    LOST = "LOST"