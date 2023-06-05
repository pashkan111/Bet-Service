import pydantic
from src.schemas import EventSchema


class BaseMessage(pydantic.BaseModel):
    """Base message for all messages sended throught rabbit"""
    message_id: int


class EventChangedMessage(BaseMessage):
    """Message for change event"""
    message_id: int | None = 1001
    data: EventSchema


class EventCreatedMessage(BaseMessage):
    """Message for create event"""
    message_id: int | None = 1002
    data: EventSchema
