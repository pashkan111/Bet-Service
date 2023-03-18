import pydantic


class BaseMessage(pydantic.BaseModel):
    """Base message for all messages sended throught rabbit"""
    message_id: int
