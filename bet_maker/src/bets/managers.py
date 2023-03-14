import sqlalchemy as sa

from db import get_session

from .models import Bet
from .schemas import BetCreateSchema, BetSchema


class BetManager:
    model = Bet

    @classmethod
    async def create_bet(cls, data: BetCreateSchema) -> BetSchema:
        async for session in get_session():
            bet = cls.model(**data.dict())
            session.add(bet)
            await session.commit()
            return BetSchema.from_orm(bet)

    @classmethod
    async def get_bets(cls) -> list[BetSchema]:
        async for session in get_session():
            query = sa.select(cls.model)
            fetched_bets = (await session.execute(query)).scalars()
            bets = [BetSchema.from_orm(bet) for bet in fetched_bets]
            return bets

