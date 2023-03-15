import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from db import Base

from .constants import EventState


class Bet(Base):
    __tablename__ = 'bet'
    __mapper_args__ = {"eager_defaults": True}

    bet_id = sa.Column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
        )
    event_id = sa.Column(sa.Integer, nullable=False)
    event_state = sa.Column(sa.Enum(EventState), default=EventState.NEW)
    coefficient = sa.Column(sa.Numeric(precision=10, scale=2), nullable=False)
    price = sa.Column(sa.Numeric(precision=10, scale=2), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now)

    def __repr__(self):
        return f'<Bet {self.bet_id}>'
