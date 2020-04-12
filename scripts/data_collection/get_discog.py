# Author: Thomas Drain
# Year: 2020

# Get function which calls the table containing all albums for one band.
# This table contains rudimentary info like album type, average rating
# (at time of scraping), year etc.
# Then tidies up the output, unlike get_band and get_review
# which have an additional JSON decoding step.

from bs4 import BeautifulSoup
from data_collection.get_url import get_url
import re
import pandas as pd


def get_discog(band):
    discog_url = 'https://www.metal-archives.com/band/discography/id/' + band + '/tab/all'
    response = get_url(discog_url)

    # Turn raw output (a series of tables) into a clean tabular output
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')  # Grab the first table
    albums = table.find_all('tr')
    clean_dat = pd.DataFrame(data='', columns=['BandID', 'AlbumName', 'AlbumType', 'AlbumYear', 'Reviews', 'Rating'],
                             index=range(0, len(albums) - 1))

    # Set the band ID for these albums
    clean_dat[clean_dat.columns[0]] = band

    # Tidy up each row (album)
    album_marker = 0
    for album in albums[1:]:  # we can ignore the header row
        column_marker = 1  # start appending data from col 1, after band ID
        columns = album.find_all('td')
        for column in columns:
            clean_dat.iat[album_marker, column_marker] = column.get_text().strip()
            column_marker += 1

        # If there's at least one review, the <td> will have the form '2 (67%)',
        # which denote the number of reviews and average rating.
        # Extract these into their own columns.
        tmp_review_col = clean_dat.loc[album_marker, 'Reviews']
        if tmp_review_col != '':
            # review count (the first set of digits before the space)
            clean_dat.loc[album_marker, 'Reviews'] = re.sub("(\\d+) \\(\\d+%\\)*$", "\\1", tmp_review_col)

            # the rating (a number followed by a percentage sign)
            tmp_rating_col = re.sub("\\d+ \\((\\d+)%\\)*$", "\\1", tmp_review_col)
            clean_dat.loc[album_marker, 'Rating'] = re.sub("(\\d+)%$", "\\1", tmp_rating_col)

        album_marker += 1

    return clean_dat
