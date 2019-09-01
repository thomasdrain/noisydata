# Author: Thomas Drain, Jon Charest
# Year: 2019

# Script for scraping album reviews and associated information from metal-archives.com

# Approach:
# For each month in a sequence (reviews must be requested in monthly chunks),
# call the scrape_MA() function which returns the review table data,
# then go into each review and extract the text itself.
# Finally save to CSV.

import datetime
import pandas as pd
from scraping import get_review
from scraping import scrape_metalarchives
from scraping import tidy_review


# Sequence of months we're going to scrape (going from most to least recent)
# Note: valid dates for review by-date listing are in YYYY-MM format
#start_date = '2019-06'
#dates = pd.date_range(end = start_date, periods = 4, freq = 'M').map(lambda x: x.strftime('%Y-%m'))[::-1]
dates = pd.date_range(start = '2002-07', end = '2002-08', freq = 'M').map(lambda x: x.strftime('%Y-%m'))[::-1]

response_len = 200
date_of_scraping = datetime.datetime.utcnow().strftime('%d-%m-%Y')

# Columns in the returned JSON
# (for date scraping - see earlier code iterations for the alpha table column names)
date_col_names = ['Date', 'ReviewLink', 'BandLink', 'AlbumLink',
                  'Score', 'UserLink', 'Time']

# Scrape all the reviews for each month in the sequence
for date in dates:
    # SCRAPE REVIEWS
    reviews_raw = scrape_metalarchives(date, get_review, response_len)

    # Set informative names
    reviews_raw.columns = date_col_names

    # Tidy up the raw scraped output
    reviews_clean = tidy_review(reviews_raw)

    # Save to CSV
    f_name_review = 'data/MA-reviews_{}_{}.csv'.format(date, date_of_scraping)
    print('Writing review data to csv file:', f_name_review)
    reviews_clean.to_csv(f_name_review)

print('Complete!')
