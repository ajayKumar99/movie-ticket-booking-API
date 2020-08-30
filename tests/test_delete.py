import pytest
from movieApi import create_app
from movieApi.extensions import db

@pytest.mark.parametrize(('ticket_id', 'message'), (
    ('', b'Ticket ID to be deleted not provided'),
    ('test', b'Invalid ticket ID'),
    ('5f4b5b9fc8a7b99dec070935', b"Ticket doesn't exists"),
))
def test_deletion_inputs(client, ticket_id, message):
    res = client.delete(
        'api/v1/ticket',
        json={'ticket_id': ticket_id}
    )

    assert message in res.data

def test_deletion(client):
    res = client.post(
        '/api/v1/ticket',
        json={'name': 'test', 'phone': '9123456789', 'timing': '2020-08-31T19:00'}
    )
    res_t = res.get_json()
    res = client.delete(
        'api/v1/ticket',
        json={'ticket_id': res_t['ticket_id']}
    )
    db.movie_tickets.tickets.drop()
    msg = 'Ticket with id-' + res_t['ticket_id'] + ' deleted successfully'
    assert msg in str(res.data)