# Application structure

```
core
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
└── wsgi.py
movie_api
├── __pycache__
├── admin.py
├── apps.py
├── migrations
│   ├── 0001_initial.py
│   ├── other_migrations.py
│   └── __init__.py
├── models.py
├── tests.py
├── urls.py
└── views.py
static
media
```


# Running the Django Application

To run the Django application, follow these steps:

Create a virtual environment and pip install the requirements.txt file

`pip install -r requirements.txt`

Then since this is a dev environment you have to run the migrations commands from the root directory of the project.

`py manage.py migrate`

Finally just run the following to spin up the application:
`py manage.py runserver`


By default the application will be served at: http://127.0.0.1:8000/
