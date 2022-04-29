from flask import (
flash,
Flask,
jsonify,
request,
redirect,
render_template,
make_response,
abort,
g
)

import config

from config import db
from models import (
    Person,
    PersonSchema,
)

from passlib.hash import sha256_crypt

import re

from json2html import *
import json

import time



regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

# Validation function against email field
def isValid(email):
    if re.fullmatch(regex, email):
      return True
    else:
      return False

# Empty value validation against all fields
def is_not_blank(s):
    return bool(s and not s.isspace())


# Referencing the config.app object instance
app = config.app
app.secret_key = 'secret project'   # Added to assist flash implementation 




###
@app.route("/")
def home():
    return "<h>Landing Page</h>"


# Using the g global object and attaching a function call to it
# To measure elapsed time for each request
@app.before_request
def before_request():
   g.request_start_time = time.time()
   g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)




###
"""
Application endpoints
"""


# To read from DB
@app.route('/read-all', methods=['GET'])
def read_all():
    """
    This function responds to a request for /read-all
    with the complete lists of people

    :return:        HTML table format of list of people
    """

    # Create the list of people from our data
    people = Person.query \
        .order_by(Person.name) \
        .all()

    # Serialize the data for the response
    person_schema = PersonSchema(many=True)

    #  storing jsonified version of all data in People table
    result = jsonify(person_schema.dump(people))

    """
    Use json.loads because result.data is of bytes type --> print(type(result.data)) ,
    which cannot be used directly with json2html.convert method
    """
    infoFromJson = json.loads(result.data)

    print(type(infoFromJson))
    print(infoFromJson)

    # Loop through json list to exclude password key and corresponding values
    new_list = [{k: v for k, v in d.items() if k != 'password'} for d in infoFromJson]

    # json2html converts json to html format table
    tabular_format = json2html.convert(json = new_list)
    return tabular_format




# To sign-in to Page
@app.route('/auth', methods=['GET', 'POST'])
def sign_in():
    """
    This function takes the registered user's email address and password
    and validate whether their account exists and password is correct.

    :return:        on success, render_template('success-page.html') 
    """

    # handle the POST request
    if request.method == 'POST':

        # data_received object containing information entered by user
        data_received = request.form
        
        user_email = data_received['email']
        user_password = data_received['password']

        # Nested If-elses to check for empty values
        if(is_not_blank(user_email)):
            if(is_not_blank(user_password)):

                # check if user_email is in valid format
                if(isValid(user_email)):
                    # checking is user exists in DB
                    existing_person = Person.query \
                        .filter(Person.email == user_email) \
                        .one_or_none()

                    # if user exists, validate password and sign-in
                    if existing_person is not None:

                        # Validate user_password against password in DB i.e. --> existing_person.password
                        if(sha256_crypt.verify(user_password, existing_person.password)):    

                            # Store success msg for 'success-page.html'
                            flash(f"User {user_email} has successfully Signed in") 
                            return render_template('success-page.html') 

                        else:
                            abort(401, 'Incorrect password')

                    # if user doesn't exist, redirect to '/registrations' API
                    elif existing_person is None:
                        flash("User doesn't exist.") 
                        return redirect('/registrations')

                    # # if both email & password are invalid, show error
                    # else:
                    #     abort(401, 'Invalid Information')
                # If user_email not in valid format, throw prompt
                else:
                    flash("Please enter a valid email format") 
                    return redirect('/auth')  # redirects to /registrations API
            else:
                flash("Empty values not accepted") 
                return redirect('/auth')
        else:
            flash("Empty values not accepted") 
            return redirect('/auth')

    else:
        # uses separate template file to show results - easier to handle multipage              
        return render_template('sign-in-page.html')
    






# To register person to DB
@app.route('/registrations', methods=['GET', 'POST'])
def register():
    """
    This function persist all valid records to a persistence-layer.
    SQLAlchemy, Marshmallow, SQLite used for this purpose

    :return:        on success, render_template('success-page.html')
    """

    # handle the POST request
    if request.method == 'POST':
        # Form data received from user input
        data_received = request.form
        
        user_name = data_received['name']
        user_email = data_received['email']
        user_password = data_received['password']

        # Nested If-elses to check for empty values
        if(is_not_blank(user_name)):
            if(is_not_blank(user_email)):
                if(is_not_blank(user_password)):

                    # check if user_email is in valid format
                    if(isValid(user_email)):

                        # storing password in encrypted format (using sha26_crypt from passlib.hash)
                        encrypted_password = sha256_crypt.encrypt(user_password)

                        # checks if user with email exists
                        existing_person = Person.query \
                            .filter(Person.email == user_email) \
                            .one_or_none()

                        # Can we insert this person?
                        if existing_person is None:

                            # Create a person instance using the schema and the passed-in person
                            schema = PersonSchema()

                            # Create a person instance using the schema and the passed-in person
                            p = Person(password=encrypted_password, email=user_email, name=user_name)
                            
                            # Add the person to the database
                            db.session.add(p)

                            db.session.commit()

                            
                            # Display success msg
                            flash("User has been successfully registered") 
                            return render_template('success-page.html')

                            # For testing (absolute) API response time
                            # return g.request_time()


                        # Otherwise, nope, person exists already
                        else:
                            abort(409, f'User {user_email} exists already')

                    # If user_email not in valid format, throw prompt
                    else:
                        flash("Please enter a valid email format") 
                        return redirect('/registrations')  # redirects to /registrations API
                else:
                    flash("Empty values not accepted") 
                    return redirect('/registrations')
            else:
                flash("Empty values not accepted") 
                return redirect('/registrations')
        else:
            flash("Empty values not accepted") 
            return redirect('/registrations')


    # render registration-page.html when executing function first-time i.e. when GET called            
    return render_template('registration-page.html')






if __name__ == '__main__':
    # Address for all devices to on local server to access this application
    # app.run(host="192.168.1.14", port=5000, debug=True, threaded=False)
    app.run()