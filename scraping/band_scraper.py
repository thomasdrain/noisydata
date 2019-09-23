# Author: Thomas Drain, Jon Charest
# Year: 2019

# Script for scraping bands and associated information from metal-archives.com

# Approach:
# For each letter in the alphabet (including 'NBR'),
# call the scrape_MA() function which returns the review table data,
# then save to CSV.

import datetime
from scraping.get_band import get_band
from scraping.scrape_metalarchives import scrape_metalarchives
from scraping.tidy_band import tidy_band
from scraping.sql.db_connect import db_connect
from scraping.sql.db_insert_into import db_insert_into
from scraping.sql.db_select_all import db_select_all
from scraping.sql.db_update_log import db_update_log


#get_album().to_csv("data/album_tmp.csv")

response_len = 500
date_of_scraping = datetime.datetime.utcnow().strftime('%d-%m-%Y')

# Columns in the returned raw data
column_names = ['NameLink', 'Country', 'Genre', 'Status', 'Scraped']

# Connect to RDS
rds_engine = db_connect()

#letters = db_select_all('')
# Valid inputs for the `letter` parameter of the URL are NBR, ~, or A through Z
#letters = 'NBR ~ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
letters = 'Z'

for letter in letters:
    # SCRAPE BANDS
    bands_raw = scrape_metalarchives(letter, get_band, response_len)

    # Set informative names
    bands_raw.columns = column_names

    # Tidy up the raw scraped output
    bands_clean = tidy_band(bands_raw)

    # Write to RDS
    db_insert_into(bands_clean, 'Band', rds_engine)

    # Update scraping log
    #db_update_log('Log_Band')

rds_engine.dispose()
print('Complete!')


