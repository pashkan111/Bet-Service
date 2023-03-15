import decimal
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .constants import EventState


class BetCreateSchema(BaseModel):
    event_id: int
    event_state: EventState | None = EventState.NEW
    coefficient: decimal.Decimal
    price: decimal.Decimal


class BetSchema(BetCreateSchema):
    bet_id: UUID
    created_at: datetime | None = None

    class Config:
        orm_mode = True


class MakeBetSchema(BaseModel):
    """Schema for create bet through api"""
    event_id: int
    price: decimal.Decimal = Field(ge=1.00, decimal_places=2)
    
    
class CallbackUpdateStateSchema(BaseModel):
    event_id: int
    event_state: EventState = Field(alias='state')
