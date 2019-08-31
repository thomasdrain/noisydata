


import get_url as gu


def get_band(letter='A', start=0, length=500):
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