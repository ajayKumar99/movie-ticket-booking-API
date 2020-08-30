import pytest
from movieApi import create_app
from movieApi.extensions import db

@pytest.mark.parametrize(('name', 'phone', 'timing', 'message'), (
    ('', '', '', b'Username not provided'),
    ('test', '', '', b'Phone number not provided'),
    ('test', '9818257676', '', b'Ticket timing not provided'),
    ('test', '9818257676', '2020-08-31T13:00', b'Ticket Booked')
))
def test_booking_inputs(client, name, phone, timing, message):
    res = client.post(
        '/api/v1/ticket',
        json={'name': name, 'phone': phone, 'timing': timing}
    )
    db.movie_tickets.tickets.drop()
    assert message in res.data

def test_booking_limit(client):
    res = ''
    for i in range(21):
        res = client.post(
            '/api/v1/ticket',
            json={'name': 'test', 'phone': '9123456789', 'timing': '2020-08-31T13:00'}
        )
    db.movie_tickets.tickets.drop()
    assert b'Maximum booking limit for this time exeeded' in res.data

