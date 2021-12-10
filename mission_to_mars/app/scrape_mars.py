import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # reference items in dict before function so it knows where to pull info
    news_title, news_p = mars_news(browser)

    # run all scrapes and store in dictionary
    scraped_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": jpl_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_layout(browser),
    }
    #quit browser, return data
    browser.quit()
    return scraped_data

def mars_news(browser):
    # set up url visit
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # create the soup object for mars site
    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')

    # collect the latest/most recent News title and Paragraph # 

    # isolate parent div
    first_news_div = mars_soup.find('div', class_='list_text')
    # store the title and first paragraph into variables
    news_title = first_news_div.find('div',class_='content_title').get_text()

    news_p = first_news_div.find('div',class_='article_teaser_body').get_text()

    return news_title, news_p

def jpl_image(browser):
    # visit JPL URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find full image button, click it
    # first button is nav bar - click second instance
    browser.find_by_tag('button')[1].click()
    # parse the page for the full img url

    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')

    # find img url

    rel_img_url = jpl_soup.find('img',class_='fancybox-image')['src']

    # combine with parent URL for maximun URL-ability
    abs_img_url = f'https://spaceimages-mars.com/{rel_img_url}'
    abs_img_url
    return abs_img_url

def mars_facts():
    # mars fact url
    url = 'https://galaxyfacts-mars.com/'
    # i think we only want the first table
    mars_df = pd.read_html(url)[0]

    mars_df.columns=['Attribute', 'Mars', 'Earth']
    mars_df.set_index('Attribute', inplace=True)

    return mars_df.to_html()

def hemisphere_layout(browser):
    # previous function not working - attributes are being passed through html before scrape
    # cut function in half to estabilish a ground work then call new scrape function inside ground work
    # so that the hemisphere dict will stop being passed while empty and throwing error


    # lay ouy the ground work for the information gathering
    url = 'https://marshemispheres.com/'

    browser.visit(url + 'index.html')
#     html = browser.html
    links = browser.links.find_by_partial_text('Enhanced')

    # make a list to hold the images and titles
    # need list of dictionaries
    hemisphere_image_urls = []
    for i in range(0,4):
        #navigate to first link, click
        browser.links.find_by_partial_text('Enhanced')[i].click()
        hemishpere_data = hemisphere_scrape(browser)
        # returned dict from hemi_scrape to list
        hemisphere_image_urls.append(hemishpere_data)
        # repeat for next loop-link
        browser.back()
    return hemisphere_image_urls


def hemisphere_scrape(browser):
    
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=True)

    # this function is part two of the previous scrape function
    # it will collect the information mid-call and have it in a dictionary ready
    # for the hemi_layout() function.

    # make dict to store values before being returned
    hemispheres = {}

    jpg_link = browser.links.find_by_partial_href('full.jpg')
    hemispheres['jpg_url']=jpg_link['href']
    hemispheres['title'] = browser.find_by_css('h2.title').text



    return hemispheres



