InterStellar Travel Services Web Application version 0.3
An experimental application.

Udacity Project 3

Victor Asselta
vasselta@gmail.com


What is it?
______________________________________________________________________________________________________

Interstellar Travel Services, or ITS, is a Travel Agent software simulator with an included simple game.
The player takes the roll of a galactic travel agent.

The player can create view, create, delete, update, and "book travel" for their clients and some
default clients. Most player functions are limited to that particular player although, any agent
can book travel for another agent.

The agent testing allows for pretend advancement. The feature is not fully implemented however, players can
play the tests and see canned results.



Requirements
______________________________________________________________________________________________________

** Important **
Requires 0.9 version of Flask.
Requires 0.8.3 version of werkzeug

The latest version of Flask will break the login and logout functions.

A fully up to date web browser with javascript enabled.
This is a student assignment and is not fully tested in all environments.

The sqlite database should be present in the home directory.
Prior to first run you can execute via python the ITS_database_setup.py file to create the database and
the ITS_database_populate.py to populate it.

After the database is in existence, and populated, run the ITS_main.py file to launch the web server.
Open your web browser and proceed to "localhost:5000" to view the app.

A google+ account is necessary to gain access to the app.
You will have to accept basic app access to basic Google+ information such as name, email, and image.

For JSON API calls you may enter the following urls:

    For travel destinations: localhost:5000/destinations/JSON

    For methods of travel: localhost:5000/travel_method/JSON

    For menu items: localhost:5000/menu/JSON

FOR XML API call you may enter the following urls(may require view page source):

    For travel destinations: localhost:5000/destinations/XML

    For methods of travel: localhost:5000/travel_method/XML

    For menu items: localhost:5000/menu/XML



File Structure
______________________________________________________________________________________________________

ITS
|
|____ templates
|        |
|        |_ agent_choose.html
|        |_ agent_home.html
|        |_ clients.html
|        |_ create_trip.html
|        |_ delete_client.html
|        |_ login.html
|        |_ master2.html
|        |_ results.html
|
|____ static
        |
        |_images
        |    |__ eyes.gif
        |    |__ ITS_3d.gif
        |    |__ octo.gif
        |    |__ robo2.gif
        |    |__ space2.gif
        |    |__ star.gif
        |    |__ weirdo.jpg
        |
        |__ upload_images
        |
        |
        ITS_script.js
        style2.css
        typed.js



Known bugs and possible upgrades
______________________________________________________________________________________________________

A number of items have been fixed or added in this release.
1) Updated google+ api url from https://www.googleapis.com/oauth2/v1/userinfo
    to https://www.googleapis.com/plus/v1/people/me and updated requests.
    The old url, and corresponding keys, did not allow for returned user email.

2) Updated this document, per reviewer request. To reflect proper flask version.
    I did attempt to update code to work with latest version of flask,
    per reviewer suggestion, but the change to json broke other objects.
    I'll have to spend more time to figure out what went wrong.

3) Fixed the upload image function.

4) Added XML response.


First Submission for reference:
This is a complicated app with allot of features.

The biggest issues I have faced so far have been Google+ and Facebook authorization.

I removed facebook authorization as it has changed recently and no longer furnishes a user's email.
I'll have to spend some more time with the API and figure out what changes. I did recently notice
some posts on the forums.

I'vs also found that I am having trouble retrieving a users email with Googleplus.
I have several accounts and it all seems to behave the same. I've had to enact alternatives in the event
fetching the email key fails.

Image uploading is present, however buggy.

The agent testing game will eventually fully implement tracking. The mechanism exists but falls down
somewhere I have yet to identify. Various mechanisms related to this game feature, displaying an agent's
status with stars, exist yet cannot be fully implemented until tracking is working.

The interface is a work in progress. This was secondary to the rest of the assignment so it received the
least attention.

Flask was also another point of contention. At several time throughout development flask would no longer
serve up post requests. I don't know if it's flask exactly or some python webserver mechanism but a total
reboot would solve the problem.