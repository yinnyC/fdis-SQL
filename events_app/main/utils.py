"""Helper functions for app."""


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
