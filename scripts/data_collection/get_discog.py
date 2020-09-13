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

    discog_url = 'https://www.metal-archives.com/band/discography/id/' + str(band) + '/tab/all'
    response = get_url(discog_url)

    # Turn raw output (a series of tables) into a clean tabular output
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')  # Grab the first table

    if table is None:
        print("* No such band ID")
        return None

    albums = table.find_all('tr')

    # If this message is displayed then the band has no recorded album - move on
    if albums[1].get_text().strip() == "Nothing entered yet. Please add the releases, if applicable.":
        print("* No albums listed")
        return None

    else:
        # Note: the order of these columns is important - watch the integer indexing below
        clean_dat = pd.DataFrame(data='', columns=['BandID', 'AlbumLink', 'AlbumID',
                                                   'AlbumName', 'AlbumType', 'AlbumYear',
                                                   'Reviews', 'Rating'],
                                 index=range(0, len(albums) - 1))

        # Set the band ID for these albums
        clean_dat[clean_dat.columns[0]] = band

        # Tidy up each row (album)
        album_counter = 0
        for album in albums[1:]:  # we can ignore the header row
            raw_columns = album.find_all('td')

            # Extract the album link/ID and then fill them in
            album_link = raw_columns[0].a['href']
            album_id = re.sub(".+/(\\d+)$", "\\1", album_link)
            clean_dat.iat[album_counter, 1] = album_link
            clean_dat.iat[album_counter, 2] = album_id

            # start appending data into our clean dataset from col 3
            # (after band ID, album ID and album link which we've already filled in)
            column_counter = 3

            # Put each <td> text into our clean dataset, sequentially
            for column in raw_columns:
                clean_dat.iat[album_counter, column_counter] = column.get_text().strip()
                column_counter += 1

            # If there's at least one review, the <td> will have the form '2 (67%)',
            # which denote the number of reviews and average rating.
            # Extract these into their own columns.
            tmp_review_col = clean_dat.loc[album_counter, 'Reviews']
            if tmp_review_col != '':
                # review count (the first set of digits before the space)
                review_count = re.sub("(\\d+) \\(\\d+%\\)*$", "\\1", tmp_review_col)
                clean_dat.loc[album_counter, 'Reviews'] = review_count

                # the rating (a number followed by a percentage sign)
                tmp_rating_col = re.sub("\\d+ \\((\\d+)%\\)*$", "\\1", tmp_review_col)
                rating = re.sub("(\\d+)%$", "\\1", tmp_rating_col)  # remove the % sign

                if review_count == 0:
                    clean_dat.loc[album_counter, 'Rating'] = None
                else:
                    clean_dat.loc[album_counter, 'Rating'] = rating

            album_counter += 1

        # This will be filled in in the main script
        clean_dat.loc[:, 'Discog_ScrapeID'] = None
        clean_dat.reset_index(drop=True, inplace=True)

        res = clean_dat[['BandID', 'AlbumID', 'AlbumName',
                         'AlbumType', 'AlbumYear', 'Reviews',
                         'Rating', 'AlbumLink', 'Discog_ScrapeID']]
        return res
