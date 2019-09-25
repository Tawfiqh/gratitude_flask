from flask import Flask, request, send_from_directory, render_template, url_for

import random
from datetime import datetime
app = Flask(__name__)

gratitudeReasons = [
    "Loving parents",
    "Having a roof over my head",
    "Good friends",
    "Always being clothed",
    "Always being fed",
    "Good health",
    "Eyesight",
    "Being able to walk, talk",
    "Warmth",
    "Peaceful political climate",
];


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       Inane miscelania
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route('/hi')
def hello_world2():
    return 'Hi, World!'


@app.route('/time')
def current_time():
    today = datetime.now()
    result =  today.strftime("%H:%M:%S on %d %B, %Y: ") + "Hello world"
    return result;






# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       Gratitude simple
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@app.route('/gratitude_simple')
def gratitudeSimple():
    random.seed()
    return random.choice(gratitudeReasons)

@app.route('/gratitude_simple/submit', methods = ['GET'])
def gratitudeSimpleSubmit():
    gratitudeMessage = request.args.get('data')
    gratitudeReasons.append(gratitudeMessage)
    return gratitudeSimple()

@app.route('/gratitude_simple/all')
def gratitudeSimpleAll():
    return "<br />".join(gratitudeReasons)





# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       frontend simple
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@app.route('/frontend/<path:path>')
def send_frontend(path):
    return send_from_directory('frontend', path)

@app.route('/')
def send_frontend_index():
    return send_from_directory('frontend', "frontend.html")









# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       DB Setup
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
from flask_sqlalchemy import SQLAlchemy
import sys


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataentry.sqlite3'
db = SQLAlchemy(app)

class Dataentry(db.Model):
    __tablename__ = "dataentry"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text())

    def __init__ (self, data):
        self.data = data

db.create_all()


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       Gratitude complex
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route('/gratitude/submit', methods = ['GET'])
def post_to_db():
    message = request.args.get('data')

    newDatum= Dataentry(message)
    try:
        db.session.add(newDatum)
        db.session.commit()

    except Exception as e:
        print( "\n FAILED entry: {}\n".format( message ) )
        print(e)
        sys.stdout.flush()

    return 'Success! Saved: \n' + message;



@app.route('/gratitude')
def gratitudeComplex():
    random.seed()
    gratitudeReasonObjects = Dataentry.query.all()

    gratitudeReasons = [];
    for reason in gratitudeReasonObjects:
        gratitudeReasons.append(reason.data)

    return random.choice(gratitudeReasons)


@app.route('/gratitude/all')
def gratitudeReadAll():
    gratitudeReasons = Dataentry.query.all()

    allReasons = [];

    for reason in gratitudeReasons:
        allReasons.append(reason.data)

    return "<br />".join(allReasons)





# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       Setup and run main app
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

if __name__ == "__main__":
    app.debug = True
    application.run(host='0.0.0.0')


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()
