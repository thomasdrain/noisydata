-- Get the latest record for each review
create view vw_Review as

	select t1.*
	from Review t1
	inner join (
		select BandID, AlbumID, Username, ReviewDate, max(Review_ScrapeID) Review_ScrapeID
		from Review
		group by BandID, AlbumID, Username, ReviewDate
	) t2 on t1.BandID = t2.BandID
	and t1.AlbumID = t2.AlbumID
	and t1.Username = t2.Username
	and t1.ReviewDate = t2.ReviewDate
	and t1.Review_ScrapeID = t2.Review_ScrapeID
;

