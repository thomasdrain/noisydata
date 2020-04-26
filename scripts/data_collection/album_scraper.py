#!venv/bin/python

# Author: Thomas Drain
# Year: 2019

# Script for scraping albums from metal-archives.com

# Approach:
# For each album in our Bands table,
# call the scrape_metalarchives() function which returns the albums' table data,
# then save to CSV.

import datetime
import pandas as pd
import pytz
import sys
import time
from data_storage.db_connect import db_connect
from data_storage.db_insert_into import db_insert_into
from data_collection.get_discog import get_discog

# This is important when running over EC2, to add this path into the workpath
sys.path.insert(1, 'scripts/')

# Column names I'm assigning, based on what the raw data has in it
# Note: keeping the names as lower case to be treated as case insensitive in Oracle,
# see https://docs.sqlalchemy.org/en/13/dialects/oracle.html
raw_data_fields = ['bandid', 'albumname', 'albumtype', 'albumyear', 'reviews', 'rating']

# Connect to RDS
rds_engine = db_connect()

# All the band IDs we have on record that have not already been scraped.
# We'll search for albums for each of these bands.
# Note: there are around 134,000 bands so all up this is almost 5 days of scraping!

band_id_qu = """
SELECT DISTINCT BandID
FROM BAND
WHERE 
BandID NOT IN (
    SELECT BandID 
    FROM DISCOGLOG 
    WHERE BandID IS NOT NULL
) AND
BandID IN (
    SELECT r.BandID
    FROM Review r
    INNER JOIN (
        SELECT BandID, COUNT(DISTINCT LOWER(ReviewLink)) as Num_Reviews
        FROM REVIEW
        WHERE BandID IS NOT NULL
        GROUP BY BandID
    ) c
    ON r.BandID = c.BandID AND
    c.Num_Reviews >= 1   
)
"""

print("Querying full list of bands...")
bands_df = pd.read_sql(band_id_qu, rds_engine)
bands = bands_df.loc[:, "bandid"]

# Need this for calculating scrape datetimes
ireland = pytz.timezone('Europe/Dublin')

# Store these so we can batch update at the end
discoglog_entries = pd.DataFrame({'bandid': bands,
                                  'scrapedate': None})

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

        print('*** Scraping albums for band #', index, ' of ',
              len(discoglog_entries), ' (band ID ', this_scrape['bandid'], ')', sep="")

        # Scrape albums
        df_raw = get_discog(this_scrape['bandid'])

        # Update discography log
        print("Updating scrape log...")
        # Set the scrape as the current time (not 100% accurate but close enough...)
        irl_time = datetime.datetime.now(ireland)
        discoglog_entries.loc[index, 'scrapedate'] = irl_time
        # For some reason the scrapedate series is stored in discoglog_entries as an object, not a datetime:
        # this causes issues when inserting into DB (see db_insert_into)
        discoglog_entries[["scrapedate"]] = discoglog_entries[["scrapedate"]].apply(pd.to_datetime)

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
            df_clean.loc[:, 'discog_scrapeid'] = last_entry.loc[0, 'discog_scrapeid']

            # Write to RDS
            print("Inserting into database...\n")
            db_insert_into(new_rows=df_clean, table='album', engine=rds_engine,
                           local='../../data/ALBUM_{}.csv'.format(irl_time.strftime('%Y-%m-%d')))
        time.sleep(2)
finally:
    # Close connection
    rds_engine.dispose()
    print('Complete!')

