"""Create Guest ad Events database model class."""
from events_app import db
from sqlalchemy.orm import backref


class Guest(db.Model):
    """Class Guest represents the Guest table in our SQL database."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    plus_one = db.Column(db.String(55), nullable=True)
    phone = db.Column(db.String(15), nullable=False)
    events_attending = db.relationship("Event", secondary="guest_event_link")

    def __repr__(self):
        """Define how we want this to look when printed."""
        return self.name


class Event(db.Model):
    """Class Event represents the Event table in our SQL database."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(90), nullable=False)
    description = db.Column(db.String(140), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    guests = db.relationship("Guest", secondary="guest_event_link")

    def __repr__(self):
        """Define how we want this to look when printed."""
        return self.title, self.description


class GuestEventLink(db.Model):
    """Joining table for guests & events."""

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guest.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    event = db.relationship(
        "Event", backref=backref("link", cascade="all, delete-orphan")
    )
    guest = db.relationship(
        "Guest", backref=backref("link", cascade="all, delete-orphan")
    )
