--drop view vw_Review_Counts;
-- IN PROGRESS

create view vw_Review_Counts as
select 
	--DATE_FORMAT(r.ReviewDate,'%Y-%m') as 
		ReviewMonth,
    count(*) as Num_Reviews
from Review r
inner join (
	select ReviewMonth, max(Review_ScrapeID) Review_ScrapeID
	from ReviewLog
	group by ReviewMonth
) l
on	--DATE_FORMAT(r.ReviewDate,'%Y-%m') = l.ReviewMonth
	r.ReviewDate = l.ReviewMonth
	and r.Review_ScrapeID = l.Review_ScrapeID
group by 
	--DATE_FORMAT(r.ReviewDate,'%Y-%m')
	r.ReviewDate
--order by year(ReviewDate), month(ReviewDate)