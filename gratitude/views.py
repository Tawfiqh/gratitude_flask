from flask import Flask, request, send_from_directory, render_template, url_for, abort, Blueprint
import os

import random
import json

from gratitude import app
from . models import Dataentry, Adhkarentry


    # from adhkar import adhkarRoutes
# app.register_blueprint(adhkarRoutes, url_prefix='/adhkar')

from gratitude import misc_routes
app.register_blueprint(misc_routes.miscRoutes)


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
    return send_from_directory('gratitude_frontend', path)

@app.route('/')
def send_frontend_index():
    return send_frontend("frontend.html")





# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       Environment setup
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def is_development_mode():
    flask_envi = os.getenv('FLASK_ENV');
    return (flask_envi == "development")


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       DB Setup
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import sys
from flask_heroku import Heroku

heroku = Heroku(app)

if(is_development_mode()):
    db_file = 'sqlite:///' + os.getenv('DB_FILE','dataentry.sqlite3');
    app.config['SQLALCHEMY_DATABASE_URI'] = db_file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
db = SQLAlchemy()
db.init_app(app)

if(is_development_mode()):
    with app.app_context():
        db.create_all()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       Gratitude complex
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def check_password():
    supplied_password = None;

    if 'authorization' in request.headers:
        supplied_password = request.headers['authorization']

    print("password:", supplied_password)
    app_password = os.getenv('FLASK_PASSWORD')
    if(supplied_password != app_password):
        abort(401);

@app.route('/gratitude/submit', methods = ['GET'])
def post_to_db():

    check_password()

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
    check_password();
    random.seed()
    gratitudeReasonObjects = Dataentry.query.all()
    
    gratitudeReasons = [];
    for reason in gratitudeReasonObjects:
        gratitudeReasons.append(reason.data)
    print("grabbed list of reasons from db:",gratitudeReasons)
    if(len(gratitudeReasons)==0):
        return gratitudeSimple();
    return random.choice(gratitudeReasons)


@app.route('/gratitude/all')
def gratitudeReadAll():
    check_password();
    gratitudeReasons = Dataentry.query.all()

    allReasons = [];

    for reason in gratitudeReasons:
        allReasons.append(reason.data)

    return "<br />".join(allReasons)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       Adkhar app
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@app.route('/adhkar/')
def adhkar_frontend():
    return send_from_directory('adhkar_frontend', "index.html")

# Limit of 5
@app.route('/adhkar/query')
def adhkar_time_query():
    time = request.args.get('time')
    if(time == 0 or time == None):
        time = 60

    print("time", time);
    adhkar_list = Adhkarentry.query.filter(Adhkarentry.secondsToRecite <= time).order_by(desc(Adhkarentry.secondsToRecite)).limit(5)

    result = [];

    for dhikr in adhkar_list:
        oneResult = {
            "arabic": dhikr.arabic,
            "english": dhikr.english,
            "description": dhikr.shortDescription,
            "time_in_seconds": dhikr.secondsToRecite,
        }
        result.append(oneResult)

    return json.dumps(result), {'Content-Type': 'application/json'}


@app.route('/adhkar/all')
def all():

    adhkar_list = Adhkarentry.query.all()

    result = [];

    for dhikr in adhkar_list:
        oneResult = {
            "arabic": dhikr.arabic,
            "english": dhikr.english,
            "description": dhikr.shortDescription,
            "time_in_seconds": dhikr.secondsToRecite,
        }
        result.append(oneResult)

    return json.dumps(result), {'Content-Type': 'application/json'}

