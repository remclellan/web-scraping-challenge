from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin
import pandas as pd

def init_browser():
    executable_path = {'executable_path': os.path.join("..","Resources","chromedriver.exe")}
    return browser = Browser('chrome', **executable_path, headless=False)

def scrape_mars():
    browser = init_browser()

    # define variables for each URL to scrape
    url_nasa = 'https://mars.nasa.gov/news/'
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    url_facts = 'https://space-facts.com/mars/'
    url_USGS = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # NASA Mars News
    browser.visit(url_nasa)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', attrs={'class': 'content_title'})
    news_title = div.find('a').text
    news_p = soup.find('div', attrs={'class': 'article_teaser_body'}).text

    # JPL Mars Featured Image
    browser.visit(url_jpl)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.click_link_by_id('full_image')
    try:
        expand = browser.find_by_css('a.fancybox-expand')
        expand.click()
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        img_partialpath = image_soup.find('img', class_='fancybox-image')['src']
    except ElementNotVisibleException:
        print(e)
        
    featured_image_url = urljoin(url_jpl, img_partialpath)

    # Mars Weather
    browser.visit(url_weather)    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', attrs={'class': 'js-tweet-text-container'})
    mars_weather = div.find('p').text

    # Mars Facts
    tables = pd.read_html(url_facts)
    df = tables[0]
    df.columns = ['Metric', 'Value']
    df.head()
    html_table = df.to_html()
    html_table

    # Mars Hemispheres
    browser.visit(url_USGS)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []

    for i in range (0,4):
        hemisphere_image = {}
        hemisphere = soup.find_all('h3')[i].text.strip('Enhanced')
        hemisphere_image["title"] = hemisphere.strip()
    
        link_name = soup.find_all('h3')[i].text.strip('Hemisphere Enhanced')
    
        try:
            browser.click_link_by_partial_text(link_name)
            browser.click_link_by_partial_text('Open')
            hemi_html = browser.html
            hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
            hemisphere_img = hemi_soup.body.find('img', class_='wide-image')
            hemi_partialpath = hemisphere_img['src']
        except:
            print("nope")
            hemi_partialpath ="/#"
        
        hemisphere_image["img_url"] = urljoin(url_USGS, hemi_partialpath)
        browser.visit(url_USGS)
    
        hemisphere_image_urls.append(hemisphere_image)

    browser.quit()

    return news_title, news_p, featured_image_url, mars_weather, html_table, hemisphere_image_urls




