# Assignment 11
## Solution to Mission Mars

This solution provides a web-based dashboard of Mars-related news and information,
by scarping the following:
* NASA Mars News Site at https://mars.nasa.gov/news/
* JPL Mars Space Images (Featured Image) at https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
* Mars Weather twitter account at https://twitter.com/marswxreport?lang=en
* Mars Facts webpage at http://space-facts.com/mars/
* USGS Astrogeology site (high resolution images of Mar's hemispheres) at https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

Upon running mars_app.py (Python script) the dashboard can be accessed at http://localhost:5000/.

Note1: mongod needs to be running (and listening on port 27017) prior to executing mars_app.py since data obtained from various web sites are stored in a Mongo database--called planets, in the mars collection.

Note2: chromedriver.exe needs to be present in the same directory/folder where mars_app.py and scrape_mars.py scripts reside. 

The root Flask route (/) retrieves the first record in this Mongo database and renders the data within this record using the HTML template file (index_tmplt.html) under the templates directory/folder.

The scrape Flask route (/scrape), accessed via the Scrape New Data button at the top of dashboard, scrapes all the web sites listed above to obtain current info, and stores this info (as a Pythin dictionary) in the Mongo database described above.
