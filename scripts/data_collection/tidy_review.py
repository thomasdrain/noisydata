from bs4 import BeautifulSoup
import pandas as pd
import re


def tidy_review(raw_dat, month):

    #review_titles = []
    #reviews = []
    review_links = []
    band_links = []
    album_links = []
    user_links = []

    # Go into each review record, access the URL and get the review text itself
    # Fetching review content
    for n, link in enumerate(raw_dat.loc[:, 'ReviewLink_html']):
        # time.sleep(1)
        # print('Review #', n + 1)
        # Get the web addresses from the review, band, album and user HTML soups
        review_link_soup = BeautifulSoup(link, 'html.parser')
        review_links.append(review_link_soup.a['href'])

        # Go into the review page itself
        # review_page = get_url(review_links[n])
        # review_page.encoding = 'UTF-8'

        # Grab the title and content
        # review_soup = BeautifulSoup(review_page.text, 'html.parser')
        # review_title = review_soup.find_all('h3')[0].text.strip()#[:-6]
        # review_titles.append(review_title)
        #
        # review = review_soup.find_all('div', {'class': 'reviewContent'})[0].text
        # reviews.append(review)

    # Fetching band IDs
    for n, link in enumerate(raw_dat.loc[:, 'BandLink_html']):
        band_link_soup = BeautifulSoup(link, 'html.parser')
        band_links.append(band_link_soup.a['href'])

    # Fetching album IDs
    for n, link in enumerate(raw_dat.loc[:, 'AlbumLink_html']):
        album_link_soup = BeautifulSoup(link, 'html.parser')
        album_links.append(album_link_soup.a['href'])

    # Fetching usernames
    for n, link in enumerate(raw_dat.loc[:, 'UserLink_html']):
        user_link_soup = BeautifulSoup(link, 'html.parser')
        user_links.append(user_link_soup.a['href'])

    # Combine the date/time fields into a datetime we can use in database
    # this seems a lot harder than it should be...

    # the month parameter is easier to pass in than ReviewDate. The latter is in format 'July 29',
    # and doesn't hold the year either.
    yyyy_mm = month
    date_of_month = raw_dat.loc[:, 'ReviewDate'].replace("^(.+) (\\d+)$", "-\\2 ", regex=True).values
    hh_mm = raw_dat.loc[:, 'ReviewTime'].values
    # seconds placeholder (setting to :00 as no data stored on this
    ss_placeholder = ":00"
    dates_tmp = pd.DataFrame({'yyyy_mm': yyyy_mm,
                              'dd': date_of_month,
                              'hh_MM': hh_mm,
                              'ss': ss_placeholder})
    combo_date = dates_tmp.loc[:, 'yyyy_mm'].map(str) + \
                 dates_tmp.loc[:, 'dd'].map(str) + \
                 dates_tmp.loc[:, 'hh_MM'].map(str) + \
                 dates_tmp.loc[:, 'ss'].map(str)
    raw_dat.loc[:, 'ReviewDate'] = combo_date.apply(pd.to_datetime).values
    raw_dat.reset_index(drop=True, inplace=True)

    # Extract the corresponding IDs from each of the link fields
    # raw_dat['ReviewID'] = [int(re.sub("^.+/(\\d+)$", "\\1", r)) for r in review_links]
    # raw_dat['bandid'] = [int(re.sub("^.+/(\\d+)$", "\\1", b)) for b in band_links]
    for n, b in enumerate(band_links):
        try:
            # This is the only current issue I've found; a couple of reviews have no band ID in the url
            # because they've been deleted.
            raw_dat.loc[n, 'BandID'] = int(re.sub("^.+/(\\d+)$", "\\1", b))
        except Exception as e:
            print("Exception (no band ID? Try searching the raw data for '/\' where the ID is missing/deleted): ")
            print(e)
            continue

    raw_dat.loc[:, 'AlbumID'] = [int(re.sub("^.+/(\\d+)$", "\\1", a)) for a in album_links]
    raw_dat.loc[:, 'Username'] = [re.sub("^.+/(.+)$", "\\1", u) for u in user_links] # note that username is a text field
    raw_dat.loc[:, 'ReviewLink'] = review_links
    raw_dat.loc[:, 'ReviewScore'] = [int(re.sub("\\%", "", s)) for s in raw_dat['ReviewScore']]

    # We will worry about these later!
    # raw_dat['ReviewTitle'] = review_titles
    # raw_dat['ReviewContent'] = reviews

    # This will be filled in in the main script
    raw_dat.loc[:, 'Review_ScrapeID'] = None
    
    # Currently all we're filtering out are the one or two null band IDs
    # which seem to correspond to reviews deleted but still appearing in the JSON
    filter_rows = raw_dat['BandID'].notnull()

    # Return final dataset
    tidy_dat = raw_dat.loc[filter_rows,
                           ['BandID', 'AlbumID', 'Username', 'ReviewDate',
                            'ReviewLink', 'ReviewScore', 'Review_ScrapeID']]
    # Current index corresponds to index in smaller chunks concatenated
    # Reset index to start at 0 and end at number of bands
    tidy_dat.index = range(len(tidy_dat))

    return tidy_dat
