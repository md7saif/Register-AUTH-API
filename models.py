"""
models.py is where the Person SQLAlchemy and PersonSchema Marshmallow class definitions are described. 
This module is dependent on config.py for some of the objects created and configured there. 
"""

from config import db, ma
import os


# Declare the model
# Creating this model using SLQAlchemy will also sanitise user data
class Person(db.Model):
    __tablename__ = "person"    # connects the class definition to the person database table
    user_id = db.Column(db.Integer, primary_key=True)     # creates a DB column containing an integer --> as the primary key for the table
    name = db.Column(db.String(60))
    email = db.Column(db.String(32))
    password = db.Column(db.String(16))


"""
 introspecting the Person class to help serialize/deserialize instances of that class.
"""
# Generate marshmallow schema from the model
class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        sql_session = db.session



# Data to initialize database with
PEOPLE = [
    # {"name": "Kent", "email": "kent@test.com", "password": "123"},
    # {"name": "Bunny", "email": "bunny@test.com", "password": "123"},
]

# Delete database file if it exists currently
def delete_table():
    if os.path.exists("people.db"):
        os.remove("people.db")

# Can be called to delete DB and initialise new DB
# delete_table()


# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
if not os.path.exists("people.db"):
    for person in PEOPLE:
        p = Person(name=person.get("name"), email=person.get("email"), password=person.get("password"))
        db.session.add(p)   # Uses the database connection instance db to access the session object. 
    
    db.session.commit()     # to actually save all the person objects created to the database
