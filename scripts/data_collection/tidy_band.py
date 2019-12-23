from bs4 import BeautifulSoup
import re


def tidy_band(input, log_natural_key):
    namesoup = [BeautifulSoup(text, 'html.parser') for text in input['Link']]

    input['Link'] = [soup.a['href'] for soup in namesoup]
    input['BandID'] = [re.sub(".+/(.+)$", "\\1", link) for link in input['Link']]
    input['Name'] = [soup.a.string for soup in namesoup]

    statussoup = [BeautifulSoup(text, 'html.parser') for text in input['Status']]
    input['Status'] = [soup.span.string for soup in statussoup]

    # Store the letter with the band (this is the natural key of the band log table),
    # so we can match this table to band log and add in the scrape ID
    input['Letter'] = log_natural_key

    output = input[['BandID', 'Name', 'Link', 'Status', 'Country', 'Genre', 'Letter']]
    # Current index corresponds to index in smaller chunks concatenated
    # Reset index to start at 0 and end at number of bands
    output.index = range(len(output))

    return output
