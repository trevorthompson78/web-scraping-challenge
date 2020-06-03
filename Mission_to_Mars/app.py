from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrapemars

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_data")

@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    # mars = mongo.db.mars
    mars_data = scrapemars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

