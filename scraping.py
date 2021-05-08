
# import splinter and beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import requests

def scrape_all():
    # set up the executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #use mars_news function to pull this data
    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "mars_hemispheres" : mars_hemis(browser),
        "last_modified": dt.datetime.now()}

    # stop webdriver and return data
    browser.quit()
    return data

#create a function
def mars_news(browser):

    # set up the url then tell the browser to visit the webpage
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # optional delay for loading the page
    # search for elements with combination of tag (div) and attribute (list_text)
    # tell browser to wait 1 second before searching for components (allows page to load)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up HMTL parser
    html = browser.html
    new_soup = soup(html, 'html.parser')

    #add try/except error handling
    try:
        # parent element - holds all of the other elements in it
        # . is used for selecting classes (ie.list_text)
        # CSS works from right to left (ie. returning the last item on the list instead of the first)
        # using select_one, the first matching element returned will be a <li /> element with a class of slide and all nested elements within it
        slide_elem = new_soup.select_one('div.list_text')

        # This variable holds a ton of information, so look inside of that information to find this specific data
        # The specific data is in a <div /> with a class of 'content_title'
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        # add .get_text() to only return text element with no html tags
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p


def featured_image(browser):
    # set up url to be able to visit
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find and click the full button image
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parse resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # add base url to the code to find the relative image
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    try:
        # read_html() specifically searches for and returns a list of tables found in the HTML
        # write the table to a df using pandas
        # set zero index to specify only pull the first table it encounters
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        #print("Unable to collect mars facts")
        return None

    # assign columns to the dataframe
    df.columns = ['Description', 'Mars', 'Earth']

    #set description column as the dataframe's index
    df.set_index('Description', inplace=True)


    # convert df back to html 
    return df.to_html()

def mars_hemis(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    for n in range(4):
        browser.find_by_css('a.product-item h3')[n].click()
        hemispheres = {}

        html = browser.html
        results = soup(html, 'html.parser')

        try:
            hemispheres['title'] = results.find('h2', class_='title').get_text()
            downloads = results.find('div', class_='downloads')
            pic_url = downloads.find('a').get('href')
            hemispheres['img_url'] = str('https://marshemispheres.com/' + pic_url)
            hemisphere_image_urls.append(hemispheres)

        except BaseException:
            return None
        
        browser.back()
    
    return hemisphere_image_urls



# script is complete and ready for action
if __name__ == "__main__":

    # if running as script, print scraped data
    print(scrape_all())




