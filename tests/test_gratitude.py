import os
import tempfile

import pytest

from gratitude import gratitude

# engine = create_engine(create_db_connection_str(config), echo=True)
# Session = scoped_session(sessionmaker(bind=engine))

# @pytest.fixture(scope="function") # or "module" (to teardown at a module level)
# def db_session():
#     Base.metadata.create_all(engine)
#     session = Session()
#     yield session
#     session.close()
#     Base.metadata.drop_all(bind=engine)


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
    '- Loving parents -',
    '- Having a roof over my head -',
    '- Good friends -',
    '- Always being clothed -',
    '- Always being fed -',
    '- Good health -',
    '- Eyesight -',
    '- Being able to walk, talk -',
    '- Warmth -',
    '- Peaceful political climate -',
];


def convert_byte_string_to_string(byte_string):
    return byte_string.decode("utf-8");


def test_gratitude_simple(client):
    response = client.get('/gratitude_simple')
    dataFound = convert_byte_string_to_string(response.data) in gratitudeReasons
    assert dataFound

def test_gratitude_simple_all(client):    
    response = client.get('/gratitude_simple/all')
    actual = str(convert_byte_string_to_string(response.data)).split('<br />')
    expected = gratitudeReasons
    print("actual",actual)
    print("expected",expected)
    assert len(actual) == len(expected)
    assert all([a == b for a, b in zip(actual, expected)])



# Database backed.
def test_gratitude(client):
    rv = client.get('/gratitude')
    assert b'No entries here so far' in rv.data


def test_gratitude_all(client):
    rv = client.get('/gratitude/all')
    assert b'No entries here so far' in rv.data
