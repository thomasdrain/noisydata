from bs4 import BeautifulSoup
from scraping import get_url
import datetime
import time


def tidy_review(input):

    review_titles = []
    reviews = []
    
    # Go into each review record, access the URL and get the review text itself
    print('Fetching review content...')
    for n, link in enumerate(input['ReviewLink']):
        time.sleep(3)
        print('Review #', n + 1)
        linksoup = BeautifulSoup(link, 'html.parser')
        review_page = get_url(linksoup.a['href'])
        review_page.encoding = 'UTF-8'
        review_soup = BeautifulSoup(review_page.text, 'html.parser')
        review_title = review_soup.find_all('h3')[0].text.strip()[:-6]
        review_titles.append(review_title)
        review = review_soup.find_all('div', {'class': 'reviewContent'})[0].text
        reviews.append(review)
    
    # Clean up resulting dataset
    output = input
    output['ReviewTitle'] = review_titles
    output['ReviewContent'] = reviews
    output['DateScraped'] = datetime.datetime.utcnow().strftime('%d-%m-%Y')

    return output