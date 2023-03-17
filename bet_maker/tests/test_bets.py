import pytest
from unittest.mock import AsyncMock
from src.bets.constants import EventSchema, EventState
from src.utils.exceptions import ClientError


@pytest.mark.asyncio
async def test_get_bets(async_client):
    response = await async_client.get("/bets/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_bet(async_client, test_data, monkeypatch):   
    mocked_func = AsyncMock()
    monkeypatch.setattr('src.bets.services.get_event', mocked_func)
    mocked_func.return_value = EventSchema(
        event_id=2, coefficient=1.88, deadline=1675647364, state=EventState.NEW
        )

    payload = test_data[1]
    response_created = await async_client.post("/bets/", json=payload)
    assert response_created.status_code == 201
    response_data = response_created.json()
    assert response_data['price'] == payload['price']
    assert response_data['bet_id'] is not None


@pytest.mark.asyncio
async def test_create_bet_with_unexisted_event(async_client, test_data, monkeypatch):
    
    mocked_func = AsyncMock()
    monkeypatch.setattr('src.bets.services.get_event', mocked_func)
    msg = 'Event does not exist'
    mocked_func.side_effect = ClientError(msg)
    
    payload = test_data[1]
    response_created = await async_client.post("/bets/", json=payload)
    assert response_created.status_code == 400
    response_data = response_created.json()
    assert response_data['detail'] == msg
