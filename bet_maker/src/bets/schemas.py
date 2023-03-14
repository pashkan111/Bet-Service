from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .constants import EventState


class BetCreateSchema(BaseModel):
    bet_id: UUID
    event_id: int
    event_state: EventState | None = EventState.IN_PROGRESS
    coefficient: float
    price: float
    created_at: datetime | None


class BetSchema(BetCreateSchema):
    bet_id: UUID
    class Config:
        orm_mode = True