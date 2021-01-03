-- Get the latest record for each band
create view vw_Band as

	select t1.*
	from Band t1
	inner join (
		select BandID, max(Band_ScrapeID) Band_ScrapeID
		from Band
		group by BandID
	) t2 on t1.BandID = t2.BandID
	and t1.Band_ScrapeID = t2.Band_ScrapeID
;