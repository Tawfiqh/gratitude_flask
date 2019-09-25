Flask backend for gratitude app.

Setup on heroku:
```fish
$ heroku config:set FLASK_ENV=production --app gratitude-py
$ heroku config:set FLASK_PASSWORD=SECRET --app gratitude-py
```

Setup python database:
```fish
$ heroku run python --app gratitude-py
```

Then in the python console:
```
>>> from api import db
>>> db.create_all()
```


Can then create entries through command line easilly.
```fish
curl -G "https://gratitude-py.herokuapp.com/gratitude/submit" --data-urlencode "password=password" --data-urlencode "data=Warmth"
```
