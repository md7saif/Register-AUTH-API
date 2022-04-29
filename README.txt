--> STEP 1:

Python 3 needs to be installed to run .py scripts
Install following libraries & packages on the host system,

pip install Flask
pip install Flask-SQLAlchemy flask-marshmallow marshmallow-sqlalchemy marshmallow
pip install passlib
pip install json2html

Version information in requirements.txt

--> STEP 2:

Run API.py

--> STEP 3:

Copy-paste development server address onto a browser and append endpoint names (identifier)

- - - - - - 


--> List of endpoints:

/auth
[POST, GET]
This endpoint takes the registered user's email address and password
and validate whether their account exists and password is correct.

/registration
[POST, GET]
This endpoint persist all valid records to a persistence-layer.
SQLAlchemy, Marshmallow, SQLite used for this purpose

/read-all
[GET]
This endpoint reads from DB Table,
and parses data to HTML table format containing list of people
