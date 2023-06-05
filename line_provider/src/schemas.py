import decimal
from enum import Enum

from pydantic import BaseModel, Field


class EventState(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    WIN = "WIN"
    LOST = "LOST"


class CreateEventSchema(BaseModel):
    coefficient: decimal.Decimal = Field(ge=1.00, decimal_places=2)
    deadline: int = Field(gt=1000_000_000)
    state: EventState | None = EventState.NEW


class UpdateEventSchema(BaseModel):
    coefficient: decimal.Decimal | None = Field(ge=1.00, decimal_places=2, default=None)
    deadline: int | None = Field(gt=1000_000_000, default=None)
    state: EventState | None = None


class EventSchema(CreateEventSchema):
    event_id: int
