#!/bin/sh
# . .env
export FLASK_APP=gratitude
export  FLASK_ENV=development
export FLASK_PASSWORD=abc
export DB_FILE=../dataentry.sqlite3
echo "FLASK_APP:" $FLASK_APP
pip install -e . #needed to install gratitude  app too.
flask run
