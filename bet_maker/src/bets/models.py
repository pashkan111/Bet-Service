import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from db import Base

from .constants import EventState


class Bet(Base):
    __tablename__ = 'bet'
    bet_id = sa.Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True
        )
    event_id = sa.Column(sa.Integer, nullable=False)
    event_state = sa.Column(sa.Enum(EventState), default=EventState.IN_PROGRESS)
    coefficient = sa.Column(sa.FLOAT, nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    created_at = sa.Column(
        sa.DateTime(timezone=True), default=datetime.datetime.now
        )

    def __repr__(self):
        return f'<Bet {self.bet_id}>'
