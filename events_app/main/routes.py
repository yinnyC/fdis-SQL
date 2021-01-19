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
    return render_template("index.html", events=event)


@main.route("/add-event", methods=["POST"])
def add_event():
    """Add event to Event table."""
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        time = datetime.strptime(request.form.get('time'), '%H:%M')

        event = Event(title=title, description=description,
                      date=date, time=time)
        db.session.add(event)
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
    event = Event.query.filter_by(id=event_id).first()
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("main.homepage"))


@main.route("/edit-event/<event_id>", methods=["POST"])
def edit_event(event_id):
    """Edit events."""
    event = Event.query.filter_by(id=event_id).first()
    event.title = request.form.get('title')
    event.description = request.form.get('description')
    event.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
    event.time = datetime.strptime(request.form.get('time'), '%H:%M')
    db.session.commit()
    return redirect(url_for("main.homepage"))


@main.route("/holidays")
def about_page():
    """Show user event information."""
    url = "https://calendarific.com/api/v2/holidays"
    print(os.getenv("API_KEY"))
    params = {
        "api_key": os.getenv("API_KEY"),
        "country": "US",
        "year": year,
        "month": month,
    }

    result_json = requests.get(url, params=params).json()
    # pp.pprint(result_json)
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

        return render_template("guests.html")
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        plus_one = request.form.get("plus-one")
        phone = request.form.get("phone")
        event_id = request.form.get("event_id")

        event = Event.query.filter_by(id=event_id).first()

        new_guest = Guest(name=name, email=email,
                          plus_one=plus_one, phone=phone, events_attending=[])
        event.guests.append(new_guest)
        db.session.add(new_guest)
        db.session.commit()
        events = Event.query.all()
        return render_template("guests.html", events=events)


@main.route("/rsvp")
def rsvp_guest():
    """Show form for guests to RSVP for events."""
    event = Event.query.all()
    return render_template("rsvp.html", events=event)
