from fastapi import FastAPI

from src.routes import event_router

app = FastAPI()
app.include_router(event_router)
