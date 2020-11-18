# Flask backend for gratitude app.


# App Structure 
`wsgi.py` runs on first load



# Running the app
## Run it locally
```fish
$ ./startServer.sh
```
s


# Heroku setup
## Setup on heroku:
```fish
$ heroku config:set FLASK_ENV=production --app gratitude-py
$ heroku config:set FLASK_PASSWORD=SECRET --app gratitude-py
```

## Setup python database:
```fish
$ heroku run python --app gratitude-py
```

Then in the python console:
```
>>> from api import db
>>> db.create_all()
```

for local:
```bash
source .env
flask shell
```

and then run:
```
>>> from api import db
>>> db.create_all()
```


## Seeing application logs on heroku

```fish
$ heroku logs --tail --app gratitude-py
```



# Creating new entries 
Can then create entries through command line easilly.
```fish
$ curl -G "https://gratitude-py.herokuapp.com/gratitude/submit" --data-urlencode "password=password" --data-urlencode "data=Warmth"
```

