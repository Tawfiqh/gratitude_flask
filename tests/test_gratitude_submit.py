import os
import tempfile

import pytest

from gratitude import gratitude


@pytest.fixture
def client():
    # db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    gratitude.app.config['TESTING'] = True

    with gratitude.app.test_client() as client:
        # with gratitude.app.app_context():
        #     gratitude.init_db()
        yield client

    # os.close(db_fd)
    # os.unlink(gratitude.app.config['DATABASE'])

gratitudeReasons = [
    'Loving parents',
    'Having a roof over my head',
    'Good friends',
    'Always being clothed',
    'Always being fed',
    'Good health',
    'Eyesight',
    'Being able to walk, talk',
    'Warmth',
    'Peaceful political climate',
];


def convert_byte_string_to_string(byte_string):
    return byte_string.decode("utf-8");


def test_gratitude_simple_submit(client):    
    rv = client.get('/gratitude_simple/submit')
    assert b'No entries here so far' in rv.data


def test_gratitude_submit(client):
    rv = client.get('/gratitude/submit')
    assert b'No entries here so far' in rv.data
