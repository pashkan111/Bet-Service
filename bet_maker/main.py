from db import init_db
from fastapi import FastAPI
from src.bets.message_handlers import message_handler
from src.bets.routes import bets_router

app = FastAPI(title='Bet Maker')


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(bets_router, tags=['Bets'])
