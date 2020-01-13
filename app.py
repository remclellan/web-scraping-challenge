from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import os

# From the separate python file in this directory, we'll import the code that is used to scrape various sites for Mars data
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

# identify the collection and drop any existing data for this demonstration
mars_info = mongo.db.mars_info
mars_info.drop()

# Render the index.html page with the Mars data in our database. 
@app.route("/")
def index():
    mars_results = mars_info.find_one()
    return render_template("index.html", mars_results=mars_results)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scrape():

    # scrape_mars.scrape() is a custom function that we've defined in the scrape_mars.py file within this directory
    mars_info
    mars_data = scrape_mars.scrape_mars()
    mars_info.update({},mars_data, upsert=True)
    
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)