import decimal
import uuid
from enum import Enum

from pydantic import BaseModel, Field


class EventState(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    WIN = "WIN"
    LOST = "LOST"


class CreateEventSchema(BaseModel):
    coefficient: decimal.Decimal = Field(ge=0.00, decimal_places=2)
    deadline: int = Field(gt=1000000000)
    state: EventState | None = EventState.NEW


class EventSchema(CreateEventSchema):
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
