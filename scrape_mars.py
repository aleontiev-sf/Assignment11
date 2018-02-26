# This Python script contains a function called scrape() that is used by the
#   root (/) Flask route conained in mars_app.py.
#
# The purpose of this function is to scrape Mars related information from a number
#   of websites, aggreate these data into a single dictionary and store it into a
#   Mongo database.
#
# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pymongo

def scrape():
    # Scrape the NASA Mars News Site for the latest news title and paragraph
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('div', class_='content_title')
    result = soup.find('div', class_='features')
    news_title = result.find('div', class_="content_title").a.text
    news_p = result.find('div', class_='rollover_description_inner').text.strip()
    news_url = result.find('div', class_="content_title").a['href']
    news_url = 'https://mars.nasa.gov' + news_url

    # Scrape the JPL's Featured Space Image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find('a', class_='button fancybox')
    featured_image_url = 'https://www.jpl.nasa.gov' + result['data-fancybox-href']

    # Scrape the Mars Weather twitter account
    url= 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = result.text

    # Scrape the Mars Facts webpage
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    facts = [ td.text for td in soup.table('td') ]
    mars_facts = []
    for i in range(0,len(facts),2):
        mars_facts.append({facts[i] : facts[i+1]})

    # Scrape the USGS Astrogeology site for high resolution images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('a', class_='itemLink product-item')
    hemispher_image_urls = []
    for i in range(0,8,2):
        new_url = 'https://astrogeology.usgs.gov' + results[i]['href']
        browser.visit(new_url)
        html2 = browser.html
        soup2 = BeautifulSoup(html2, 'html.parser')
        hemisphere_image = soup2.find_all('a')
        hemisphere_image_url = hemisphere_image[41]['href']
        hemisphere_title = soup2.find('h2').contents[0]
        hemispher_image_urls.append({'title' : hemisphere_title, 'img_url' : hemisphere_image_url})
    # Aggregate all the data above into a single dictionary and return to the caller
    mars_data = {
        'news_title' : news_title,
        'news_p' : news_p,
        'news_url' : news_url,
        'featured_image' : featured_image_url,
        'weather' : mars_weather,
        'facts' : mars_facts,
        'image1' : hemispher_image_urls[0],
        'image2' : hemispher_image_urls[1],
        'image3' : hemispher_image_urls[2],
        'image4' : hemispher_image_urls[3]
    }
    return mars_data
