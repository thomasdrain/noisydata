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
import pytz
import sys
from data_storage.db_connect import db_connect
from data_storage.db_insert_into import db_insert_into
from data_collection.get_band import get_band
from data_collection.scrape_metalarchives import scrape_metalarchives
from data_collection.tidy_band import tidy_band

# This is important when running over EC2, to add this path into the workpath
sys.path.insert(1, 'scripts/')

response_len = 500

# Column names I'm assigning, based on what the raw data has in it
# Keeping these the same as the columns in the database
raw_data_fields = ['BandLink', 'Country', 'Genre', 'BandStatus']

# Connect to RDS
rds_engine = db_connect()

# Valid inputs for the `letter` parameter of the URL are NBR, ~, or A through Z
letters = 'NBR ~ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()

# Need this for calculating scrape datetimes
ireland = pytz.timezone('Europe/Dublin')

# Store these so we can batch update at the end
bandlog_entries = pd.DataFrame({'Letter': letters,
                                'ScrapeDate': None})

bandlog_qu = """
SELECT t1.Band_ScrapeID
FROM BANDLOG t1
INNER JOIN (
    SELECT MAX(ScrapeDate) max_date
    FROM BANDLOG
) t2
on t1.ScrapeDate = t2.max_date
"""

try:
    for index, this_scrape in bandlog_entries.iterrows():
        # Scrape bands
        df_raw = scrape_metalarchives(item=this_scrape['Letter'],
                                      get_func=get_band,
                                      col_names=raw_data_fields,
                                      response_len=response_len)

        # Update band log
        print("Updating scrape log...")
        # Set the scrape as the current time (not 100% accurate but close enough...)
        irl_time = datetime.datetime.now(ireland)
        bandlog_entries.loc[index, 'ScrapeDate'] = irl_time
        # For some reason the ScrapeDate series is stored in bandlog_entries as an object, not a datetime:
        # this causes issues when inserting into DB (see db_insert_into)
        # bandlog_entries[["ScrapeDate"]] = bandlog_entries[["ScrapeDate"]].apply(pd.to_datetime)

        db_insert_into(bandlog_entries.iloc[index:index+1], 'bandlog', rds_engine)

        # Get the last entry of the band log, so we can take the scrape ID
        last_entry = pd.read_sql(bandlog_qu, rds_engine)

        # Tidy up the raw scraped output
        print("Tidying output...")
        df_clean = tidy_band(df_raw, letter=this_scrape['Letter'])
        df_clean.loc[:, 'Band_ScrapeID'] = last_entry.loc[0, 'Band_ScrapeID']

        # Write to RDS
        print("Inserting into database...\n")
        db_insert_into(new_rows=df_clean, table='band', engine=rds_engine,
                       local='../../data/BAND_{}.csv'.format(irl_time.strftime('%Y-%m-%d')))
finally:
    # Close connection
    rds_engine.dispose()
    print('Complete!')

