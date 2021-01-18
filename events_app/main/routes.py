"""Import packages and modules."""
import os
import requests
from flask import Blueprint, request, render_template, redirect, url_for
from datetime import date, datetime
from pprint import PrettyPrinter
from events_app.main.utils import get_holiday_data

from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint("main", __name__)

##########################################
#            App setup                   #
##########################################

# Define global variables (stored here for now)

# This initializes our PrettyPrinter object:

pp = PrettyPrinter(indent=4)

today = date.today()
# Now, let's just get the month as a number:
month = today.strftime("%m")
# Now, let's get the current year:
year = today.strftime("%Y")
# I also want to know the name of the month for later:
month_name = today.strftime("%B")


##########################################
#           Routes                       #
##########################################


@main.route("/")
def homepage():
    """
    Return template for home.

    Show upcoming events to users!
    """
    event = Event.query.all()
    return render_template("index.html", event=event)


@main.route("/add-event", methods=["POST"])
def add_event():
    """Add event to Event table."""
    # Notice I've wrapped this in a try except block.
    # Dates are picky - watch your formatting!
    try:
        # TODO:
        # Access our values from our event form
        # and use these to instantiate our Event model
        # Make sure we call db.session.add() on our new object!
        # HINT: don't forget to also call db.session.commit() to commit changes

        title = request.form.get('title')
        description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')

        event = Event(title=title, description=description,
                      date=date, time=time)
        db.session.add(guest)
        db.session.commit()
        return redirect(url_for("main.homepage"))
    except ValueError:
        return redirect(url_for("main.homepage"))


@main.route("/delete-event/<event_id>", methods=["POST"])
def delete_event(event_id):
    """
    Delete event.

    Delete event after the date it occurs automatically.
    """
    # TODO: write code to delete the specific event.
    # HINT: You'll have to run a query for the event first.
    return redirect(url_for("main.homepage"))


@main.route("/edit-event/<event_id>", methods=["POST"])
def edit_event(event_id):
    """Edit events."""
    event = Event.query.filter_by(id=event_id).first()

    # TODO: access our form values and write the code
    # HINT: You'll be updating an object - you know how to do this!
    # Just don't forget to commit your changes :)
    return redirect(url_for("main.homepage"))


@main.route("/holidays")
def about_page():
    """Show user event information."""
    url = "https://calendarific.com/api/v2/holidays"

    params = {
        "api_key": os.getenv("API_KEY"),
        "country": "US",
        "year": year,
        "month": month,
    }

    result_json = requests.get(url, params=params).json()
    # You can use pp.pprint() to print out your result -
    # This will help you know how to access different items if you get stuck
    # pp.pprint(result_json)

    # Call get_holiday_data to return our list item

    holidays = get_holiday_data(result_json)

    context = {"holidays": holidays, "month": month_name}

    return render_template("about.html", **context)


@main.route("/guests", methods=["GET", "POST"])
def show_guests():
    """
    Show guests that have RSVP'd.

    Add guests to RSVP list if method is POST.
    """
    if request.method == "GET":
        # TODO: We're not going to be able to pass guests to our
        # template - Why do you think this is?
        # If we want it to show up nicely, we need to access guests for
        # each event and not the other way around. Write the query
        # To make this happen!
        return render_template("guests.html")
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        plus_one = request.form.get("plus-one")
        phone = request.form.get("phone")
        event_id = request.form.get("event_id")

        # TODO: Change this code so that we're adding
        # A guest object to our database rather than to a list.

        return render_template("guests.html", events=events)


@main.route("/rsvp")
def rsvp_guest():
    """Show form for guests to RSVP for events."""
    # TODO: We're going to want to pass our events
    # to our rsvp template so that we have separate RSVP forms for each
    # event.
    return render_template("rsvp.html")
