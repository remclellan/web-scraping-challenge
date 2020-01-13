#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# Using BeautifulSoup, Pandas, and Requests/Splinter, will perform a web scraping of the following:
# - [NASA Mars News Sites](https://mars.nasa.gov/news/) to collect the latest News Title and Paragraph Text and store for later use;
# - [JPL Mars Space Images](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) to collect the full size .jpg of the featured image;
# - [Mars Weather Twitter](https://twitter.com/marswxreport?lang=en) to scrape the latest Mars weather tweets from the page;
# - [Mars Facts page](https://space-facts.com/mars/) - using Pandas to scrape table containing facts about the planet such as Diameter, Mass, etc.; and
# - [USGS Astrology Site](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to collect high resolution impages for each of Mar's hemispheres

# ### Import dependencies

# In[30]:


from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin
import pandas as pd


# ### Setup Splinter configuration variables

# In[2]:


# use if os join doesn't work: '../resources/chromedriver.exe'
executable_path = {'executable_path': os.path.join("..","Resources","chromedriver.exe")}
browser = Browser('chrome', **executable_path, headless=False)


# ### Define variables for each URL to scrape

# In[3]:


url_nasa = 'https://mars.nasa.gov/news/'
url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
url_weather = 'https://twitter.com/marswxreport?lang=en'
url_facts = 'https://space-facts.com/mars/'
url_USGS = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# ### NASA Mars News

# ##### Pass through nasa url variable to browser to visit site and establish variables to capture underlying HTML and pass back to BeautifulSoup

# In[4]:


browser.visit(url_nasa)


# In[5]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# ##### Establish variables to capture first news title and associated p tags for latest news info

# In[6]:


div = soup.find('div', attrs={'class': 'content_title'})
news_title = div.find('a').text


# In[7]:


news_p = soup.find('div', attrs={'class': 'article_teaser_body'}).text


# In[8]:


print(news_title)
print(news_p)


# ### JPL Mars Featured Image

# ##### Pass through jpl url variable to browser to visit site and establish variables to capture underlying HTML and pass back to BeautifulSoup

# In[60]:


browser.visit(url_jpl)


# In[61]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# ##### Click through full size image button feature image, expand image to get to img src and then establish variable to capture full size Feature Image partial path and use urljoin to merge partial to absolute path.

# In[63]:


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


# In[64]:


print(featured_image_url)


# ### Mars Weather

# ##### Pass through weather url variable to browser to visit site and establish variables to capture underlying HTML and pass back to BeautifulSoup

# In[34]:


browser.visit(url_weather)


# In[35]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# ##### Establish variables to capture first news title and associated p tags for latest news info

# In[36]:


div = soup.find('div', attrs={'class': 'js-tweet-text-container'})
mars_weather = div.find('p').text


# In[37]:


print(mars_weather)


# ### Mars Facts

# ##### Using Pandas read_html function using the facts url variable to brower to visit site and capture table

# In[38]:


tables = pd.read_html(url_facts)
len(tables)


# In[39]:


df = tables[0]
df.columns = ['Metric', 'Value']
df.head()


# ##### Using Pandas to_html function convert to HTML table string

# In[43]:


html_table = df.to_html()
html_table


# In[44]:


html_table.replace('\n', '')


# In[45]:


df.to_html('table.html')


# ### Mars Hemispheres using USGS Astrology Site

# ##### Pass through USGS url variable to browser to visit site and establish variables to capture underlying HTML and pass back to BeautifulSoup

# In[149]:


browser.visit(url_USGS)


# In[150]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# ##### Using a for loop, identify the div class containing the hemisphere data and link to image download and store as dictionary

# In[167]:


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


# In[168]:


print(hemisphere_image_urls)


# In[ ]:




