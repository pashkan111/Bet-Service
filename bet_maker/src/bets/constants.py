import enum


class EventState(str, enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    WIN = "WIN"
    LOST = "LOST"