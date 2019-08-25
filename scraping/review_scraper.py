# Author: Thomas Drain, Jon Charest
# Year: 2019

# Script for scraping album reviews and associated information from metal-archives.com

# Approach:
# For each month in a sequence (reviews must be requested in monthly chunks),
# call the scrape_MA() function which returns the review table data,
# then go into each review and extract the text itself.
# Finally save to CSV.

import time
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import get_url as gu
import scrape_MA as sma


def get_review_url(date = "2019-01", start=0, length=200):
    """Gets the review listings displayed as monthly tables on M-A for
    input `date`, starting at `start` and ending at `start` + `length`.
    Returns a `Response` object. Data can be accessed by calling the `json()`
    method of the returned `Response` object.
    Note: this can be done alphabetically, however to minimise calls I've
    used the monthly tables"""

    review_url = 'http://www.metal-archives.com/review/ajax-list-browse/by/date/selection/' + date + '/json/1'

    review_payload = {'sEcho': 1,
                      'iColumns': 7,
                      'iDisplayStart': start,
                      'iDisplayLength': length}
    if start == 0:
        print('Current month = ', date)

    r = gu.get_url(review_url, payload = review_payload)

    return r


# Sequence of months we're going to scrape (going from most to least recent)
# Note: valid dates for review by-date listing are in YYYY-MM format
#start_date = '2019-06'
#dates = pd.date_range(end = start_date, periods = 4, freq = 'M').map(lambda x: x.strftime('%Y-%m'))[::-1]
dates = pd.date_range(start = '2002-07', end = '2002-08', freq = 'M').map(lambda x: x.strftime('%Y-%m'))[::-1]

response_len = 200
date_of_scraping = datetime.datetime.utcnow().strftime('%d%M%Y')

# Columns in the returned JSON
# (for date scraping - see earlier code iterations for the alpha table column names)
date_col_names = ['Date', 'ReviewLink', 'BandLink', 'AlbumLink',
                  'Score', 'UserLink', 'Time']

# Scrape all the reviews for each month in the sequence
for date in dates:

    raw = sma.scrape_MA(date, get_review_url, response_len)

    clean = raw
    clean.columns = date_col_names

    # Fetch review title and content
    review_titles = []
    reviews = []

    # Go into each review record, access the URL and get the review text itself
    print('Fetching review content...')
    for n, link in enumerate(clean['ReviewLink']):
        time.sleep(3)
        print('Review #', n+1)
        linksoup = BeautifulSoup(link, 'html.parser')
        review_page = gu.get_url(linksoup.a['href'])
        review_page.encoding = 'UTF-8'
        review_soup = BeautifulSoup(review_page.text, 'html.parser')
        review_title = review_soup.find_all('h3')[0].text.strip()[:-6]
        review_titles.append(review_title)
        review = review_soup.find_all('div', {'class': 'reviewContent'})[0].text
        reviews.append(review)

    # Store review data & save to disk
    clean['ReviewTitle'] = review_titles
    clean['ReviewContent'] = reviews
    clean['DateScraped'] = date_of_scraping

    f_name = 'data/MA-reviews_{}_{}.csv'.format(date, date_of_scraping)
    print('Writing reviews to csv file:', f_name)
    clean.to_csv(f_name)

print('Complete!')
