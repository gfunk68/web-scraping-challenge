import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser



def scrape():

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text,'html.parser')
    title = soup.find('div', class_="content_title").text
    teaser = soup.find('div', class_="rollover_description_inner").text
    executable_path={'executable_path':'chromedriver.exe'}
    browser=Browser('chrome',**executable_path,headless=False)
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    # JPL Mars Space Images - Featured Image
    browser.click_link_by_partial_text('FULL IMAGE')
    html = browser.html
    img_soup = bs(html,'html.parser')
    image_url = img_soup.find('a', class_='fancybox')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov'+ image_url

    # Mars Weather
    twitterurl = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitterurl)
    twitsoup = bs(response.text, 'html.parser')
    mars_weather = twitsoup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # Mars Facts
    facts = pd.read_html('https://space-facts.com/mars/')
    mars_facts_df = facts[0]
    mars_facts_html = mars_facts_df.to_html()

    # Mars Hemispheres
    hemisphere_image_urls = [
        {'title': 'Cerberus Hemisphere', "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
        {'title': 'Schiaparelli Hemisphere', "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
        {'title': 'Syrtis Major Hemisphere', "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
        {'title': 'Valles Marineris Hemisphere', "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"}
    ]

    scraped_dict = {
        'mars_facts_html' : mars_facts_html, 
        'title': title, 
        'teaser' : teaser, 
        'hemisphere_image_urls':hemisphere_image_urls,
        'featured_image_url':featured_image_url,
        'mars_weather': mars_weather
    }

    return scraped_dict
