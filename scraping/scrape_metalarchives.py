
# Author: Thomas Drain, Jon Charest
# Year: 2019

# General purpose loop for scraping metal-archives.com,
# flexible in which kind of data able to be scraped (e.g. bands, reviews)

# Approach:
# Using the supplied scraper function, call the url of the supplied url
# Determine how many requests are required, then issue requests
# Read JSON object
# Read contents in 'aaData' key and put into a pandas `DataFrame`
# Return raw results after all requests have been made

import json
import datetime
import time
from pandas import DataFrame


def scrape_metalarchives(element, get_func, response_len = 500):

    res = DataFrame()  # for collecting the results

    # Get response from URL, then convert that response into a JSON string
    r = get_func(element, 0, response_len)
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
        print('Fetching entries ', start, 'to ', end)

        for attempt in range(10):
            time.sleep(3)  # Obeying their robots.txt "Crawl-delay: 3"
            try:
                # We've already run this response once to get the record lengths,
                # so don't call on the first iteration
                if i > 0:
                    r = get_func(element, start=start, length=response_len)
                    js = r.json()
                # Store response
                df = DataFrame(js['aaData'])
                df['Scraped'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                res = res.append(df)

            # If the response fails, r.json() will raise an exception, so retry
            except ValueError:
                print('JSONDecodeError on attempt ', attempt, ' of 10.')
                print('Retrying...')
                continue
            break
    return res