"""Create example database model class."""
from events_app import db


class User(db.Model):
    """Class User represents the user table in our SQL database."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    avatar = db.Column(
        db.String(30),
        nullable=False,
        default="lucifer.jpeg",
    )
