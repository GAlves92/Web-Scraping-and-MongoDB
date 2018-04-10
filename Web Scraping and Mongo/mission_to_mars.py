from splinter import Browser
import requests
from bs4 import BeautifulSoup
from sys import platform
import time
import pandas

def init_browser():
    if platform == "darwin":
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    else:
        executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=True)

def scrape_url():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204%3A19&blank_scope=Latest'

    browser = init_browser()
    four_pics = []
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    news_title = soup.find_all("div", class_="content_title")[0]
    
    news_title = news_title.text.strip()

    time.sleep(3)

    news_p = soup.find_all("div", class_="article_teaser_body")[0]
    
    news_p = news_p.text.strip()

    browser.quit()
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    pics = soup.find('article', class_='carousel_item')
    full_pic = pics('a', class_='button fancybox')
    time.sleep(2)
    
    browser.click_link_by_id("full_image")
    time.sleep(1)
    browser.click_link_by_partial_text("more info")

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('figure', class_="lede")
    img_url = img.find("a")['href']
    featured_image_url = (img.find("img", class_="main_image")['src'])
    featured_image_link = 'https://www.jpl.nasa.gov' + featured_image_url
   
    browser.quit()
    
    url = 'https://twitter.com/marswxreport?lang=en'

    browser = init_browser()
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    weather_mars = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0]
    weather_mars = weather_mars.text.strip()
    
    browser.quit()
    
    url = 'https://space-facts.com/mars/'
    
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_facts = soup.find_all("table")[0]
    pandas.read_html('https://space-facts.com/mars/')

    mars_facts_table = pandas.read_html('https://space-facts.com/mars/')
    
    browser.quit()
        
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser = init_browser()
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    result = BeautifulSoup(html, 'html.parser')
    results = result.find_all('div', class_="result-list")
    new_link = results[0].find_all('a', class_='itemLink product-item')[0]['href']
    link_names = 'https://astrogeology.usgs.gov' + new_link
    
    browser.visit(link_names)
    html = browser.html
    result = BeautifulSoup(html, 'html.parser')
    link_ready = result.find_all('div', class_="downloads")[0].find('a')['href']
    browser.back()
    browser.quit()
 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser = init_browser()
    mars = {}
    browser.visit(url)
    html = browser.html
    result = BeautifulSoup(html, 'html.parser')
    results = result.find_all('div', class_="description")
       
    for result in results:
        title = result.find('a', class_="itemLink product-item").find('h3').text
        new_link = result.find_all('a', class_='itemLink product-item')[0]['href']
        link_names = 'https://astrogeology.usgs.gov' + new_link
        browser.visit(link_names)
        html = browser.html
        result = BeautifulSoup(html, 'html.parser')
        link_ready = result.find_all('div', class_="downloads")[0].find('a')['href']
        browser.back()      
        four_pics.append(title)
        four_pics.append(link_ready)   
        
    mars['news_p'] = news_p
    mars['featured_image_link'] = featured_image_link
    mars['news_title'] = news_title
    mars['weather_mars'] = weather_mars
    mars['mars_facts_table'] = mars_facts_table 
    mars['link_ready'] = link_ready
    mars['title'] = title
    four_pics.append(mars)

    browser.quit()
    return [four_pics]
    