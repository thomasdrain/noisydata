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
import scraping_sequence

BASE_URL = 'http://www.metal-archives.com'

# for reviews alphabetically
#URL_EXT_ALPHA = '/review/ajax-list-browse/by/alpha/selection/'
# for reviews by date

encoding = 'UTF-8'

#@scraping_sequence
def get_review_url(date = "2019-01", start=0, length=200):
    """Gets the review listings displayed as alphabetical tables on M-A for
    input `letter`, starting at `start` and ending at `start` + `length`.
    Returns a `Response` object. Data can be accessed by calling the `json()`
    method of the returned `Response` object."""

    review_url = '/review/ajax-list-browse/by/date/selection/' + date + '/json/1'

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

# Valid letter entries for alphabetical listing
#letters = 'nbr A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
#letters = 'Z'

# start_date being the start of the reverse sequence of dates (excludes current month)
#today_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
today_date = '2019-06'
# Sequence of months we're going to scrape (going from most to least recent)
# Note: valid dates for review by-date listing are in YYYY-MM format
dates = pd.date_range(end = today_date, periods = 4, freq = 'M').map(lambda x: x.strftime('%Y-%m'))[::-1]

data = DataFrame()

# Retrieve the review listings
# Get the reviews by month (in reverse order)
for date in dates:

    # Get total records for a given date & calculate number of chunks
    print('Current month = ', date)
    r = get_review_url(date=date, start=0, length=response_len)
    js = r.json()
    n_records = js['iTotalRecords']
    n_chunks = int(n_records / response_len) + 1
    print('Total records = ', n_records)

    # Retrieve chunks
    for i in range(n_chunks):
        start = response_len * i
        if start + response_len < n_records:
            end = start + response_len
        else:
            end = n_records
        print('Fetching review entries', start, 'to', end)

        for attempt in range(10):
            time.sleep(3) # Obeying their robots.txt "Crawl-delay: 3"
            try:
                r = get_review_url(date=date, start=start, length=response_len)
                r.encoding = encoding
                js = r.json()
                # Store response
                df = DataFrame(js['aaData'], columns=date_col_names)
            # If the response fails, r.json() will raise an exception, so retry
            except JSONDecodeError:
                print('JSONDecodeError on attempt ', attempt, ' of 10.')
                print('Retrying...')
                continue
            break

        # Fetch review title and content
        review_titles = []
        reviews = []
        print('Fetching review content...')
        for n, link in enumerate(df['ReviewLink']):
            time.sleep(3)
            print('Review #', n+1)
            linksoup = BeautifulSoup(link, 'html.parser')
            review_page = gu.get_url(linksoup.a['href'])
            review_page.encoding = encoding
            review_soup = BeautifulSoup(review_page.text, 'html.parser')
            review_title = review_soup.find_all('h3')[0].text.strip()[:-6]
            review_titles.append(review_title)
            review = review_soup.find_all('div', {'class': 'reviewContent'})[0].text
            reviews.append(review)

        # Store review data & save to disk
        df['ReviewTitle'] = review_titles
        df['ReviewContent'] = reviews
        df['DateScraped'] = today_date
        f_name = 'data/MA-reviews_' + date + '_' + '%03d' % i + '.csv'
        print('Writing chunk to csv file:', f_name)
        df.to_csv(f_name)

print('Complete!')
