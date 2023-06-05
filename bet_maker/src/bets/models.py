import datetime
import uuid

import sqlalchemy as sa
from db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .schemas import EventState


class Bet(Base):
    __tablename__ = 'bet'
    __mapper_args__ = {"eager_defaults": True}

    bet_id = sa.Column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
        )
    event_id = sa.Column(sa.ForeignKey('event.event_id'))
    event = relationship('Event', lazy='joined', backref='bets')
    bet_coefficient = sa.Column(sa.Numeric(precision=10, scale=2), nullable=False)
    price = sa.Column(sa.Numeric(precision=10, scale=2), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now)

    def __repr__(self):
        return f'<Bet {self.bet_id}>'


class Event(Base):
    __tablename__ = 'event'
    event_id = sa.Column(sa.Integer, primary_key=True)
    coefficient = sa.Column(sa.DECIMAL)
    deadline = sa.Column(sa.BIGINT)
    state = sa.Column(sa.Enum(EventState), default=EventState.NEW)

    def __repr__(self):
        return f"<Event id={self.id} coef={self.coefficient}>"
