from bs4 import BeautifulSoup
import re


def tidy_band(raw_dat, letter):

    # Pull apart the attributes of interest from the link field
    link_soup = [BeautifulSoup(text, 'html.parser') for text in raw_dat['BandLink']]
    raw_dat['BandLink'] = [soup.a['href'] for soup in link_soup]
    raw_dat['BandName'] = [soup.a.string for soup in link_soup]

    raw_dat['BandID'] = [int(re.sub(".+/(.+)$", "\\1", link)) for link in raw_dat['BandLink']]

    # Pull apart the attribute of interest ('Status') from the link field
    status_soup = [BeautifulSoup(text, 'html.parser') for text in raw_dat['BandStatus']]
    raw_dat['BandStatus'] = [soup.span.string for soup in status_soup]

    # Store the letter with the band (this is the natural key of the band log table),
    # so we can match this table to band log and add in the scrape ID
    raw_dat['Letter'] = letter

    # This will be filled in in the main script
    raw_dat['Band_ScrapeID'] = None

    tidy_dat = raw_dat[['BandID', 'BandName', 'BandLink', 'BandStatus', 'Country', 'Genre', 'Letter', 'Band_ScrapeID']]
    # Current index corresponds to index in smaller chunks concatenated
    # Reset index to start at 0 and end at number of bands
    tidy_dat.index = range(len(tidy_dat))

    return tidy_dat
