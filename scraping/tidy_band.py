from bs4 import BeautifulSoup
import re

def tidy_band(input):
    namesoup = [BeautifulSoup(text, 'html.parser') for text in input['NameLink']]

    input['BandLink'] = [soup.a['href'] for soup in namesoup]
    input['BandID'] = [re.sub(".+/(.+)$", "\\1", link) for link in input['BandLink']]
    input['BandName'] = [soup.a.string for soup in namesoup]

    statussoup = [BeautifulSoup(text, 'html.parser') for text in input['Status']]
    input['BandStatus'] = [soup.span.string for soup in statussoup]

    output = input[['BandID', 'BandName', 'BandLink', 'BandStatus', 'Country', 'Genre', 'Scraped']]
    # Current index corresponds to index in smaller chunks concatenated
    # Reset index to start at 0 and end at number of bands
    output.index = range(len(output))

    return output
