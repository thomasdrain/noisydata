from bs4 import BeautifulSoup
import re
import pandas as pd


def tidy_discog(raw_dat, band_ids):

    # Turn raw output into a clean tabular output
    soup = BeautifulSoup(raw_dat.text, 'html.parser')
    table = soup.find('table')  # Grab the first table
    discogs = table.find_all('tr')
    new_table = pd.DataFrame(data='', columns=['BandID', 'AlbumName', 'AlbumType', 'AlbumYear', 'Reviews', 'Rating'],
                             index=range(0, len(discogs) - 1))

    new_table[new_table.columns[0]] = band_ids

    # Tidy up each row (album)
    discog_marker = 0
    for discog in discogs[1:]:  # we can ignore the header row
        column_marker = 1  # start appending data from col 1, after band ID
        columns = discog.find_all('td')
        for column in columns:
            new_table.iat[discog_marker, column_marker] = column.get_text().strip()
            column_marker += 1

        # If there's at least one review, the <td> will have the form '2 (67%)',
        # which denote the number of reviews and average rating.
        # Extract these into their own columns.
        tmp_review_col = new_table.iat[discog_marker, 4]
        if tmp_review_col != '':
            new_table.iat[discog_marker, 4] = re.sub("(\\d+) \\(\\d+%\\)*$", "\\1", tmp_review_col)
            new_table.iat[discog_marker, 5] = re.sub("\\d+ \\((\\d+%)\\)*$", "\\1", tmp_review_col)

        discog_marker += 1

    return new_table

    # Empty list which will hold all the individual discographies
    # albums_list = []
    # band_counter = 0
    #
    # print("Getting albums from {} bands".format(len(band_ids)))
    #
    # for band in band_ids:
    #     if band_counter % 10 == 0:
    #         print("Fetching albums from bands: {} - {}".format(band_counter, band_counter + 9))
    #
    #     # Scrape this band's discography
    #     band_albums = get_album(band)
    #
    #     # Append to list of discographies
    #     albums_list.append(band_albums)
    #
    #     # Obeying their robots.txt "Crawl-delay: 3"
    #     if band_counter % 10 == 0:
    #         time.sleep(3)
    #
    #     band_counter += 1
    #
    # all_albums = pd.concat(albums_list)
    # return all_albums

print(tidy_discog())

