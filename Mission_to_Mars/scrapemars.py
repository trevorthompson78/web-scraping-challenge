from bs4 import BeautifulSoup
from splinter import Browser
import requests
import time
import pandas as pd






def init_browser():
    
    executable_path = {"executable_path":"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless = False)


def scrape():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(5)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text



    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(url)
    large_image = browser.find_by_id('full_image')
    large_image.click()
    time.sleep(2)
    browser.click_link_by_partial_text('more info')


    Mars_url = browser.html
    soup = BeautifulSoup(Mars_url, 'html.parser')
    main_image_url = soup.find('img', class_="main_image")['src']
    featured_image_url = url + main_image_url
    featured_image_url


    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # mars_weather = soup.find('p', class_= 'TweetTextSize')
    data = requests.get(twitter_url)
    html = BeautifulSoup(data.text, 'html.parser')
    timeline = html.select('#timeline li.stream-item')

    for tweet in timeline:

        tweet_id = tweet['data-item-id']
        tweet_text = tweet.select('p.tweet-text')[0].text
        # all_tweets.append({"id": tweet_id, "text": tweet_text})

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    html = browser.html
    
    soup = BeautifulSoup(html, 'html.parser')

    mars_table = pd.read_html(facts_url)
    mars_table

    mars_df = mars_table[0]
    mars_df.columns = ['Category','Fact']
    # mars_df.head(100)

    mars_df = mars_df.to_html()
    # html_table

    mars_image_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_image_url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find('div', class_='result-list')
    images = results.find_all('div', class_='item')


    # mars_hemispheres_image_urls = []

    # for image in images:
    #     title = image.find("h3").text
    #     title = title.replace("Enhanced", "")
    #     image_link = image.find("a")["href"]
    #     link = "https://astrogeology.usgs.gov/" + image_link    
    #     browser.visit(link)
    #     html = browser.html
    #     soup = BeautifulSoup(html, "html.parser")
    #     downloads = soup.find("div", class_="downloads")
    #     image_url = downloads.find("a")["href"]
    #     mars_hemispheres_image_urls.append({"title": title, "img_url": image_url})

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": tweet_text,
        "mars_facts": mars_df,
        "hemisphere_image_urls": mars_hemispheres_image_urls
    }

    browser.quit()

    return mars_data

if __name__ == '__main__':
    scrape()