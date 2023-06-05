import decimal
import enum
from datetime import datetime
from uuid import UUID

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

    class Config:
        orm_mode = True


class EventsSchema(BaseModel):
    __root__: list[EventSchema]


class BetCreateSchema(BaseModel):
    event_id: int
    price: decimal.Decimal


class BetSchema(BetCreateSchema):
    bet_id: UUID
    created_at: datetime | None = None

    class Config:
        orm_mode = True


class BetDetailedSchema(BetSchema):
    bet_id: UUID
    created_at: datetime | None = None
    state: str

    class Config:
        orm_mode = True
