import pytest
from movieApi import create_app
from movieApi.extensions import db

@pytest.mark.parametrize(('ticket_id', 'timing', 'message'), (
    ('', '', b'Time for which data to be fetched not provided'),
    ('test', '', b'Invalid ticket ID'),
    ('5f4b5b9fc8a7b99dec070935', '', b"Ticket doesn't exists"),
    ('', '2020-08-31T13:00', b"tickets")
))
def test_tickets_inputs(client, ticket_id, timing, message):
    res = client.get(
        '/api/v1/ticket',
        json={'ticket_id': ticket_id, 'timing': timing}
    )

    assert message in res.data


def test_tickets_by_id(client):
    res = client.post(
        '/api/v1/ticket',
        json={'name': 'test', 'phone': '9123456789', 'timing': '2020-08-31T19:00'}
    )
    res = res.get_json()
    
    res = client.get(
        'api/v1/ticket',
        json={'ticket_id': res['ticket_id']}
    )
    db.movie_tickets.tickets.drop()

    assert b'data' in res.data
