## Update the review records which don't have a scrape ID
## with the scrape ID of the most recent scrape (from ReviewLog)

select l.Review_ScrapeID, b.*
from Review b
#update Review b
# get the most recent record for each Review that doesn't have a scrape ID
inner join (
	select BandID, AlbumID, Username, ReviewDate, max(Review_RecordID) Review_RecordID
    from Review
    group by BandID, AlbumID, Username, ReviewDate
) m		
on m.BandID = b.BandID
and m.AlbumID = b.AlbumID
and m.Username = b.Username
and m.ReviewDate = b.ReviewDate
and m.Review_RecordID = b.Review_RecordID
and b.Review_ScrapeID is null
# join on the Review_scrapeID
left join ReviewLog l
on l.Month = b.Month
# grab the most recent scrape date
inner join (
	select Month, max(ScrapeDate) ScrapeDate
    from ReviewLog
    group by Month
) l2 	
on l.Month = l2.Month
and l.ScrapeDate = l2.ScrapeDate

#set b.Review_ScrapeID = l.Review_ScrapeID