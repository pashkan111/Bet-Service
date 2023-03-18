import pydantic
from src.schemas import EventSchema


class BaseMessage(pydantic.BaseModel):
    """Base message for all messages sended throught rabbit"""
    message_id: int


class EventChangedMessage(BaseMessage):
    message_id: int | None = 1001
    data: EventSchema
