from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin
import pandas as pd


url_nasa = 'https://mars.nasa.gov/news/'
url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
url_weather = 'https://twitter.com/marswxreport?lang=en'
url_facts = 'https://space-facts.com/mars/'
url_USGS = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

executable_path = {'executable_path': os.path.join("..","Resources","chromedriver.exe")}
browser = Browser('chrome', **executable_path, headless=False)    

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
        hemi_partialpath ="/#"
        
    hemisphere_image["img_url"] = urljoin(url_USGS, hemi_partialpath)
    browser.visit(url_USGS)
    
    hemisphere_image_urls.append(hemisphere_image)
        
print(hemisphere_image_urls)
browser.quit()