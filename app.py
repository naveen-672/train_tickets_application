from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = "train_booking_secret_key_2024"

# Sample train data (static)
TRAINS = [
    {
        "id": "12951",
        "name": "Rajdhani Express",
        "from": "Mumbai",
        "to": "Delhi",
        "departure": "16:35",
        "arrival": "08:15",
        "duration": "15h 40m",
        "price_sl": 1200,
        "price_3a": 2100,
        "price_2a": 3050,
        "price_1a": 5200,
        "rating": 4.5,
    },
    {
        "id": "12009",
        "name": "Shatabdi Express",
        "from": "Mumbai",
        "to": "Pune",
        "departure": "06:25",
        "arrival": "09:35",
        "duration": "3h 10m",
        "price_sl": 400,
        "price_3a": 850,
        "price_2a": 1250,
        "price_1a": 2000,
        "rating": 4.7,
    },
    {
        "id": "12621",
        "name": "Tamil Nadu Express",
        "from": "Delhi",
        "to": "Chennai",
        "departure": "22:30",
        "arrival": "07:40",
        "duration": "33h 10m",
        "price_sl": 950,
        "price_3a": 1800,
        "price_2a": 2600,
        "price_1a": 4400,
        "rating": 4.3,
    },
    {
        "id": "12301",
        "name": "Howrah Rajdhani",
        "from": "Delhi",
        "to": "Kolkata",
        "departure": "16:55",
        "arrival": "09:55",
        "duration": "17h 00m",
        "price_sl": 1100,
        "price_3a": 2050,
        "price_2a": 2950,
        "price_1a": 5000,
        "rating": 4.6,
    },
    {
        "id": "12626",
        "name": "Kerala Express",
        "from": "Delhi",
        "to": "Trivandrum",
        "departure": "11:25",
        "arrival": "12:15",
        "duration": "48h 50m",
        "price_sl": 1300,
        "price_3a": 2450,
        "price_2a": 3500,
        "price_1a": 5900,
        "rating": 4.2,
    },
    {
        "id": "12002",
        "name": "Bhopal Shatabdi",
        "from": "Delhi",
        "to": "Bhopal",
        "departure": "06:00",
        "arrival": "14:05",
        "duration": "8h 05m",
        "price_sl": 650,
        "price_3a": 1250,
        "price_2a": 1800,
        "price_1a": 3100,
        "rating": 4.4,
    },
    {
        "id": "12723",
        "name": "Telangana Express",
        "from": "Hyderabad",
        "to": "Delhi",
        "departure": "06:25",
        "arrival": "08:00",
        "duration": "25h 35m",
        "price_sl": 900,
        "price_3a": 1700,
        "price_2a": 2500,
        "price_1a": 4200,
        "rating": 4.1,
    },
    {
        "id": "16525",
        "name": "Island Express",
        "from": "Bangalore",
        "to": "Kanyakumari",
        "departure": "08:00",
        "arrival": "21:30",
        "duration": "13h 30m",
        "price_sl": 550,
        "price_3a": 1100,
        "price_2a": 1600,
        "price_1a": 2800,
        "rating": 4.0,
    },
    {
        "id": "12259",
        "name": "Sealdah Duronto",
        "from": "Kolkata",
        "to": "Delhi",
        "departure": "20:00",
        "arrival": "12:00",
        "duration": "16h 00m",
        "price_sl": 1050,
        "price_3a": 1950,
        "price_2a": 2850,
        "price_1a": 4800,
        "rating": 4.5,
    },
    {
        "id": "12841",
        "name": "Coromandel Express",
        "from": "Kolkata",
        "to": "Chennai",
        "departure": "14:50",
        "arrival": "17:40",
        "duration": "26h 50m",
        "price_sl": 850,
        "price_3a": 1600,
        "price_2a": 2350,
        "price_1a": 4000,
        "rating": 4.3,
    },
]

CITIES = sorted(set([t["from"] for t in TRAINS] + [t["to"] for t in TRAINS]))


@app.route("/")
def index():
    return render_template("index.html", cities=CITIES, trains=TRAINS[:3])


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        from_city = request.form.get("from_city")
        to_city = request.form.get("to_city")
        journey_date = request.form.get("journey_date")
    else:
        from_city = request.args.get("from_city", "")
        to_city = request.args.get("to_city", "")
        journey_date = request.args.get("journey_date", "")

    results = [
        t for t in TRAINS
        if (not from_city or t["from"].lower() == from_city.lower())
        and (not to_city or t["to"].lower() == to_city.lower())
    ]

    if not from_city and not to_city:
        results = TRAINS

    return render_template(
        "search.html",
        trains=results,
        cities=CITIES,
        from_city=from_city,
        to_city=to_city,
        journey_date=journey_date,
    )


@app.route("/book/<train_id>", methods=["GET", "POST"])
def book(train_id):
    train = next((t for t in TRAINS if t["id"] == train_id), None)
    if not train:
        return redirect(url_for("index"))

    if request.method == "POST":
        passenger_name = request.form.get("passenger_name")
        passenger_age = request.form.get("passenger_age")
        passenger_gender = request.form.get("passenger_gender")
        coach_class = request.form.get("coach_class", "SL")
        journey_date = request.form.get("journey_date", "")

        price_map = {
            "SL": train["price_sl"],
            "3A": train["price_3a"],
            "2A": train["price_2a"],
            "1A": train["price_1a"],
        }
        fare = price_map.get(coach_class, train["price_sl"])
        pnr = "PNR" + str(random.randint(1000000, 9999999))

        booking = {
            "pnr": pnr,
            "train_id": train["id"],
            "train_name": train["name"],
            "from": train["from"],
            "to": train["to"],
            "departure": train["departure"],
            "arrival": train["arrival"],
            "journey_date": journey_date,
            "passenger_name": passenger_name,
            "passenger_age": passenger_age,
            "passenger_gender": passenger_gender,
            "coach_class": coach_class,
            "fare": fare,
        }
        session["booking"] = booking
        return redirect(url_for("confirmation"))

    journey_date = request.args.get("journey_date", "")
    return render_template("booking.html", train=train, journey_date=journey_date)


@app.route("/confirmation")
def confirmation():
    booking = session.get("booking")
    if not booking:
        return redirect(url_for("index"))
    return render_template("confirmation.html", booking=booking)


@app.route("/trains")
def all_trains():
    return render_template("search.html", trains=TRAINS, cities=CITIES,
                           from_city="", to_city="", journey_date="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
