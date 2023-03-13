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
    coefficient: decimal.Decimal
    deadline: int
    state: EventState | None = EventState.NEW


class EventSchema(CreateEventSchema):
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)


e1 = CreateEventSchema(coefficient=1.22, deadline=12, state=EventState.NEW)
e2 = CreateEventSchema(coefficient=1.55, deadline=152, state=EventState.IN_PROGRESS)

e1 = e1.copy(update=dict(e2))
print(e1)