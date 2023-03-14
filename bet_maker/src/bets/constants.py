import decimal
import enum

from pydantic import BaseModel


class EventState(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    WIN = "WIN"
    LOST = "LOST"


class EventSchema(BaseModel):
    event_id: int
    coefficient: decimal.Decimal
    deadline: int
    state: EventState


class EventsSchema(BaseModel):
    __root__: list[EventSchema]
