
import get_album as ga
import pandas as pd
import time

def tidy_album(band_ids):

    # Empty list which will hold all the individual discographies
    albums_list = []
    band_counter = 0

    print("Getting albums from {} bands".format(len(band_ids)))

    for band in band_ids:
        if band_counter % 10 == 0:
            print("Fetching albums from bands: {} - {}".format(band_counter, band_counter + 9))

        # Scrape this band's discography
        band_albums = ga.get_album(band)

        # Append to list of discographies
        albums_list.append(band_albums)

        # Obeying their robots.txt "Crawl-delay: 3"
        if band_counter % 10 == 0:
            time.sleep(3)

        band_counter += 1

    all_albums = pd.concat(albums_list)
    return all_albums