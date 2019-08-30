# Author: Thomas Drain, Jon Charest
# Year: 2019

# Script for scraping bands and associated information from metal-archives.com

# Approach:
# For each letter in the alphabet (including 'NBR'),
# call the scrape_MA() function which returns the review table data,
# then save to CSV.

from bs4 import BeautifulSoup
import datetime
import pandas as pd
import re
import scrape_MA as sma
import get_url as gu


def get_band_url(letter='A', start=0, length=500):
    """Gets the listings displayed as alphabetical tables on M-A for input
    `letter`, starting at `start` and ending at `start` + `length`.
    Returns a `Response` object. Data can be accessed by calling the `json()`
    method of the returned `Response` object."""

    band_url = 'http://www.metal-archives.com/browse/ajax-letter/json/1/l/' + letter

    band_payload = {'sEcho': 0,  # if not set, response text is not valid JSON
                    'iDisplayStart': start,  # set start index of band names returned
                    'iDisplayLength': length} # only response lengths of 500 work
    if start == 0:
        print('Current letter = ', letter)

    r = gu.get_url(band_url, payload = band_payload)
    return r


def get_album_url(band_id = '125'):
    discog_url = 'https://www.metal-archives.com/band/discography/id/' + band_id + '/tab/all'
    r = gu.get_url(discog_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table')  # Grab the first table
    albums = table.find_all('tr')
    new_table = pd.DataFrame(data = '', columns = ['Band ID', 'Name', 'Type', 'Year', 'Reviews', 'Rating'],
                             index = range(0, len(albums) - 1))

    new_table[new_table.columns[0]] = band_id

    album_marker = 0
    for album in albums[1:]: # we can ignore the header row
        column_marker = 1 # start appending data from col 1, after band ID
        columns = album.find_all('td')
        for column in columns:
            new_table.iat[album_marker, column_marker] = column.get_text().strip()
            column_marker += 1

        # If there's at least one review, the <td> will have the form '2 (67%)',
        # which denote the number of reviews and average rating
        tmp_review_col = new_table.iat[album_marker, 4]
        if tmp_review_col != '':
            new_table.iat[album_marker, 4] = re.sub("(\\d+) \\(\\d+%\\)*$", "\\1", tmp_review_col)
            new_table.iat[album_marker, 5] = re.sub("\\d+ \\((\\d+%)\\)*$", "\\1", tmp_review_col)

        album_marker += 1

    return new_table
    #return table

get_album_url().to_csv("data/album_tmp.csv")

response_len = 500
date_of_scraping = datetime.datetime.utcnow().strftime('%d-%m-%Y')

# Columns in the returned raw data
column_names = ['NameLink', 'Country', 'Genre', 'Status', 'Scraped']

# Valid inputs for the `letter` parameter of the URL are NBR, ~, or A through Z
#letters = 'NBR ~ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
letters = 'Z'

for letter in letters:
    raw = sma.scrape_MA(letter, get_band_url, response_len)

    # PUT ALL THIS IN TIDY() FUNCTION
    # Set informative names
    raw.columns = column_names

    namesoup = [BeautifulSoup(text, 'html.parser') for text in raw['NameLink']]

    raw['BandLink'] = [soup.a['href'] for soup in namesoup]
    raw['BandID'] = [re.sub(".+/(.+)$", "\\1", link) for link in raw['BandLink']]
    raw['BandName'] = [soup.a.string for soup in namesoup]

    statussoup = [BeautifulSoup(text, 'html.parser') for text in raw['Status']]
    raw['BandStatus'] = [soup.span.string for soup in statussoup]

    clean = raw[['BandID', 'BandName', 'BandLink', 'BandStatus', 'Country', 'Genre', 'Scraped']]
    # Current index corresponds to index in smaller chunks concatenated
    # Reset index to start at 0 and end at number of bands
    clean.index = range(len(clean))

    # Save to CSV
    f_name = 'data/MA-band-names_{}_{}.csv'.format(letter, date_of_scraping)
    print('Writing band data to csv file:', f_name)
    clean.to_csv(f_name)

    # PUT FOR LOOP HERE TO GET ALBUMS; WRITE NEW FUNCTION LIKE SCRAPE_MA WHICH INCLUDES SLEEP TIMES ETC??
print('Complete!')
