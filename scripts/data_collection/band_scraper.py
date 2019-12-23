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
from data_storage import db_connect, db_insert_into
from data_collection import get_band, scrape_metalarchives, tidy_band


#get_album().to_csv("data/album_tmp.csv")

response_len = 500
date_of_scraping = datetime.datetime.utcnow().strftime('%d-%m-%Y')

# Columns in the returned raw data
column_names = ['NameLink', 'Country', 'Genre', 'Status', 'Scraped']

# Connect to RDS
rds_engine = db_connect()


#letters = db_select_all('')
# Valid inputs for the `letter` parameter of the URL are NBR, ~, or A through Z
letters = 'NBR ~ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
#letters = 'Z'

#bandlog = pd.read_sql("select * from BandLog order by LastScraped desc, Letter limit 2", rds_engine)
bandlog_recent = pd.read_sql("""
select t1.Letter, t2.ScrapeDate
from BandLog t1
inner join (
	select Letter, max(ScrapeDate) ScrapeDate
    from BandLog
    group by Letter
) t2
on t1.Letter = t2.Letter
""")
print(bandlog_recent)

bandlog = pd.merge(bandlog_recent, letters, how = "outer")

# Store these so we can batch update at the end
bandlog_scrape_date = bandlog['LastScraped']

try:
    for index, row in bandlog.iterrows():
        # SCRAPE BANDS
        bands_raw = scrape_metalarchives(row['Letter'], get_band, tidy_band, column_names, response_len)

        # Record time this letter finished scraping
        last_scraped[index] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

finally:
    # Update scraping log
    bandlog['LastScraped'] = last_scraped
    bandlog.sort_values('LastScraped', ascending = False, inplace = True)
    db_insert_into(bandlog, 'Log_Band', rds_engine, operation = 'replace')

    # Close connection
    rds_engine.dispose()

    print('Complete!')


