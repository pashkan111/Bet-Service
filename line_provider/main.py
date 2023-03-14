from fastapi import FastAPI

from src.routes import event_router

app = FastAPI(title='Line Provider')

app.include_router(event_router)
