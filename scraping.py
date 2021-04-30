
# import splinter and beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set up the executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

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
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# set up url to be able to visit
url = 'https://spaceimages-mars.com'
browser.visit(url)

# find and click the full button image
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# parse resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# add base url to the code to find the relative image
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# read_html() specifically searches for and returns a list of tables found in the HTML
# write the table to a df using pandas
# set zero index to specify only pull the first table it encounters
df = pd.read_html('https://galaxyfacts-mars.com')[0]

# assign columns to the dataframe
df.columns = ['description', 'Mars', 'Earth']

#set description column as the dataframe's index
df.set_index('description', inplace=True)
df

# convert df back to html 
df.to_html()

# close the webrowser when done scraping
browser.quit()




