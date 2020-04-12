# Author: Thomas Drain
# Year: 2020

# Get function which calls the table containing all albums for one band.
# This table contains rudimentary info like album type, average rating
# (at time of scraping), year etc.

from data_collection.get_url import get_url


def get_discog(band_id):
    discog_url = 'https://www.metal-archives.com/band/discography/id/' + band_id + '/tab/all'
    r = get_url(discog_url)

    return r
