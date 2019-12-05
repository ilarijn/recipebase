## Local installation

For a local installation of the application, you must have Python 3 installed.

Make sure you can run `python3` and `pip` from the command line, download the contents of this repository and enter the following commands in the application's root directory.

Install virtual environment:

```python3 -m venv venv```

Activate virtual environment::

```source venv/bin/activate```

Install requirements:

```pip install -r requirements.txt```

Run the application:

```python3 run.py```

The application is now accessible by browser at http://localhost:5000/.

---

## Deploying to Heroku

Make sure the repository contains a Procfile with the following settings:
 
```web: gunicorn --preload --workers 1 application:app```

Run the following to initialize a Heroku project, add it as a remote and push:

```heroku create [project_name]```

```git remote add heroku https://git.heroku.com/[repository_name].git```

```git push heroku master```

Initialize a database on Heroku:

```heroku addons:add heroku-postgresql:hobby-dev```

Configure the application to use PostgreSQL when running on Heroku. Run:

```heroku config:set HEROKU=1```

And make sure `__init__.py` contains the following setting:

```python
 if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
```

The database on Heroku can be accessed with:

```heroku pg:psql```