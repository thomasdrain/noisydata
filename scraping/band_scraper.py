
# ! /usr/bin/env python
#
# Script for scraping band names and basic associated information from
# http://www.metal-archives.com
#
# Author: Jon Charest (http://github.com/jonchar
# Year: 2016
#
# Approach:
# For each {NBR, A-Z}
# Read number of entries for given letter using result from `get_url`
# Determine how many requests of 500 entries are required, issue requests
# Read JSON in the `Requests` object returned by `get_url` using `r.json()`
# Read contents in 'aaData' key into a pandas `DataFrame`
# Set column names to `column_names`
# Clean up columns
# Concatenate & store outputs in a DataFrame
# Save final DataFrame to csv

import time
import datetime
import scrape_MA as sma
import get_url as gu

def get_band_url(letter='A', start=0, length=500):
    """Gets the listings displayed as alphabetical tables on M-A for input
    `letter`, starting at `start` and ending at `start` + `length`.
    Returns a `Response` object. Data can be accessed by calling the `json()`
    method of the returned `Response` object."""

    band_url = 'http://www.metal-archives.com/browse/ajax-letter/json/1/l/' + letter

    band_payload = {'sEcho': 0,  # if not set, response text is not valid JSON
                    'iDisplayStart': start,  # set start index of band names returned
                    'iDisplayLength': length} # only response lengths of 500 work
    if start == 0:
        print('Current letter = ', letter)

    r = gu.get_url(band_url, payload = band_payload)
    return r


# Data columns returned in the JSON object
column_names = ['NameLink', 'Country', 'Genre', 'Status']
response_len = 500

# Valid inputs for the `letter` parameter of the URL are NBR or A through Z
letters = 'NBR A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
letters = 'Z'

for letter in letters:
    raw = sma.scrape_MA(letter, get_band_url, response_len)

    clean = raw
    # Set informative names
    clean.columns = column_names

    # Current index corresponds to index in smaller chunks concatenated
    # Reset index to start at 0 and end at number of bands
    clean.index = range(len(clean))

    # Save to CSV
    date_of_scraping = datetime.datetime.utcnow().strftime('%d%M%Y')
    f_name = 'data/MA-band-names_{}_{}.csv'.format(letter, date_of_scraping)
    print('Writing band data to csv file:', f_name)
    clean.to_csv(f_name)

print('Complete!')
