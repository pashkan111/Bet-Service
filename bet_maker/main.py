from fastapi import FastAPI

from db import init_db
from src.bets.routes import router

app = FastAPI(title='Bet Maker')


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(router)