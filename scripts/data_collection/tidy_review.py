from bs4 import BeautifulSoup
from data_collection.get_url import get_url
import time
import pandas as pd
import re


def tidy_review(input, scrape):

    #review_titles = []
    #reviews = []
    review_links = []
    band_links = []
    album_links = []
    user_links = []

    # Go into each review record, access the URL and get the review text itself
    # Fetching review content
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

    # Fetching band IDs
    for n, link in enumerate(input['BandLink_html']):
        band_link_soup = BeautifulSoup(link, 'html.parser')
        band_links.append(band_link_soup.a['href'])

    # Fetching album IDs
    for n, link in enumerate(input['AlbumLink_html']):
        album_link_soup = BeautifulSoup(link, 'html.parser')
        album_links.append(album_link_soup.a['href'])

    # Fetching usernames
    for n, link in enumerate(input['UserLink_html']):
        user_link_soup = BeautifulSoup(link, 'html.parser')
        user_links.append(user_link_soup.a['href'])

    # Combine the date/time fields into a datetime we can use in database
    # this seems a lot harder than it should be...
    date_of_month = input['Date'].replace("^(.+) (\\d+)$", "-\\2 ", regex=True).values
    hh_MM = input['Time'].values
    # seconds placeholder (setting to :00 as no data stored on this
    ss_placeholder = ":00"
    dates_tmp = pd.DataFrame({'yyyy_mm' : scrape['Month'].repeat(len(date_of_month)),
                            'dd': date_of_month,
                            'hh_MM': hh_MM,
                            'ss': ss_placeholder})
    combo_date = dates_tmp['yyyy_mm'].map(str) + \
                 dates_tmp['dd'].map(str) + \
                 dates_tmp['hh_MM'].map(str) + \
                 dates_tmp['ss'].map(str)
    combo_date.reset_index(drop=True, inplace=True)
    input['ReviewDate'] = combo_date

    # Extract the corresponding IDs from each of the link fields
    # input['ReviewID'] = [int(re.sub("^.+/(\\d+)$", "\\1", r)) for r in review_links]
    input['BandID'] = [int(re.sub("^.+/(\\d+)$", "\\1", b)) for b in band_links]
    input['AlbumID'] = [int(re.sub("^.+/(\\d+)$", "\\1", a)) for a in album_links]
    input['Username'] = [re.sub("^.+/(.+)$", "\\1", u) for u in user_links] # note that Username is a text field
    input['ReviewLink'] = review_links
    input['ReviewScore'] = [int(re.sub("\\%", "", s)) for s in input['Score']]

    # We will worry about these later!
    # input['ReviewTitle'] = review_titles
    # input['ReviewContent'] = reviews

    # This is important! it allows us to match the record back to the log
    input['Review_ScrapeID'] = scrape['Review_ScrapeID']

    # Return final dataset
    output = input[['BandID', 'AlbumID', 'Username',
                    'ReviewDate', 'ReviewLink', 'ReviewScore',
                    'Review_ScrapeID']]
                    #, 'ReviewTitle', 'ReviewContent'
    #output.to_csv('review.csv')

    return output
