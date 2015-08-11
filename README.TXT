InterStellar Travel Services Web Application version 0.2
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



Know bugs and possible upgrades
______________________________________________________________________________________________________

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