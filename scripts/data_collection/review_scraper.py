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
import pytz
import sys
import time
from data_storage.db_connect import db_connect
from data_storage.db_insert_into import db_insert_into
from data_collection.get_review import get_review
from data_collection.scrape_metalarchives import scrape_metalarchives
from data_collection.tidy_review import tidy_review


# Sequence of months we're going to scrape
# Note: valid dates for review by-date listing are in YYYY-MM format
end_month = '2020-01'
months = pd.date_range(start='2002-07', end=end_month, freq='M').map(lambda x: x.strftime('%Y-%m'))

response_len = 200

# Connect to RDS
rds_engine = db_connect()

# Column names I'm assigning, based on what the raw data has in it
# Note: keeping the names as lower case to be treated as case insensitive in Oracle,
# see https://docs.sqlalchemy.org/en/13/dialects/oracle.html
raw_data_fields = ['date', 'reviewlink_html', 'bandlink_html', 'albumlink_html',
                    'score', 'userlink_html', 'time']

# Need this for calculating scrape datetimes
ireland = pytz.timezone('Europe/Dublin')

# Store these so we can batch update at the end
reviewlog_entries = pd.DataFrame({'month': months,
                                  'scrapedate': None})

reviewlog_qu = """
SELECT t1.Review_ScrapeID
FROM REVIEWLOG t1
INNER JOIN (
    SELECT MAX(ScrapeDate) max_date
    FROM REVIEWLOG
) t2
on t1.ScrapeDate = t2.max_date
"""

try:
    for index, this_scrape in reviewlog_entries.iterrows():
        # Scrape reviews
        df_raw = scrape_metalarchives(item=this_scrape['month'],
                                      get_func=get_review,
                                      col_names=raw_data_fields,
                                      response_len=response_len)

        print("Updating scrape log...")
        # Set the scrape as the current time (not 100% accurate but close enough...)
        irl_time = datetime.datetime.now(ireland)
        reviewlog_entries.loc[index, 'scrapedate'] = irl_time

        # For some reason the scrapedate series is stored in reviewlog_entries as an object, not a datetime:
        # this causes issues when inserting into DB (see db_insert_into)
        reviewlog_entries[["scrapedate"]] = reviewlog_entries[["scrapedate"]].apply(pd.to_datetime)

        # Insert the new log entry
        db_insert_into(reviewlog_entries.iloc[index:index+1], 'reviewlog', rds_engine)

        # Get the last entry of the band log, so we can take the scrape ID
        last_entry = pd.read_sql(reviewlog_qu, rds_engine)

        # Tidy up the raw scraped output
        print("Tidying output...")
        df_clean = tidy_review(df_raw, month=this_scrape['month'])
        df_clean.loc[:, 'review_scrapeid'] = last_entry.loc[0, 'review_scrapeid']

        # Write to RDS
        print("Inserting into database...\n")
        db_insert_into(new_rows=df_clean, table='review', engine=rds_engine)

finally:
    # Close connection
    rds_engine.dispose()
    print('Complete!')