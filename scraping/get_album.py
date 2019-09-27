from bs4 import BeautifulSoup
import pandas as pd
import re
import get_url


def get_album(band_id = '125'):
    discog_url = 'https://www.metal-archives.com/band/discography/id/' + band_id + '/tab/all'
    r = get_url(discog_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table')  # Grab the first table
    albums = table.find_all('tr')
    new_table = pd.DataFrame(data = '', columns = ['BandID', 'AlbumName', 'AlbumType', 'AlbumYear', 'Reviews', 'Rating'],
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
        # which denote the number of reviews and average rating.
        # Extract these into their own columns.
        tmp_review_col = new_table.iat[album_marker, 4]
        if tmp_review_col != '':
            new_table.iat[album_marker, 4] = re.sub("(\\d+) \\(\\d+%\\)*$", "\\1", tmp_review_col)
            new_table.iat[album_marker, 5] = re.sub("\\d+ \\((\\d+%)\\)*$", "\\1", tmp_review_col)

        album_marker += 1

    return new_table
