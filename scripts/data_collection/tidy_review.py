from bs4 import BeautifulSoup
from data_collection.get_url import get_url
import time
import pandas as pd
import re


def tidy_review(input, log_natural_key):

    #review_titles = []
    #reviews = []
    review_links = []
    band_links = []
    album_links = []
    user_links = []

    # Go into each review record, access the URL and get the review text itself
    print('Fetching review content...')
    for n, link in enumerate(input['ReviewLink_html']):
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

    print('Fetching band IDs...')
    for n, link in enumerate(input['BandLink_html']):
        band_link_soup = BeautifulSoup(link, 'html.parser')
        band_links.append(band_link_soup.a['href'])

    print('Fetching album IDs...')
    for n, link in enumerate(input['AlbumLink_html']):
        album_link_soup = BeautifulSoup(link, 'html.parser')
        album_links.append(album_link_soup.a['href'])

    print('Fetching usernames...')
    for n, link in enumerate(input['UserLink_html']):
        user_link_soup = BeautifulSoup(link, 'html.parser')
        user_links.append(user_link_soup.a['href'])

    # Store the month with the review (this is the natural key of the review log table),
    # so we can match this table to review log and add in the scrape ID
    input['Month'] = log_natural_key

    # Combine the date/time fields into a datetime we can use in database
    date_tmp = input['Date'].replace("^(.+) (\\d+)$", "-\\2 ", regex=True)
    input['ReviewDate'] = input['Month'].str.cat(others=[date_tmp.values,
                                                         input['Time'].values,
                                                         pd.Series(":00").repeat(len(input)).values])

    # Extract the corresponding IDs from each of the link fields
    #input['ReviewID'] = [int(re.sub("^.+/(\\d+)$", "\\1", r)) for r in review_links]
    input['BandID'] = [int(re.sub("^.+/(\\d+)$", "\\1", b)) for b in band_links]
    input['AlbumID'] = [int(re.sub("^.+/(\\d+)$", "\\1", a)) for a in album_links]
    input['Username'] = [re.sub("^.+/(.+)$", "\\1", u) for u in user_links] # note that Username is a text field
    input['ReviewLink'] = review_links

    # We will worry about these later!
    #input['ReviewTitle'] = review_titles
    #input['ReviewContent'] = reviews

    # Return final dataset
    output = input[[#'ReviewID',
                     'BandID', 'AlbumID', 'Username',
                    'ReviewDate', 'ReviewLink'#, 'ReviewTitle', 'ReviewContent'
                    ]]
    output.to_csv('review.csv')

    return output
