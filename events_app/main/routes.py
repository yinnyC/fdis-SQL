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
    events = Event.query.all()
    return render_template("index.html", events=events)


@main.route("/add-event", methods=["POST"])
def add_event():
    """Add event to Event table."""
    try:
        new_event_title = request.form.get("title")
        new_event_description = request.form.get("description")
        new_event_date = datetime.strptime(
            request.form.get("date"), "%m-%d-%Y"
        )
        new_event_time = datetime.strptime(request.form.get("time"), "%H:%M")

        event = Event(
            title=new_event_title,
            description=new_event_description,
            date=new_event_date,
            time=new_event_time,
        )

        db.session.add(event)
        db.session.commit()
        return redirect(url_for("main.homepage"))
    except ValueError:
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
        return render_template("guests.html")
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        plus_one = request.form.get("plus-one")
        phone = request.form.get("phone")
        # guest_list.append(Guest(name, email, plus_one, phone))
        return render_template("guests.html")


@main.route("/rsvp")
def rsvp_guest():
    """Show form for guests to RSVP for events."""
    return render_template("rsvp.html")
