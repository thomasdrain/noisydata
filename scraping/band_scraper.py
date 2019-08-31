# Author: Thomas Drain, Jon Charest
# Year: 2019

# Script for scraping bands and associated information from metal-archives.com

# Approach:
# For each letter in the alphabet (including 'NBR'),
# call the scrape_MA() function which returns the review table data,
# then save to CSV.

import datetime
import get_band as gb
import scrape_metalarchives as sma
from scraping import tidy_album as ta
import tidy_band as tb



#get_album_url().to_csv("data/album_tmp.csv")

response_len = 500
date_of_scraping = datetime.datetime.utcnow().strftime('%d-%m-%Y')

# Columns in the returned raw data
column_names = ['NameLink', 'Country', 'Genre', 'Status', 'Scraped']

# Valid inputs for the `letter` parameter of the URL are NBR, ~, or A through Z
#letters = 'NBR ~ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
letters = 'Z'

for letter in letters:
    # SCRAPE BANDS
    bands_raw = sma.scrape_metalarchives(letter, gb.get_band, response_len)

    # Set informative names
    bands_raw.columns = column_names

    # Tidy up the raw scraped output
    bands_clean = tb.tidy_band(bands_raw)

    # Save to CSV
    f_name_bands = 'data/bands/MA-band-names_{}_{}.csv'.format(letter, date_of_scraping)
    print('Writing band data to csv file:', f_name_bands)
    bands_clean.to_csv(f_name_bands)

    # SCRAPE ALBUMS
    albums = ta.tidy_album(bands_clean['BandID'][0:20])

    # Save to CSV
    f_name_albums = 'data/albums/MA-albums_{}_{}.csv'.format(letter, date_of_scraping)
    print('Writing album data to csv file:', f_name_albums)
    albums.to_csv(f_name_albums)

print('Complete!')


