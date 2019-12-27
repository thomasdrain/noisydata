from bs4 import BeautifulSoup
from data_collection.get_url import get_url
import datetime
import time
import pandas as pd

def tidy_review(input, log_natural_key):

    review_titles = []
    reviews = []
    
    # Go into each review record, access the URL and get the review text itself
    print('Fetching review content...')
    for n, link in enumerate(input['ReviewLink']):
        time.sleep(1)
        print('Review #', n + 1)
        review_link_soup = BeautifulSoup(link, 'html.parser')
        review_page = get_url(review_link_soup.a['href'])
        review_page.encoding = 'UTF-8'

        review_soup = BeautifulSoup(review_page.text, 'html.parser')
        review_title = review_soup.find_all('h3')[0].text.strip()[:-6]
        review_titles.append(review_title)

        review = review_soup.find_all('div', {'class': 'reviewContent'})[0].text
        reviews.append(review)

    # Store the month with the review (this is the natural key of the review log table),
    # so we can match this table to review log and add in the scrape ID
    input['Letter'] = log_natural_key

    # Clean up resulting dataset
    output = input
    output['ReviewTitle'] = review_titles
    output['ReviewContent'] = reviews
    output['DateScraped'] = datetime.datetime.utcnow().strftime('%d-%m-%Y')

    # TODO:
    # 1) REPLACE DATE AND TIME WITH A REVIEWDATE FIELD (DATETIME)
    # 2) EXTRACT BAND ID FROM BAND LINK (THE NUMBER AFTER THE LAST SLASH)
    # 3) EXTRACT USERNAME FROM REVIEWLINK (THE TEXT AFTER THE LAST SLASH)

    output.to_csv('review.csv')

    return output
