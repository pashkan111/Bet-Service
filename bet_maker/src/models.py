import datetime
import enum
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import Base


class EventState(str, enum.Enum):
    WIN = "WIN"
    LOST = "LOST"


class Bet(Base):
    __tablename__ = 'bet'
    bet_id = sa.Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True
        )
    event_id = sa.Column(UUID(as_uuid=True), index=True, nallable=False)
    event_state = sa.Column(sa.Enum(EventState))
    coefficient = sa.Column(sa.FLOAT, nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    created_at = sa.Column(
        sa.DateTime(timezone=True), default=datetime.datetime.now
        )
    user = relationship("User", back_populates="bets")

    def __repr__(self):
        return f'<Bet {self.bet_id}>'


class User(Base):
    __tablename__ = 'person'
    phone = sa.Column(sa.String(11), primary_key=True)
    password = sa.Column(sa.String, index=True)
    name = sa.Column(sa.String)
    bets = relationship("Bet", back_populates="user")
    
    def __repr__(self):
        return f'<User {self.phone}>'
