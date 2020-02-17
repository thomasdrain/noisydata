
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


import time
import pandas as pd


def scrape_metalarchives(item, get_func, col_names, response_len=500):

    # Empty list for storing results
    dat = []

    # Get response from URL, then convert that response into a JSON string
    r = get_func(item, 0, response_len)
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

        # for attempt in range(10):
        time.sleep(3)  # Obeying their robots.txt "Crawl-delay: 3"
        # try:
        # We've already run this response once to get the record lengths,
        # so don't call on the first iteration
        if i > 0:
            r = get_func(item, start=start, length=response_len)
            js = r.json()

        # Store results in the list of Dataframes
        dat.append(pd.DataFrame(js['aaData']))

    # Append together all the dataframes
    res = pd.concat(dat)

    # Set informative names
    res.columns = col_names

    return res
