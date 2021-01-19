"""Import packages and modules for initializing our app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from events_app.config import Config

# Some of this undoubtedly looks a little foreign right now.
# That's okay! We'll learn about Flask blueprints & packages
# later.

app = Flask(__name__)
app.config.from_object(Config)

# to initialize your database taking our app as its parameter.

db = SQLAlchemy(app)
from events_app.main.routes import main
app.register_blueprint(main)
