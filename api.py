from flask import Flask, request, send_from_directory

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

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hi')
def hello_world2():
    return 'Hi, World!'


@app.route('/time')
def current_time():
    today = datetime.now()
    result =  today.strftime("%H:%M:%S on %d %B, %Y: ") + "Hello world"
    return result;


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

@app.route('/frontend/<path:path>')
def send_frontend(path):
    return send_from_directory('frontend', path)

@app.route('/frontend')
def send_frontend_index():
    return send_from_directory('frontend', "frontend.html")



if __name__ == "__main__":
    application.run(host='0.0.0.0')
