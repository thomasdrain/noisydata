def unpack_bands(dat):

    date_of_scraping = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    f_name = 'data/MA-band-names_{}.csv'.format(date_of_scraping)
    print('Writing band data to csv file:', f_name)
    dat.to_csv(f_name)
    print('Complete!')