import flask
import requests
from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
db = SQLAlchemy(app)
class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)

API_KEY = "065f489cb0f1a39404103d9d561f3f4b"


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    responses = requests.get(url)
    return responses.json()

@app.route("/", methods = ["GET","POST"])
def home():

    if request.method == "POST":
        city = request.form["city"]
        data = get_weather(city)

        new_search = Search(city=city)
        db.session.add(new_search)
        db.session.commit()

        history = Search.query.all()

        return render_template("home.html", weather=data, history=history)

    history = Search.query.all()
    return render_template("home.html", history=history)
  # runs on GET, shows empty form

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
