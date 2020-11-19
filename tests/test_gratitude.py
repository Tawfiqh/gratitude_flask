import os, sys

import pytest

from gratitude import gratitude
from gratitude import models
from dotenv import load_dotenv


def saveDbModel(db, dbModel):
    try:
        db.session.add(dbModel)
        db.session.commit()
    except Exception as e:
        print( "\n FAILED entry: {}\n".format( message ) )
        print(e)
        sys.stdout.flush()


def newGratitudeData(db, message):
    newDatum= models.Dataentry(message)
    saveDbModel(db, newDatum)



db_gratitudeReasons = [
    "Test gratitude reason db 1",
    "Test gratitude reason db 2",
    "Test gratitude reason db 3",
];

def populate_db(db):
    for reason in db_gratitudeReasons:
        newGratitudeData(db,reason)

@pytest.fixture
def some_db(request):
    gratitude.app.config['TESTING'] = True
    gratitude.app.config['CSRF_ENABLED'] = False
    gratitude.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'test.db')
    gratitude.db.create_all()
    populate_db(gratitude.db);

    def fin():
        gratitude.db.session.remove()
        gratitude.db.drop_all()
    request.addfinalizer(fin)

@pytest.fixture
def client():
    load_dotenv()
    gratitude.app.config['TESTING'] = True

    with gratitude.app.test_client() as client:
        yield client

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
def test_gratitude(client, some_db):
    headers = {
        'Authorization': os.getenv('FLASK_PASSWORD')
    }

    response = client.get('/gratitude', headers=headers)
    
    dataFound = convert_byte_string_to_string(response.data) in db_gratitudeReasons
    assert dataFound


def test_gratitude_all(client, some_db):

    headers = {
        'Authorization': os.getenv('FLASK_PASSWORD')
    }

    response = client.get('/gratitude/all', headers=headers)
    
    actual = str(convert_byte_string_to_string(response.data)).split('<br />')
    expected = db_gratitudeReasons
    # expected = gratitudeReasons
    print("actual",actual)
    print("expected",expected)
    assert len(actual) == len(expected)
    assert all([a == b for a, b in zip(actual, expected)])
