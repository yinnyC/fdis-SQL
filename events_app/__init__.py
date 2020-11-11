"""Import packages and modules for initializing our app."""
from flask import Flask

# TODO: import SQLALchemy
from events_app.config import Config

# Some of this undoubtedly looks a little foreign right now.
# That's okay! We'll learn about Flask blueprints & packages
# later.

app = Flask(__name__)
# TODO: add your config statement so you can access environment variables!


# TODO: Use the instructions in your assignment
# to initialize your database taking our app as its parameter.


from events_app.main.routes import main

app.register_blueprint(main)

# TODO: add your statement to create database tables
