# This Python script contains Flask routes for the Mission to Mars dashboard.
#
# The root (/) route retrieves data from a Mongo database and redners the
#   information using a Jinja HTML template (index_tmplt.html).
#
# The scrape (/scrape) route scrapes data from various web sites using the 
#   scrape() function which is contained in scrape_mars.py module.
#
# Dependencies
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.planets

# This route defines the function which retrieves a record from the mars collection
#   in a Mongo database called planets.  Data in this record are then disaggregted
#   and passed to a Jinja HTML template to render.
@app.route('/')
def index():
    results = db.mars.find()
    facts = results[0]['facts']
    mars_facts = {}
    # The following loop converts the Mars facts dictionary to a list of dictionaries
    # each containing the data within a row of the Mars facts table.
    for key, value in enumerate(facts):
        for k, v in value.items():
            mars_facts[k] = v
    return render_template('index_tmplt.html', 
      news_title=results[0]['news_title'],
      news_p = results[0]['news_p'],
      news_url = results[0]['news_url'],
      featured_image_url=results[0]['featured_image'],
      mars_weather=results[0]['weather'],
      facts = mars_facts,
      image1 = results[0]['image1'],
      image2 = results[0]['image2'],
      image3 = results[0]['image3'],
      image4 = results[0]['image4']
    )

# This route defines a function that calls the scrape() function, which in turn
#   scrapes data from various websites and returns them in a single dictionary.
#
# This function then stores the dictionary into the mars collection, and issues a
#   redirect call, resulting in an invokation of the root route (defined above) with
#   the net result of the latest scraped info being rendered.
@app.route('/scrape')
def scrape():
    updated_data = scrape_mars.scrape()
    mars_collection = db.mars
    mars_collection.update({}, updated_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=False)
