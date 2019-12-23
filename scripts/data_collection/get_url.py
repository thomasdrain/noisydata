#####
# get_url is a little workhorse designed to be used in scraping the
# bands, reviews and albums from Metal-Archives.
import requests

useragent_header = {'User-Agent': 'Mozilla/5.0'}

# header: The default used by noisydata is Mozilla, which prevents a 403 error.
# see https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
def get_url(url, payload = None, header = useragent_header):

    if payload != None:
        r = requests.get(url, params=payload, headers=header)
    else:
        r = requests.get(url, headers=header)
    return r
