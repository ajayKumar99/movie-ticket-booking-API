from movieApi import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    res = client.get('/')
    assert b'Movie Ticket Booking API' in res.data