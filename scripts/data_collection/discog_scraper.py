#!venv/bin/python

# Author: Thomas Drain
# Year: 2019

# Script for scraping discographies (i.e. list of albums of each band) from metal-archives.com

# Approach:
# For each album in our Bands table,
# call the scrape_metalarchives() function which returns the albums' table data,
# then save to CSV.

import datetime
import pandas as pd
import pytz
import sys
from data_storage.db_connect import db_connect
from data_storage.db_insert_into import db_insert_into
from data_collection.get_discog import get_discog
from data_collection.scrape_metalarchives import scrape_metalarchives
from data_collection.tidy_discog import tidy_discog

# This is important when running over EC2, to add this path into the workpath
sys.path.insert(1, 'scripts/')

response_len = 500

# Column names I'm assigning, based on what the raw data has in it
# Note: keeping the names as lower case to be treated as case insensitive in Oracle,
# see https://docs.sqlalchemy.org/en/13/dialects/oracle.html
raw_data_fields = ['bandid', 'albumname', 'albumtype', 'albumyear', 'reviews', 'rating']

# Connect to RDS
rds_engine = db_connect()

# Valid inputs for the `band` parameter of the URL are NBR, ~, or A through Z
bands = 'xxx'  # QUERY GETTING ALL BAND IDS

# Need this for calculating scrape datetimes
ireland = pytz.timezone('Europe/Dublin')

# Store these so we can batch update at the end
discoglog_entries = pd.DataFrame({'band': bands,
                                'scrapedate': None})

discoglog_qu = """
SELECT t1.BandDiscogs_ScrapeID
FROM DISCOGLOG t1
INNER JOIN (
    SELECT MAX(ScrapeDate) max_date
    FROM DISCOGLOG
) t2
on t1.ScrapeDate = t2.max_date
"""
##############

try:
    for index, this_scrape in discoglog_entries.iterrows():
        # Scrape discography
        df_raw = scrape_metalarchives(item=this_scrape['band'],
                                      get_func=get_discog,
                                      col_names=raw_data_fields,
                                      response_len=response_len)

        # Update discography log
        print("Updating scrape log...")
        # Set the scrape as the current time (not 100% accurate but close enough...)
        irl_time = datetime.datetime.now(ireland)
        discoglog_entries.loc[index, 'scrapedate'] = irl_time
        # For some reason the scrapedate series is stored in discoglog_entries as an object, not a datetime:
        # this causes issues when inserting into DB (see db_insert_into)
        discoglog_entries[["scrapedate"]] = discoglog_entries[["scrapedate"]].apply(pd.to_datetime)

        db_insert_into(discoglog_entries.iloc[index:index+1], 'discoglog', rds_engine)

        # Get the last entry of the discography log, so we can take the scrape ID
        last_entry = pd.read_sql(discoglog_qu, rds_engine)

        # Tidy up the raw scraped output
        print("Tidying output...")
        df_clean = tidy_discog(df_raw, band=this_scrape['band'])
        df_clean.loc[:, 'discog_scrapeid'] = last_entry.loc[0, 'discog_scrapeid']

        # Write to RDS
        print("Inserting into database...\n")
        db_insert_into(new_rows=df_clean, table='discog', engine=rds_engine,
                       local='../../data/DISCOG_{}.csv'.format(irl_time.strftime('%Y-%m-%d')))
finally:
    # Close connection
    rds_engine.dispose()
    print('Complete!')

