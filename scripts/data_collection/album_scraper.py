#!venv/bin/python

# Author: Thomas Drain
# Year: 2020

# Script for scraping albums from metal-archives.com

# Approach:
# For each album in our Bands table,
# call the scrape_metalarchives() function which returns the albums' table data,
# then save to CSV.

import datetime
import pandas as pd
import pytz
import time
from data_storage.db_connect import db_connect
from data_storage.db_insert_into import db_insert_into
from data_collection.get_discog import get_discog

# Column names I'm assigning, based on what the raw data has in it
# Note: keeping the names as lower case to be treated as case insensitive in Oracle,
# see https://docs.sqlalchemy.org/en/13/dialects/oracle.html
raw_data_fields = ['BandID', 'AlbumName', 'AlbumType', 'AlbumYear', 'Reviews', 'Rating']

# Connect to RDS
rds_engine = db_connect()

# All the band IDs we have on record that have not already been scraped.
# We'll search for albums for each of these bands.
# Note: there are around 134,000 bands so all up this is almost 5 days of scraping!
band_id_qu = """
SELECT DISTINCT b.BandID, r.Num_Reviews
FROM BAND b 
LEFT JOIN (
    SELECT BandID, COUNT(DISTINCT LOWER(ReviewLink)) as Num_Reviews
    FROM REVIEW
    WHERE BandID IS NOT NULL
    GROUP BY BandID
) r
ON b.BandID = r.BandID
WHERE 
b.BandID NOT IN (
    SELECT BandID 
    FROM DISCOGLOG 
    WHERE BandID IS NOT NULL
)
ORDER BY r.Num_Reviews desc
"""

print("Querying full list of bands...")
bands_df = pd.read_sql(band_id_qu, rds_engine)
bands = bands_df.loc[:, 'BandID']

# Need this for calculating scrape datetimes
ireland = pytz.timezone('Europe/Dublin')

# Store these so we can batch update at the end
discoglog_entries = pd.DataFrame({'BandID': bands,
                                  'ScrapeDate': None})

print("There are ", len(discoglog_entries), " bands to scrape today.", sep="")

# The most recent discography scrapes (i.e. the last time
# the albums were scraped from each band).
# This query gets run for each discography, so we know what the ID should be
discoglog_qu = """
SELECT t1.Discog_ScrapeID
FROM DISCOGLOG t1
INNER JOIN (
    SELECT MAX(ScrapeDate) max_date
    FROM DISCOGLOG
) t2
on t1.ScrapeDate = t2.max_date
"""

try:
    for index, this_scrape in discoglog_entries.iterrows():

        if index > 0:
            # Wait 60 mins every 50,000 scrapes
            if index % 50000 == 0:
                time.sleep(3600)

            # Wait 20 mins every 10,000 scrapes
            elif index % 10000 == 0:
                time.sleep(1200)

            # Wait 5 mins every 1000 scrapes
            elif index % 1000 == 0:
                time.sleep(300)

        print('*** Scraping albums for band #', index, ' of ',
              len(discoglog_entries), ' (band ID ', this_scrape['BandID'], ')', sep="")

        # Scrape albums
        df_raw = get_discog(this_scrape['BandID'])

        # Update discography log
        print("Updating scrape log...")
        # Set the scrape as the current time (not 100% accurate but close enough...)
        irl_time = datetime.datetime.now(ireland)
        discoglog_entries.loc[index, 'ScrapeDate'] = irl_time
        
        db_insert_into(discoglog_entries.iloc[index:index+1], 'discoglog', rds_engine)

        # If no result returned then there is no discography for that band (i.e. no albums)
        if df_raw is None:
            print("Moving on...\n")
        else:
            # Get the last entry of the discography log at this loop iteration,
            # so we can take the current scrape ID
            last_entry = pd.read_sql(discoglog_qu, rds_engine)

            # Currently there is no additional 'tidy' step; all is done in the
            # get_discog() as it's a fairly easy manipulation
            df_clean = df_raw
            df_clean.loc[:, 'Discog_ScrapeID'] = last_entry.loc[0, 'Discog_ScrapeID']

            # Write to RDS
            print("Inserting into database...\n")
            db_insert_into(new_rows=df_clean, table='album', engine=rds_engine
                           #, local='../../data/ALBUM_{}.csv'.format(irl_time.strftime('%Y-%m-%d'))
                           )
        time.sleep(2)

finally:
    # Close connection
    rds_engine.dispose()
    print('Complete!')

