#! /usr/bin/env python
#
# Script for scraping album reviews and associated information from
# http://www.metal-archives.com
#
# Author: Jon Charest (http://github.com/jonchar)
# Year: 2016
#
# Approach:
# For each {nbr, A-Z}
# Read number of entries for given letter using result from `get_url`
# Determine how many requests of 200 entries are required, issue requests
# Read JSON in the `Requests` object returned by `get_url` using `r.json()`
# Read contents in 'aaData' key into a pandas `DataFrame`
# Set column names to `date_col_names`
# For each link in the list of reviews, visit link and extract the title
# of the review and the content of the review
# Save chunk of reviews to csv file

import time
import datetime
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import get_url as gu
import scrape_MA as sma


# for reviews alphabetically
#URL_EXT_ALPHA = '/review/ajax-list-browse/by/alpha/selection/'

#@scraping_sequence
def get_review_url(date = "2019-01", start=0, length=200):
    """Gets the review listings displayed as alphabetical tables on M-A for
    input `letter`, starting at `start` and ending at `start` + `length`.
    Returns a `Response` object. Data can be accessed by calling the `json()`
    method of the returned `Response` object."""

    review_url = 'http://www.metal-archives.com/review/ajax-list-browse/by/date/selection/' + date + '/json/1'

    review_payload = {'sEcho': 1,
                      'iColumns': 7,
                      'iDisplayStart': start,
                      'iDisplayLength': length}
    if start == 0:
        print('Current month = ', date)

    r = gu.get_url(review_url, payload = review_payload)

    return r

# Data columns in the returned JSON
#alpha_col_names = ['BandName', 'ReviewLink', 'BandLink', 'AlbumLink',
#                   'Score', 'UserLink', 'Date']
date_col_names = ['Date', 'ReviewLink', 'BandLink', 'AlbumLink',
                  'Score', 'UserLink', 'Time']

# start_date being the start of the reverse sequence of dates (excludes current month)
#today_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
today_date = '2019-06'
# Sequence of months we're going to scrape (going from most to least recent)
# Note: valid dates for review by-date listing are in YYYY-MM format
#dates = pd.date_range(end = today_date, periods = 4, freq = 'M').map(lambda x: x.strftime('%Y-%m'))[::-1]
dates = pd.date_range(start = '2002-07', end = '2002-08', freq = 'M').map(lambda x: x.strftime('%Y-%m'))[::-1]

response_len = 200

# For each month in our sequence, scrape all the reviews
for date in dates:

    raw = sma.scrape_MA(date, get_review_url, response_len)

    clean = raw
    # Set informative names
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
    clean['DateScraped'] = today_date

    date_of_scraping = datetime.datetime.utcnow().strftime('%d%M%Y')
    f_name = 'data/MA-reviews_{}_{}.csv'.format(date, date_of_scraping)
    print('Writing reviews to csv file:', f_name)
    clean.to_csv(f_name)

print('Complete!')
