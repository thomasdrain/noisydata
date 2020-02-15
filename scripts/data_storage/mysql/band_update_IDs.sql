## Update the band records which don't have a scrape ID
## with the scrape ID of the most recent scrape (from BandLog)

update Band b
# get the most recent record for each band that doesn't have a scrape ID
inner join (
	select BandID, max(Band_RecordID) Band_RecordID
    from Band
    group by BandID
) m		
on m.BandID = b.BandID 
and m.Band_RecordID = b.Band_RecordID
and b.Band_ScrapeID is null
# join on the band_scrapeID
left join BandLog l
on l.Letter = b.Letter
# grab the most recent scrape date
inner join (
	select Letter, max(ScrapeDate) ScrapeDate
    from BandLog
    group by Letter
) l2 	
on l.Letter = l2.Letter
and l.ScrapeDate = l2.ScrapeDate

set b.Band_ScrapeID = l.Band_ScrapeID