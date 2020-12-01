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
import time
from data_storage.db_connect import db_connect
from data_storage.db_insert_into import db_insert_into
from data_collection.get_review import get_review
from data_collection.scrape_metalarchives import scrape_metalarchives
from data_collection.tidy_review import tidy_review

response_len = 200

# Connect to RDS
rds_engine = db_connect()

# Get the max review date on the DB
month_range_sql = """
SELECT 
    -- The month of our latest review on the table (we'll scrape this again next month, 
    -- but just to be sure we haven't missed any reviews). 
    FORMAT(ISNULL(MAX(ReviewDate), '01-AUG-2002'), 'yyyy-MM') START_DATE
    -- The previous month (relative to today - range is non-inclusive)
    , FORMAT(SYSDATETIME(), 'yyyy-MM') END_DATE
FROM Review
"""

month_ranges = pd.read_sql(month_range_sql, rds_engine)
start_date = month_ranges.loc[:, 'START_DATE'].values[0]
end_date = month_ranges.loc[:, 'END_DATE'].values[0]

# Sequence of months we're going to scrape
# Note: valid dates for review by-date listing are in YYYY-MM format
months = pd.date_range(start=start_date, end=end_date, freq='M').map(lambda x: x.strftime('%Y-%m'))

# Column names I'm assigning, based on what the raw data has in it
# Keeping these the same as the columns in the database
raw_data_fields = ['ReviewDate', 'ReviewLink_html', 'BandLink_html', 'AlbumLink_html',
                   'ReviewScore', 'UserLink_html', 'ReviewTime']

# Need this for calculating scrape datetimes
ireland = pytz.timezone('Europe/Dublin')

# Store these so we can batch update at the end
reviewlog_entries = pd.DataFrame({'ReviewMonth': months,
                                  'ScrapeDate': None})

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
        df_raw = scrape_metalarchives(item=this_scrape['ReviewMonth'],
                                      get_func=get_review,
                                      col_names=raw_data_fields,
                                      response_len=response_len)

        print("Updating scrape log...")
        # Set the scrape as the current time (not 100% accurate but close enough...)
        irl_time = datetime.datetime.now(ireland)
        reviewlog_entries.loc[index, 'ScrapeDate'] = irl_time

        # Insert the new log entry
        db_insert_into(reviewlog_entries.iloc[index:index+1], 'reviewlog', rds_engine)

        # Get the last entry of the band log, so we can take the scrape ID
        last_entry = pd.read_sql(reviewlog_qu, rds_engine)

        # Tidy up the raw scraped output
        print("Tidying output...")
        df_clean = tidy_review(df_raw, month=this_scrape['ReviewMonth'])
        df_clean.loc[:, 'Review_ScrapeID'] = last_entry.loc[0, 'Review_ScrapeID']

        # Write to RDS
        print("Inserting into database...\n")
        db_insert_into(new_rows=df_clean, table='review', engine=rds_engine
                       #, local='../../data/REVIEW_{}.csv'.format(irl_time.strftime('%Y-%m-%d'))
                       )
        # This job is quite large, particularly when running it the first time, so sleep a bit after each month
        time.sleep(60)

finally:
    # Close connection
    rds_engine.dispose()
    print('Complete!')