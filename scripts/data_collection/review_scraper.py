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
import sys
import time
from data_storage.db_connect import db_connect
from data_storage.db_insert_into import db_insert_into
from data_collection.get_review import get_review
from data_collection.scrape_metalarchives import scrape_metalarchives
from data_collection.tidy_review import tidy_review

# This is important when running over EC2, to add this path into the workpath
sys.path.insert(1, 'scripts/')

# Sequence of months we're going to scrape (going from most to least recent)
# Note: valid dates for review by-date listing are in YYYY-MM format
#start_date = '2019-06'
#dates = pd.date_range(end = start_date, periods = 4, freq = 'M').map(lambda x: x.strftime('%Y-%m'))[::-1]
#dates = pd.date_range(start = '2002-07', end = '2002-08', freq = 'M').map(lambda x: x.strftime('%Y-%m'))[::-1]
#dates = '2002-07'

response_len = 200

# Connect to RDS
rds_engine = db_connect()

# Columns in the returned JSON
# (for date scraping - see earlier code iterations for the alpha table column names)
raw_data_fields = ['Date', 'ReviewLink_html', 'BandLink_html', 'AlbumLink_html',
                    'Score', 'UserLink_html', 'Time']

# Prioritise which months we get first: those not completed, then those completed longest ago
log_qu = """
select *
from ReviewLog
where ScrapeDate is null and Month = '2019-11'
"""

reviewlog = pd.read_sql(log_qu, rds_engine)

# Store these so we can batch update at the end
new_entries = pd.DataFrame({'Month': reviewlog['Month'],
                            'ScrapeDate': None,
                            'Completed': None})

# We'll need this query to update the review records themselves with the log's scrape ID
this_scrape_qu = """
select *
from ReviewLog
where Review_ScrapeID = (
    select max(Review_ScrapeID) 
    from ReviewLog
)
"""

for index, row in reviewlog.iterrows():
    new_entries['ScrapeDate'][index] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    # Update review log
    # I'll need to figure out how to check whether the run was completed successfully...
    # new_entries['Completed'][index] = 'Y'
    db_insert_into(new_entries.iloc[[index]], 'ReviewLog', rds_engine)
    this_scrape = pd.read_sql(this_scrape_qu, rds_engine)

    # SCRAPE REVIEWS AND STORE IN DB
    scrape_metalarchives('Review', row['Month'], get_review, tidy_review,
                         raw_data_fields, this_scrape, response_len)

    time.sleep(3)

# TODO
# 1) UPDATE REVIEW TABLE WITH A JOIN TO REVIEWLOG, TO GET THE REVIEW_SCRAPEID FIELD
# USE data_storage/review_update_IDs.sql

# 2) FIGURE OUT WHAT TO DO WITH THE REVIEW TEXT ITSELF
# Close connection
rds_engine.dispose()

print('Complete!')
