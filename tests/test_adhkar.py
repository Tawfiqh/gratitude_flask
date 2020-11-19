import os, sys
import pytest

from gratitude import gratitude
from gratitude import models


def saveDbModel(db, dbModel):
    try:
        db.session.add(dbModel)
        db.session.commit()
    except Exception as e:
        print( "\n FAILED entry: {}\n".format( message ) )
        print(e)
        sys.stdout.flush()

def newAdhkarData(db, dataTuple):
    arabic = dataTuple[0]
    english = dataTuple[1]
    secondsToRecite = dataTuple[2]
    minutesToRecite = dataTuple[3]
    shortDescription = dataTuple[4]

    newDatum= models.Adhkarentry(arabic, english, secondsToRecite,minutesToRecite, shortDescription)

    saveDbModel(db, newDatum)
    

db_adhkar = [
        (None, None, 120, 2.0, "salawat x 33"),
    	(None, None, 360, 6.0, "salawat x 100"),
    	(None, None, 60, 1.0, "subhanallah x 33, alhamdulillah x 33, allahuak"),
    	(None, None, 18, 0.3, "subhanallah x 10, alhamdulillah x 10, allahuak"),
    	(None, None, 0, None, "hasbunallahu wa nimal wakeel"),
];

def populate_db(db):
    for adhkar in db_adhkar:
        newAdhkarData(db,adhkar)

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


# Query for adhkar
def test_adhkar_query(client, some_db):    
    rv = client.get('/adhkar/query')
    assert b'No entries here so far' in rv.data



# Adhkar all
def test_adhkar_all(client, some_db):
    rv = client.get('/adhkar/all')
    assert b'No entries here so far' in rv.data
