from bs4 import BeautifulSoup
import pandas as pd
import re
import sys


def tidy_review(raw_dat, month):

    #review_titles = []
    #reviews = []
    review_links = []
    band_links = []
    album_links = []
    user_links = []

    # Go into each review record, access the URL and get the review text itself
    # Fetching review content
    for n, link in enumerate(raw_dat['reviewlink_html']):
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
    for n, link in enumerate(raw_dat['bandlink_html']):
        band_link_soup = BeautifulSoup(link, 'html.parser')
        band_links.append(band_link_soup.a['href'])

    # Fetching album IDs
    for n, link in enumerate(raw_dat['albumlink_html']):
        album_link_soup = BeautifulSoup(link, 'html.parser')
        album_links.append(album_link_soup.a['href'])

    # Fetching usernames
    for n, link in enumerate(raw_dat['userlink_html']):
        user_link_soup = BeautifulSoup(link, 'html.parser')
        user_links.append(user_link_soup.a['href'])

    # Combine the date/time fields into a datetime we can use in database
    # this seems a lot harder than it should be...
    date_of_month = raw_dat['date'].replace("^(.+) (\\d+)$", "-\\2 ", regex=True).values
    hh_mm = raw_dat['time'].values
    # seconds placeholder (setting to :00 as no data stored on this
    ss_placeholder = ":00"
    dates_tmp = pd.DataFrame({'yyyy_mm' : month,
                              'dd': date_of_month,
                              'hh_MM': hh_mm,
                              'ss': ss_placeholder})
    combo_date = dates_tmp['yyyy_mm'].map(str) + \
                 dates_tmp['dd'].map(str) + \
                 dates_tmp['hh_MM'].map(str) + \
                 dates_tmp['ss'].map(str)
    raw_dat['reviewdate'] = combo_date.apply(pd.to_datetime)
    raw_dat.reset_index(drop=True, inplace=True)

    # Extract the corresponding IDs from each of the link fields
    # raw_dat['ReviewID'] = [int(re.sub("^.+/(\\d+)$", "\\1", r)) for r in review_links]
    # raw_dat['bandid'] = [int(re.sub("^.+/(\\d+)$", "\\1", b)) for b in band_links]
    for n, b in enumerate(band_links):
        try:
            raw_dat.loc[n, 'bandid'] = int(re.sub("^.+/(\\d+)$", "\\1", b))
        except Exception as e:
            print("Exception (no band ID? Try searching the raw data for '/\' where the ID is missing/deleted): ")
            print(e)
            continue

    raw_dat['albumid'] = [int(re.sub("^.+/(\\d+)$", "\\1", a)) for a in album_links]
    raw_dat['username'] = [re.sub("^.+/(.+)$", "\\1", u) for u in user_links] # note that username is a text field
    raw_dat['reviewlink'] = review_links
    raw_dat['reviewscore'] = [int(re.sub("\\%", "", s)) for s in raw_dat['score']]

    # We will worry about these later!
    # raw_dat['ReviewTitle'] = review_titles
    # raw_dat['ReviewContent'] = reviews

    # Store the letter with the band (this is the natural key of the band log table),
    # so we can match this table to band log and add in the scrape ID
    # Update: don't end up using this field anymore, need to remove from the tidy functions altogether
    # raw_dat['month'] = month
    
    # This will be filled in in the main script
    raw_dat['review_scrapeid'] = None
    
    # Return final dataset
    tidy_dat = raw_dat[['bandid', 'albumid', 'username',
                        'reviewdate', 'reviewlink', 'reviewscore',
                        'review_scrapeid']]
    # Current index corresponds to index in smaller chunks concatenated
    # Reset index to start at 0 and end at number of bands
    tidy_dat.index = range(len(tidy_dat))

    return tidy_dat
