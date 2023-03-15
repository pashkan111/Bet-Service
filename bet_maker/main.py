from fastapi import FastAPI

from db import init_db
from src.bets.routes import bets_router
from src.bets.callbacks import callback_router

app = FastAPI(title='Bet Maker')


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(bets_router, tags=['Bets'])
app.include_router(callback_router, tags=['Callbacks'])
