import time
from decimal import Decimal

import sqlalchemy as sa
from db import Session

from . import schemas
from .exceptions import EventNotFoundError
from .models import Bet, Event


class BetManager:
    """
    Contains main operations with Bet model in database
    """
    model = Bet

    @classmethod
    async def _create_bet(
        cls, data: schemas.BetCreateSchema, coefficient: Decimal
    ) -> schemas.BetSchema:
        async with Session() as session:
            bet = cls.model(**data.dict(), bet_coefficient=coefficient)
            session.add(bet)
            await session.commit()
            return schemas.BetSchema.from_orm(bet)

    @classmethod
    async def get_bets(cls) -> list[schemas.BetDetailedSchema]:
        async with Session() as session:
            query = sa.select(
                cls.model.event_id,
                cls.model.price,
                cls.model.bet_id,
                cls.model.created_at,
                Event.state
                ).join(Event, cls.model.event_id == Event.event_id)
            fetched_bets = (await session.execute(query)).fetchall()
            bets = [schemas.BetDetailedSchema.from_orm(bet) for bet in fetched_bets]
            return bets

    @classmethod
    async def place_bet(cls, data: schemas.BetCreateSchema) -> schemas.BetSchema:
        event = await EventManager.get_event_by_id(data.event_id)
        bet = await cls._create_bet(data, event.coefficient)
        return bet


class EventManager:
    """
    Contains main operations with Event model in database
    """
    model = Event

    @classmethod
    async def create_event(cls, data: schemas.EventSchema) -> schemas.EventSchema:
        async with Session() as session:
            event = cls.model(**data.dict())
            session.add(event)
            await session.commit()
            return data

    @classmethod
    async def get_event_by_id(
        cls, event_id: int
    ) -> schemas.EventSchema | None:
        async with Session() as session:
            event = await session.get(cls.model, event_id)
            if event is None:
                raise EventNotFoundError('Event with such id does not exist')
            return event

    @classmethod
    async def get_events(cls) -> list[schemas.EventSchema]:
        async with Session() as session:
            current_timestamp = int(time.time())
            query = sa.select(cls.model).where(cls.model.deadline > current_timestamp)
            fetched_events = await session.scalars(query)
            events = [schemas.EventSchema.from_orm(event) for event in fetched_events]
            return events

    @classmethod
    async def update_event_data(cls, data: schemas.EventSchema) -> None:
        async with Session() as session:
            query = sa.update(cls.model)\
                .where(cls.model.event_id == data.event_id)\
                .values(**data.dict(exclude={'event_id'}))
            await session.execute(query)
            await session.commit()
