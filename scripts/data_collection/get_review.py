from scraping import get_url

def get_review(date = "2019-01", start=0, length=200):
    """Gets the review listings displayed as monthly tables on M-A for
    input `date`, starting at `start` and ending at `start` + `length`.
    Returns a `Response` object. Data can be accessed by calling the `json()`
    method of the returned `Response` object.
    Note: this can be done alphabetically, however to minimise calls I've
    used the monthly tables"""

    review_url = 'http://www.metal-archives.com/review/ajax-list-browse/by/date/selection/' + date + '/json/1'

    review_payload = {'sEcho': 1,
                      'iColumns': 7,
                      'iDisplayStart': start,
                      'iDisplayLength': length}
    if start == 0:
        print('Current month = ', date)

    r = get_url(review_url, payload = review_payload)

    return r
