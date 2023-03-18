import sqlalchemy as sa
from db import Session

from .models import Bet
from .schemas import BetCreateSchema, BetSchema, CallbackUpdateStateSchema


class BetManager:
    """
    Contains main operations with Bet model in database
    """
    model = Bet

    @classmethod
    async def create_bet(cls, data: BetCreateSchema) -> BetSchema:
        async with Session() as session:
            bet = cls.model(**data.dict())
            session.add(bet)
            await session.commit()
            return BetSchema.from_orm(bet)

    @classmethod
    async def get_bets(cls) -> list[BetSchema]:
        async with Session() as session:
            query = sa.select(cls.model)
            fetched_bets = (await session.execute(query)).scalars()
            bets = [BetSchema.from_orm(bet) for bet in fetched_bets]
            return bets

    @classmethod
    async def update_bets_event_state(cls, data: CallbackUpdateStateSchema) -> None:
        async with Session() as session:
            query = sa.update(cls.model)\
                .where(cls.model.event_id==data.event_id)\
                .values(event_state=data.event_state)
            await session.execute(query)
            await session.commit()

