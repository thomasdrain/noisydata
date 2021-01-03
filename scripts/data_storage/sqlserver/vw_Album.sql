-- Get the latest record for each discog
create view vw_Album as

	select t1.*
	from Album t1
	inner join (
		select BandID, max(Discog_ScrapeID) Discog_ScrapeID
		from Album
		group by BandID
	) t2 on t1.BandID = t2.BandID
	and t1.Discog_ScrapeID = t2.Discog_ScrapeID
;

