"""
config.py gets the necessary modules imported into the program and configured.
"""

import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask



app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))	# creates the variable basedir pointing to the directory the program is running in.

# Build the Sqlite ULR for SqlAlchemy
sqlite_url = "sqlite:///" + os.path.join(basedir, "people.db")


# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True	# 'True' logs SQLite operations to console
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url		# tells SQLAlchemy to use SQLite as the database, and a file named people.db in the current directory as the database file. 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 	# Since you’re not creating an event-driven program, turn this feature off.

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)