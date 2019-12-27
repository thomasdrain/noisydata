#!venv/bin/python

# Author: Thomas Drain, Jon Charest
# Year: 2019

# Script for scraping bands and associated information from metal-archives.com

# Approach:
# For each letter in the alphabet (including 'NBR'),
# call the scrape_MA() function which returns the review table data,
# then save to CSV.

import datetime
import pandas as pd
import sys
import time
from data_storage.db_connect import db_connect
from data_storage.db_insert_into import db_insert_into
from data_collection.get_band import get_band
from data_collection.scrape_metalarchives import scrape_metalarchives
from data_collection.tidy_band import tidy_band

# This is important when running over EC2, to add this path into the workpath
sys.path.insert(1, 'scripts/')

response_len = 500

# Column names I'm assigning, based on what the raw data has in it
column_names = ['Link', 'Country', 'Genre', 'Status']

# Connect to RDS
rds_engine = db_connect()

# Valid inputs for the `letter` parameter of the URL are NBR, ~, or A through Z
#letters = 'NBR ~ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
#letters = 'Z'

# Prioritise which letters we get first: those not completed, then those completed longest ago
log_qu = """
select *
from BandLog
order by Completed, ScrapeDate
#limit 1
"""

bandlog = pd.read_sql(log_qu, rds_engine)

# Store these so we can batch update at the end
new_entries = pd.DataFrame({'Letter': bandlog['Letter'],
                            'ScrapeDate': None,
                            'Completed': 'N'})

try:
    for index, row in bandlog.iterrows():

        new_entries['ScrapeDate'][index] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # SCRAPE BANDS
        bands_raw = scrape_metalarchives('Band', row['Letter'], get_band, tidy_band, column_names, response_len)

        new_entries['Completed'][index] = 'Y'

        time.sleep(111)

finally:
    # If we have missing dates then the scrape never started
    # (but we keep incomplete records, in case of an error)
    print(new_entries)
    new_entries.dropna(how='any')
    print(new_entries)
    # Update band log
    db_insert_into(new_entries, 'BandLog', rds_engine)

    # TODO
    # UPDATE BAND TABLE WITH A JOIN TO BANDLOG, TO GET THE BAND_SCRAPEID FIELD
    # USE data_storage/band_update_IDs.sql
    # Close connection
    rds_engine.dispose()

    print('Complete!')


