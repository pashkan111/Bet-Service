import pytest
from main import app
from fastapi.testclient import TestClient
from src.schemas import EventSchema
from unittest.mock import AsyncMock


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


@pytest.fixture
def events(monkeypatch):
    events_db = {
        1: EventSchema(coefficient=1.77, deadline=1696756453, event_id=1),
        2: EventSchema(coefficient=1.56, deadline=1696756483, event_id=2)
    }
    monkeypatch.setattr('src.routes.events', events_db)
    return events_db


@pytest.fixture
def mocked_send_callback(monkeypatch):
    mocked_func = AsyncMock()
    monkeypatch.setattr('src.services.send_callback', mocked_func)
    return mocked_func
