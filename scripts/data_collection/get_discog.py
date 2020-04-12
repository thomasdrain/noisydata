

from data_collection.get_url import get_url


def get_discog(band_id = '125'):
    discog_url = 'https://www.metal-archives.com/band/discography/id/' + band_id + '/tab/all'
    r = get_url(discog_url)

    return r
