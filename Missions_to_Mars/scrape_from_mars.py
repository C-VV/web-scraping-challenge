from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests

#initializing browser 
def init_browser():

    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    ##### NASA Mars News ####
    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    nasa_html = browser.html
    # Create BeautifulSoup object; parse with 'html'
    soup = BeautifulSoup(nasa_html,'html.parser')


    u_list = soup.find("ul", class_= "item_list")
    li_list = u_list.find("li", class_="slide" )
    title_results = soup.find('div', class_= "content_title").find('a').text
    article_teaser = soup.find('div', class_= "article_teaser_body").text
    ##### JPL Mars Space Images - Featured Image ####

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    browser.click_link_by_partial_text("FULL IMAGE")

    jplimage_html = browser.html
    jplimage_soup = BeautifulSoup(jplimage_html,"html.parser")

    img = jplimage_soup.find("img", class_="thumb")["src"]
    image_path = f"https://www.jpl.nasa.gov{img}"
    

    ##### Mars Weather ####

    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(mars_twitter_url)

    mars_twitter_soup = BeautifulSoup(response.text,"lxml")

    mars_tweet = mars_twitter_soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    current_weather_tweet = mars_tweet[0].text

    ##### Mars Facts ####

    mars_facts = "https://space-facts.com/mars/"
    fact_tables = pd.read_html(mars_facts)
    fact_tables
    mars_table = fact_tables[0]
   

    ##### Mars Hemispheres ####

    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)
    mars_html = browser.html
    html_soup = BeautifulSoup(mars_html, "html.parser")

    hemis = html_soup.find_all("div", class_="item")

    hemisphere_image_urls = []
    for hemi in hemis:
        image_title = hemi.find("h3").text
        url_link = hemi.find("a")["href"]
        url = "https://astrogeology.usgs.gov/"
        image_link = url + url_link 
        browser.visit(image_link)
        html= browser.html
        link_soup = BeautifulSoup(html, "html.parser")
        image_download = link_soup.find("div",class_= "downloads")
        image_url = image_download.find("a")["href"]
        hemisphere_image_urls.append({"Title:":image_title ,"Image URL:":image_url})
    
# Scraped data into a dictionary
    mars_info_scrape = {
        "title_results": title_results,
        "news_par": article_teaser ,
        "featured_image_url": image_path,
        "mars_weather": current_weather_tweet,
        "mars_table": mars_table,
        "hemisphere_image_urls":hemisphere_image_urls
    }
    
    browser.quit()  
    # Return results
    return mars_info_scrape