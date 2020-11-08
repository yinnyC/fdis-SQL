"""
Initialize your Flask app. This is what will run your server.

Don't forget to install your dependencies from requirements.txt!
This is a doc string! It's a special kind of comment that is expected
in Python files. Usually, you use this at the top of your code and in
every function & class to explain what the code does.
"""
import os
import requests
from flask import Flask, request, render_template, url_for
from guest import Guest
from datetime import datetime, date
from pprint import PrettyPrinter

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

# Define global variables (stored here for now)

guest_list = []

# This initializes our PrettyPrinter object:

pp = PrettyPrinter(indent=4)

today = date.today()
# Now, let's just get the month as a number:
month = today.strftime("%m")
# Now, let's get the current year:
year = today.strftime("%Y")


##########################################
#           # Helper functions           #
##########################################


def get_holiday_data(result):
    """Loop through our JSON results and get only the information we need."""
    data = []
    for holiday in result["response"]["holidays"]:
        new_holiday = {
            "name": holiday["name"],
            "description": holiday["description"],
            "date": holiday["date"]["iso"],
        }
        data.append(new_holiday)
    return data


##########################################
#           Routes                       #
##########################################


@app.route("/")
def homepage():
    """Return template for home."""
    return render_template("index.html")


@app.route("/about")
def about_page():
    """Show user event information."""
    url = "https://calendarific.com/api/v2/holidays"

    params = {
        "api_key": API_KEY,
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

    return render_template("about.html", holidays=holidays)


@app.route("/guests", methods=["GET", "POST"])
def show_guests():
    """
    Show guests that have RSVP'd.

    Add guests to RSVP list if method is POST.
    """
    if request.method == "GET":
        return render_template("guests.html", guests=guest_list)
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        plus_one = request.form.get("plus-one")
        phone = request.form.get("phone")
        guest_list.append(Guest(name, email, plus_one, phone))
        return render_template("guests.html", guests=guest_list)


@app.route("/rsvp")
def rsvp_guest():
    """Show form for guests to RSVP for events."""
    return render_template("rsvp.html")


if __name__ == "__main__":
    app.run(debug=True)
