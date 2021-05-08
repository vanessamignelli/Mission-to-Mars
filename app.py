#import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo 
import scraping

# set up flask app
app = Flask(__name__)

# use flask_pymongo to set up mongo connection
# connect app to mongo using a URI (uniform resource identifier)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for our html page
@app.route('/')

# use pymongo to find the mars collection in the db
# return an html template using an index.html file
# mars = mars means use mars collection in mongodb
# function links visual representation of work to web app
def index():
    mars = mongo.db.mars.find_one()
    #print(mars)
    return render_template("index.html", mars=mars)

# set up scraping route
# button of web app - scrape updated data when told from homepage
@app.route('/scrape')

#access data and scrape new data using using scraping.py script
# mars_data - create variable to hold newly scraped data (reference scrape_all func in scraping.py)
# update database using .update()
# .update(query_parameter, data, options)
# {} - insert data by adding empty JSON object
# mars_data - use data stored in this variable
# upsert=True - create a new document if one doesn't already exist
# return redirect after successfully scraping
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    #print(mars_data)
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run()