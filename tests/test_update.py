import pytest
from movieApi import create_app
from movieApi.extensions import db

@pytest.mark.parametrize(('ticket_id', 'timing', 'message'), (
    ('', '', b'Ticket ID to update not provided'),
    ('test', '', b'Invalid ticket ID'),
    ('5f4b5b9fc8a7b99dec070935', '', b'Updated time not provided'),
    ('5f4b5b9fc8a7b99dec070935', '2020-08-31T13:00', b"This ticket doesn't exists")
))
def test_updation_inputs(client, ticket_id, timing, message):
    res = client.put(
        '/api/v1/ticket',
        json={'ticket_id': ticket_id, 'timing': timing}
    )
    assert message in res.data

def test_updation(client):
    res = client.post(
        '/api/v1/ticket',
        json={'name': 'test', 'phone': '9123456789', 'timing': '2020-08-31T13:00'}
    )
    res = res.get_json()
    res = client.put(
        'api/v1/ticket',
        json={'ticket_id': res['ticket_id'], 'timing': '2020-08-31T19:00'}
    )
    db.movie_tickets.tickets.drop()
    assert b'Ticket timing updated' in res.data

def test_updation_limit(client):
    for i in range(21):
        res = client.post(
            '/api/v1/ticket',
            json={'name': 'test', 'phone': '9123456789', 'timing': '2020-08-31T13:00'}
        )

    res = client.post(
        '/api/v1/ticket',
        json={'name': 'test', 'phone': '9123456789', 'timing': '2020-08-31T19:00'}
    )
    res = res.get_json()
    res = client.put(
        'api/v1/ticket',
        json={'ticket_id': res['ticket_id'], 'timing': '2020-08-31T13:00'}
    )
    db.movie_tickets.tickets.drop()
    assert b'Maximum booking limit for this time exeeded' in res.data
    