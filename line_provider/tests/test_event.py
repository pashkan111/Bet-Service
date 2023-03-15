from src.schemas import CreateEventSchema, EventState, UpdateEventSchema
import decimal


def test_create_event(test_client, events):
    data = CreateEventSchema(
        coefficient=decimal.Decimal('1.66'),
        deadline=167888837463,
        state=EventState.IN_PROGRESS
    ) 
    assert len(events) == 2
    response = test_client.post("/events", content=data.json())
    assert len(events) == 3
    assert response.status_code == 201
    

def test_create_event_bad_request(test_client, events):
    data = dict(
        coefficient=decimal.Decimal('0.88'),
        deadline=167888837463,
        state=EventState.IN_PROGRESS
    ) 
    response = test_client.post("/events", data=data)
    assert len(events) == 2
    assert response.status_code == 422


def test_get_events(test_client, events):
    response = test_client.get("/events")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    
def test_update_event_success(test_client, events, mocked_send_callback):
    event_id = 1
    update_coefficient = decimal.Decimal("4.33")
    update_data = UpdateEventSchema(coefficient=update_coefficient)
    
    response = test_client.patch(f"/events/{event_id}", content=update_data.json())
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['event_id'] == event_id
    assert response_data['coefficient'] == float(update_coefficient)
    
    assert mocked_send_callback.call_count == 1


def test_update_event_not_found(test_client, events, mocked_send_callback):
    event_id = 12
    update_coefficient = decimal.Decimal("8.1")
    update_data = UpdateEventSchema(coefficient=update_coefficient)
    
    response = test_client.patch(f"/events/{event_id}", content=update_data.json())
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == 'Event with this id has not been found'

