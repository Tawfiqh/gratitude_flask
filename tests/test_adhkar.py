import os, sys, json
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
    

db_adhkar_input = [
        # arabic, english, secondsToRecite, minutesToRecite, shortDescription
        (None, None, 120, 2.0, "Test: salawat x 33"),
    	(None, None, 360, 6.0, "Test: salawat x 100"),
    	(None, None, 60, 1.0, "Test: subhanallah x 33, alhamdulillah x 33, allahuak"),
    	(None, None, 18, 0.3, "Test: subhanallah x 10, alhamdulillah x 10, allahuak"),
    	(None, None, 0, None, "Test: hasbunallahu wa nimal wakeel"),
];

def populate_db(db):
    for adhkar in db_adhkar_input:
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
    gratitude.app.config['TESTING'] = True
    with gratitude.app.test_client() as client:
        yield client


def convert_byte_string_to_string(byte_string):
    return byte_string.decode("utf-8");

def compareArrays(actual, expected):
    print("actual",actual)
    print("expected",expected)
    assert len(actual) == len(expected)
    assert all([a == b for a, b in zip(actual, expected)])


def _parseResponseItemBackToFormat(responseItem):

    arabic = responseItem["arabic"]
    english = responseItem["english"]
    description = responseItem["description"]
    time_in_seconds = responseItem["time_in_seconds"]

    result = (arabic, english, description, time_in_seconds)
    return result;

def _parseResponse(responseData):
    responseItems = json.loads( str(convert_byte_string_to_string(responseData)) )
    
    return list(map(_parseResponseItemBackToFormat, responseItems))
    
# Convert our input-data to the same order as the response data
def _dbInputToResponseTuple(dbTupleInput):
    # (None, None, 120, 2.0, 'Test: salawat x 33')
    # (None, None, 'Test: salawat x 33', 120)
    return (dbTupleInput[0],
            dbTupleInput[1],
            dbTupleInput[4],  
            dbTupleInput[2]
        )


# Adhkar all
def test_adhkar_all(client, some_db):
    response = client.get('/adhkar/all')    
    
    actual = _parseResponse(response.data);

    # Need to switch up the order to the o
    expected = list(map(_dbInputToResponseTuple, db_adhkar_input))

    compareArrays(actual, expected);


def _dbInputFilteredByTimeLimit(timeLimit, db_adhkar_input):
    # secondsToRecite = tuple[2]
    filtered_db_adhkar = filter(lambda x: x[2] <= timeLimit, db_adhkar_input)
    expected = map(_dbInputToResponseTuple, filtered_db_adhkar)
    expected = list(expected)
    # print('filtered_db_adhkar_input', expected)
    expected.sort(key=lambda x: x[3], reverse=True)#changes list in place. use .sorted() to return new sorted list.
    return expected



# Query for adhkar
def test_adhkar_query(client, some_db):
    for timeLimit in range(0,1000, 15):
        response = client.get(f'/adhkar/query?time={timeLimit}')
        actual = _parseResponse(response.data);

        print("Testing time limit:", timeLimit)
        # Need to switch up the order and filter by time
        expected = _dbInputFilteredByTimeLimit(timeLimit, db_adhkar_input)

        compareArrays(list(actual), expected );
