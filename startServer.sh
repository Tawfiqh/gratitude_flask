#!/bin/sh
export FLASK_APP=api.py
export FLASK_ENV=development
export FLASK_PASSWORD=abc

flask run
