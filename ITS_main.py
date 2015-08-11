# Interstellar Travel Services
#authored by Victor Asselta (with a little help from stackoverflow)
#August 10, 2015
#
# For Udacity's Full Stack developers course project 3
#
#_________________________________________________________________________
#
# This file represents the controller portion of an MVC style app
#
# See ITS.db for the model, and the templates folder for the view components.
# Please read the README.TXT DO. It's short.
#
# ITS.db is necessary to run this app. Use ITS_db.setup.py to create the database
# and ITS_db_populate.py to populate it.
#___________________________________________________________________________


# Core Flask imports
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory

app = Flask(__name__)

# Anti-forgery State tokes import
from flask import session as login_session
import random, string, os

# oauth imports
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# ORM imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ITS_db_setup import Base, Passengers, Species, Agents, Destinations, TravelMethod, Menu, TestPassengers, \
    TestingStatus, Tests

# import bleach to sanitize image queries
import bleach

# Create the database connection and engine
engine = create_engine('sqlite:///ITS.db')
Base.metadata.bind = engine

# Create an instance of session to handle CRUD
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Stored Google+ local secrets file path
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Routes for index/ login area
@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
@app.route('/index.html/', methods=['GET'])
@app.route('/login', methods=['GET'])
def index():

    # Page to render within master.
    user_location = 'login.html'

    # Anti-forgery State Token generation.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('master2.html', STATE=state, page=user_location, navigation=False)


# Agent/ User landing page after successful login.
@app.route('/agent_home/', methods=['GET', 'POST'])
def agent_home():

    # Verify that user is logged in. If not redirect.
    # Repeated for all locations requiring authorization.
    if 'username' not in login_session:
        print "User is not logged in. Redirecting to index."
        return index()
    else:

        # A mechanism to add star images to the agent's home page
        # based on how many tests completed. A ranking if you will
        # Not fully implemented.

        # Begin variable to hold star related html
        output = ''

        # Attempt to load the agent's test history.
        # Each attempt is recorded so only one successful
        # completion of each of the three tests is necessary
        try:
            stars = 0
            test1 = session.query(TestingStatus).filter_by(test_id=1, test_complete=True).one()
            test2 = session.query(TestingStatus).filter_by(test_id=2, test_complete=True).one()
            test3 = session.query(TestingStatus).filter_by(test_id=3, test_complete=True).one()

            # Check the results and tally the stars
            if test1 is not None:
                stars += 1
            if test2 is not None:
                stars += 1
            if test3 is not None:
                stars += 1

            counter = 0
            star = '<div class="float_image"><img src="../static/images/star.gif" height="50", width="50" ' \
                   'alt="star"></div>'

            while counter <= stars:
                output += star

        # Exception in the even that the above is incomplete.
        except:
            print "Unable to access Testing Status for current agent."

        # Page to render within master.
        user_location = 'agent_home.html'

        return render_template('master2.html', page=user_location, stars=output)


# Complete interface for working with all available clients.
# Function accepts a client id in the case of an edit event.
# Client is set to none in the case that a client has yet to be chosen  or created.
@app.route('/clients', methods=['GET', 'POST'])
@app.route('/clients/<int:client_id>', methods=['GET', 'POST'])
def clients(client_id=None):

    if 'username' not in login_session:
        print "User is not logged in. Redirecting to index."
        return index()
    else:

        # Page to render within master.
        user_location = 'clients.html'

        # Default client image in the event that none is provided.
        default_image = '../static/images/eyes.gif'

        # Populate selection drop down menu with all clients.
        # Including those of other agents.
        # Agents have limited access to other agents clients.
        client_list = session.query(Passengers).all()
        client_drop_down = ''

        for client in client_list:
            client_drop_down += '<option value="{}">{}</option>'.format(client.id, client.last_name)

        # Populate species drop down form input
        # Load all different potential species choices from the database.
        species_list = session.query(Species).all()
        species_drop_down = ''

        for species in species_list:
            species_drop_down += '<option value="{}">{}</option>'.format(species.id, species.name)

        # If the edit_client form is submitted via POST
        # for saved changes for recently edited or newly
        # created clients.
        if request.method == 'POST':
            is_new_client = request.form['new_client']

            # Is this a new client?
            # Check to see if client is new.
            # Add current Agent's own id for ownership purposes.
            if is_new_client == 'True':
                print "New client route taken."

                # Attempt to establish current logged in Agent_id
                # Google+ does not always supply email leading to mssing email key.
                try:
                    # email maybe be default added email if this is the case.
                    new_agent_id = get_agent_id(login_session['email'])

                except:
                    # if key email problematic, attempt to
                    # gain previously established agent_id.
                    new_agent_id = login_session['agent_id']

                # If agent_id fails, set default.
                if new_agent_id is None:
                    new_agent_id = '2'
                    print ("Warning: default agent_id set")

                # retrieve form values
                new_first_name = request.form['first_name']
                new_last_name = request.form['last_name']
                new_species_id = request.form['current_species']
                new_notes = request.form['notes']

                # try:
                #     new_image = request.form['image']
                # except:
                #     print "Warning: No Image data from form"

                # Call the default client image
                uploaded_image = default_image

                # Attempt call the upload function and
                # update the image location.
                # try:
                #     if new_image is not None:
                #         is_true = upload_client_image(new_image)
                #         if is_true == True:
                #             uploaded_image = new_image
                # except:
                #     print "Unable to add image"

                # Add the new client to the Passenger table in the database
                new_client = Passengers(first_name=new_first_name, last_name=new_last_name, species_id=new_species_id,
                                        agent_id=new_agent_id, notes=new_notes, image=default_image)

                session.add(new_client)
                session.commit()

                flash("Client successfully added.")

                # Try to locate newly created client based off of first and last name for necessary id
                try:
                    locate_new_client = session.query(Passengers).filter_by(last_name=new_last_name,
                                                                        first_name=new_first_name).one()
                    locate_id = locate_new_client.id

                    # client_id establish so set on client's page
                    return render_template('master2.html', page=user_location, choose_client=client_drop_down,
                                           choose_species=species_drop_down, client_id=locate_id)

                # Did not locate necessary client_id. Redirect to agent_home so client page can reload properly.
                except:

                    # return url_for('agent_home')
                    agent_home()

            # Path for editing an existing client record.
            else:
                print "Modified client route taken"
                # retrieve form values
                edit_client_id = request.form['client_id']
                edit_first_name = request.form['first_name']
                edit_last_name = request.form['last_name']
                edit_species_id = request.form['current_species']
                edited_notes = request.form['notes']

                # try:
                #     edited_image = request.form['image']
                # except:
                #     print "Warning: No Image data from form"

                # Load the default client image
                uploaded_image = default_image

                # Attempt call the upload function and
                # update the image location.
                # try:
                #     if edited_image is not None:
                #         is_true = upload_client_image(edited_image)
                #         if is_true is True:
                #             uploaded_image = edited_image
                # except:
                #     print "Unable to add image."

                client_to_edit = session.query(Passengers).filter_by(id=edit_client_id).one()
                if client_to_edit.agent_id != login_session['agent_id']:
                    flash("You can only edit your own clients")
                    return redirect(url_for('clients'))

                client_to_edit.first_name = edit_first_name
                client_to_edit.last_name = edit_last_name
                client_to_edit.species_id = edit_species_id
                client_to_edit.notes = edited_notes
                client_to_edit.image = uploaded_image
                session.add(client_to_edit)
                session.commit()

                updated_client = session.query(Passengers).filter_by(id=edit_client_id).one()
                flash("Client successfully updated.")

                return render_template('master2.html', page=user_location, choose_client=client_drop_down,
                                       choose_species=species_drop_down, first_name=updated_client.first_name,
                                       last_name=updated_client.last_name, selected_species_id=updated_client.species_id,
                                       notes=updated_client.notes, client_id=updated_client.id,
                                       client_image=default_image)

        # Non-post route that allows for loading a client to edit before post submission.
        # Also allows the form to render if a new client is created.
        # If there is a chosen client to work with proceed.
        elif client_id is not None:

                # Error checking. Attempt to load a complete client record.
                try:
                    # attempt to load the selected client from the database
                    passenger = session.query(Passengers).filter_by(id=client_id).one()
                    species = session.query(Species).filter_by(id=passenger.species_id).one()

                    return render_template('master2.html', page=user_location, choose_client=client_drop_down,
                                           choose_species=species_drop_down, first_name=passenger.first_name,
                                           last_name=passenger.last_name, selected_species_id=species.id,
                                           selected_species_name=species.name, notes=passenger.notes,
                                           client_id=client_id, client_image=default_image)

                # If there is an error loading client information
                # Alert the user with a flash message and disable form elements.
                except:
                    flash("Unable to retrieve client information")
                    return render_template('master2.html', page=user_location, choose_client=client_drop_down,
                                           choose_species=species_drop_down, selected_species_id='empty',
                                           selected_species_name='Species..', trip_button='disabled',
                                           edit_button='disabled', client_image=default_image)

        # No client appears to be chosen
        # Render the form disabled until an actionable choice has been made.
        else:
            return render_template('master2.html', page=user_location, choose_client=client_drop_down,
                                   choose_species=species_drop_down, trip_button='disabled',
                                   edit_button='disabled', client_image=default_image, selected_species_id='1')


# Route for client deletion.
# Requires integer variable of client_id.
# A javascript generated warning/ confirmation precedes this path. (See static\ITS_script.js)
@app.route('/delete_client/<int:client_id>', methods=['GET', 'POST'])
def delete_client(client_id):

    # Page to render within master.
    user_location = 'results.html'

    # Check for user login. Redirect if username is missing.
    if 'username' not in login_session:
        print "User is not logged in. Redirecting to index."
        return index()

    else:
        # Load passenger to delete.
        passenger_delete = session.query(Passengers).filter_by(id=client_id).one()

        # Check if passenger id matches the current logged in agent's
        # If does not match, alert the agent.
        if passenger_delete.agent_id != login_session['agent_id']:
            flash("Unauthorized intrusion detected")
            message = "Unauthorized intrusion detected. Action Denied"

            return render_template('master2.html', page=user_location, message=message )

        # All checks passed. Delete the client.
        else:
            session.delete(passenger_delete)
            session.commit()
            flash("Passenger Deleted")
            message = "Passenger has been successfully deleted."

            return render_template('master2.html', page=user_location, message=message)


# Path for logged in agent to book a trip for previously selected client.
# Requires integer variable of client_id
# Path no longer requires post, just client id.
@app.route('/create_trip/<int:client_id>', methods=['GET', 'POST'])
def create_trip(client_id):

    # Page to render within master.
    user_location = 'create_trip.html'

    # Check for user login. Redirect if username is missing.
    if 'username' not in login_session:
        print "User is not logged in. Redirecting to index."
        return index()

    elif client_id is not None:

                passenger = session.query(Passengers).filter_by(id=client_id).one()
                name = "Name: " + str(passenger.first_name) + " " + str(passenger.last_name)
                image = '../static/images/eyes.gif'

                flash("Booking travel for: {} {}".format(passenger.first_name, passenger.last_name))
                return render_template('master2.html', page=user_location, name=name, client_image=image,
                                       client_id=client_id, notes=passenger.notes)

    else:
        flash("Choose a passenger from clients to continue")
        return render_template('master2.html', page=user_location, choice_where="disabled",
                               choice_how="disabled", choice_food='disabled', book_it='disabled')


# Route to a generic results page that alerts a user to outcomes.
# Accepts variable integer client_id to provide personalized response.
# Known bug. client_id is not always being passed resulting
@app.route('/results', methods=['GET', 'POST'])
@app.route('/results/<int:client_id>', methods=['GET', 'POST'])
def results(client_id=None):

    user_location = 'results.html'

    if 'username' not in login_session:
        print "User is not logged in. Redirecting to index."
        return index()
    else:

        flash("LOCATION: Trip Results")

        if request.method == 'POST':

            # Check for properly passed client_id.
            # If present render personalized message.
            if client_id is not None:
                passenger = session.query(Passengers).filter_by(id=client_id).one()

                message = "We are please to inform you that your client " + str(passenger.first_name) + " " \
                          + str(passenger.last_name) + " was quite pleased with your choices for travel, accommodations, " \
                                                       "and cuisine. On behalf of Interstellar Travel Services, " \
                                                       "we would like to thank you for using our services. Billing " \
                                                       "will, of course, be hounding you, without any mercy, shortly. " \
                                                       "Management"
                return render_template('master2.html', page=user_location, message=message)

            # Client_id has not been received.
            # Return generic message.
            else:

                message = "We are please to inform you that your client was quite pleased with your choices for travel, " \
                          "accommodations, and cuisine. On behalf of Interstellar Travel Services, we would like to " \
                          "thank you for using our services. Billing will, of course, be hounding you, without any " \
                          "mercy, shortly. Management"

                return render_template('master2.html', page=user_location, message=message)

        # In the event that user is not properly logged in.
        # Send alert.
        else:
            message = "You should not be here. The authorities have been notified"
            return render_template('master2.html', page=user_location, message=message)


# Begin Agent Testing generation
@app.route('/agent_choose_test', methods=['GET', 'POST'])
def agent_choose_test():

    # Verify that user is logged in. If not redirect.
    # Repeated for all locations requiring authorization.
    if 'username' not in login_session:
        print "User is not logged in. Redirecting to index."
        return index()

    user_location = 'agent_choose_test.html'

    # Attempt to load the test passengers for the agent game.
    # Build out the html code and add the the template
    try:
        test_passengers = session.query(TestPassengers).all()

        output = ''

        for client in test_passengers:
            output += '<span class="float_image">'
            output += '<a href="/agent_testing/' + str(client.id) + '">'
            output += '<p>' + str(client.first_name) + ' ' + str(client.last_name) + '</p>'
            output += '<img src="' + str(client.image) + '" height="200" width="180"'
            output += 'alt="' + str(client.first_name) + '" >'
            output += '</a></span>'

        return render_template('master2.html', page=user_location, clients=output)

    except:
        flash("Error: Unable to access test clients.")
        return render_template('master2.html', page=user_location, client='Unable to access clients')


# The agent testing page is a sister page to the create_trip page.
# Takes the test client id from the above script and loads the page
# with an image of said client and basic info.
@app.route('/agent_testing/<int:test_client_id>', methods=['GET', 'POST'])
def agent_testing(test_client_id):

    # Verify that user is logged in. If not redirect.
    # Repeated for all locations requiring authorization.
    if 'username' not in login_session:
        print "User is not logged in. Redirecting to index."
        return index()

    # Page to render within master.
    user_location = 'agent_testing.html'

    # Check for user login. Redirect if username is missing.
    if 'username' not in login_session:
        print "User is not logged in. Redirecting to index."
        return index()

    test_passenger = session.query(TestPassengers).filter_by(id=test_client_id).one()
    name = "Name: " + str(test_passenger.first_name) + " " + str(test_passenger.last_name)
    image = test_passenger.image

    flash("Booking travel for: {} {}".format(test_passenger.first_name, test_passenger.last_name))

    return render_template('master2.html', page=user_location, name=name, client_image=image,
                           client_id=test_passenger.id, notes=test_passenger.notes)


# A sister page to the results page. Uses the result.html template.
# Take a client id and builds out a result message.
@app.route('/test_results', methods=['GET', 'POST'])
@app.route('/test_results/<int:test_client_id>', methods=['GET', 'POST'])
def test_results(test_client_id=None):

    # Verify that user is logged in. If not redirect.
    # Repeated for all locations requiring authorization.
    if 'username' not in login_session:
        print "User is not logged in. Redirecting to index."
        return index()

    if test_client_id is None:
        test_client_id = request.form['client_id']

    user_location = 'results.html'

    # The following attempts to load the users choices, the correct selections
    # as outlined in the database and evaluate and store the results.
    try:
        # email maybe be default added email if this is the case.
        new_agent_id = get_agent_id(login_session['email'])

    except:
        # if key email problematic, attempt to
        # gain previously established agent_id.
        new_agent_id = login_session['agent_id']

    # If agent_id fails, set default.
    if new_agent_id is None:
        new_agent_id = '2'
        print ("Warning: default agent_id set")

    # Submitted answers
    submitted_where = request.form['trip_where']
    submitted_how = request.form['trip_how']
    submitted_food = request.form['trip_food']

    # Correct answers
    test_parameters = session.query(Tests).filter_by(passenger_id=test_client_id).one()
    test_id = test_parameters.id
    test_name = test_parameters.test_name
    test_where = test_parameters.destination_id
    test_how = test_parameters.travel_method_id
    test_food = test_parameters.menu_id

    if submitted_where == test_where and submitted_how == test_how and submitted_food == test_food:

        flash_message = "Success! TEST: " + str(test_name) + " completed"

        results_message = "Success. Your swift intuition and keen understanding of client needs have netted you," \
                          "and you client an upgrade!"

        try:
            update_agent_status = TestingStatus(agent_id=new_agent_id, test_id=test_id, test_complete=True)
            session.add(update_agent_status)
            session.commit()
        except:
            flash_message += " -> Warning <- unable to add test results"

    else:

        flash_message = "Initiate Lock down! TEST: " + str(test_name) + " has gone horribly wrong!"

        results_message = "Unfortunately your choices have led to death and property damage of staggering severity." \
                          "Please report to the legal department."

        try:
            update_agent_status = TestingStatus(agent_id=new_agent_id, test_id=test_id, test_complete=False)
            session.add(update_agent_status)
            session.commit()
        except:
            flash_message += " -> Warning <- unable to add test results"

    flash(flash_message)

    return render_template('master2.html', page=user_location, message=results_message)


# Return all vacation destination in JSON format
@app.route('/destinations/JSON')
def destinations_info_json():
    destinations = session.query(Destinations).all()
    return jsonify(destinations=[i.serialize for i in destinations])


# Return all vacation travel methods in JSON format
@app.route('/travel_method/JSON')
def travel_method_info_json():
    travel_method = session.query(TravelMethod).all()
    return jsonify(travel_method=[i.serialize for i in travel_method])


# Return all menu items available during travel in JSON format
@app.route('/menu/JSON')
def menu_info_json():
    menu = session.query(Menu).all()
    return jsonify(menu=[i.serialize for i in menu])


# Begin Login related functions

# Agent Handling Functions
def create_agent(login_session):
    new_agent = Agents(name = login_session['username'], email=login_session['email'],
                       picture=login_session['picture'])
    session.add(new_agent)
    agent = session.query(Agents).filter_by(email=login_session['email']).one()
    return agent.id


def get_agent_info(agent_id):
    agent = session.query(Agents).filter_by(id=agent_id).one()
    return agent


def get_agent_id(email):
    try:
        agent = session.query(Agents).filter_by(email=email).one()
        return agent.id
    except:
        return None


# Google Connect Function
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID does not match giver user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data["name"]
    print login_session['username']
    login_session['picture'] = data["picture"]
    print login_session['picture']
    try:
        login_session['email'] = data["email"]
        print login_session['email']
    except:
        login_session['email'] = 'email@email.com'
        print "Warning: 'email' key not supplied, default email set"

    # For generic logout function
    login_session['provider'] = 'google'

    output = ''
    output += '<span class="message_flashing">Welcome, '
    output += login_session['username']
    output += '!</span>'
    output += '<img src="'
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px; webkit-radius: 150px;' \
              'moz-border-radius: 150px;">'

    flash("Travel Agent Identified as: %s" % login_session['username'])

    # See if user exists, if it doesn't make a new one
    agent_id = get_agent_id(login_session['email'])
    if not agent_id:
        agent_id = create_agent(login_session)
    login_session['agent_id'] = agent_id

    return output


# Google Disconnect and purge session parameters
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token.
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        try:
            del login_session['email']
        except:
            print "No email key to delete"
        del login_session['picture']

        # response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('index'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400)
        )
        response.headers['Content-Type'] = 'application/json'
        # return response
        return redirect(url_for('index'))

# Begin Image handling functions
# For custom images for clients

# Setup a directory for file uploads for custom image handling
app.config['UPLOAD_FOLDER'] = '../static/uploads/'

# key for accepted file types
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'gif', 'png'])


# check to see if file is accepted file type
def check_file_type(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# Function that attempts to process and uploaded client image
def upload_client_image(image):

    try:
        image = request.files['image']
        print image
        if image and check_file_type(image.filename):
            # provided extension not available to secure file name.
            # Need to find an alternative
            # filename = secure_filename(file.filename)

            filename = bleach.clean(image.filename)
            print filename

            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print "Message: Image upload successful"

        return True

    except:
        print "Warning: Image upload failed"

        return False


""" Removed FB login in this version. """
""" The API has since changed and does not return and email """
""" Also have been unable to download client secret file referenced on line 527 """

# @app.route('/fbconnect', methods=['POST'])
# def fbconnect():
#     if request.args.get('state') != login_session['state']:
#         response = make_response(json.dumps('Invalid state parameter.'), 401)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#     access_token = request.data
#
#     # Exchange client token for long-lived server-side token with GET /oauth/
#
#     app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
#     app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
#     url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s' \
#           'client_secret=%s&fb_exchange_token=%s' % (app_id,app_secret,access_token)
#     h = httplib2.Http()
#     result = h.request(url, 'GET')[1]
#
#     # Use token to get user info from API
#     userinfo_url = "https://graph.facebook.com/v2.2/me"
#     # strip expire tag from access token
#     token = result.split("&")[0]
#
#     url = 'https://graph.facebook.com/v2.2/me?%s' % token
#     h = httplib2.Http()
#     result = h.request(url, 'GET')[1]
#
#     data = json.loads(result)
#     login_session['provider'] = 'facebook'
#     login_session['username'] = data['name']
#     login_session['email'] = data['email']
#     login_session['facebook_id'] = data['id']
#
#     # Get user picture
#     url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200' % token
#     h = httplib2.Http()
#     result = h.request(url, 'GET')[1]
#     data = json.loads(results)
#
#     login_session['picture'] = data['data']['url']
#
#     # See if user exists, if it doesn't make a new one
#     agent_id = get_agent_id(login_session['email'])
#     if not agent_id:
#         agent_id = create_agent(login_session)
#     login_session['agent_id'] = agent_id
#
# @app.route('/fbdisconnect')
# def fbdisconnect():
#
#     facebook_id = login_session['facebook_id']
#     url = 'https://graph.facebook.com/%s/permissions' % facebook_id
#     h = httplib2.Http(url, 'DELETE')[1]
#     del login_session['username']
#     del login_session['email']
#     del login_session['picture']
#     del login_session['user_id']
#     del login_session['facebook_id']
#
#     return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)