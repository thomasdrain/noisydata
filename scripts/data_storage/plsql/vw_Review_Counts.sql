drop view vw_Review_Counts;

create view vw_Review_Counts as
select 
	DATE_FORMAT(r.ReviewDate,'%Y-%m') as Month,
    count(*) as Num_Reviews
from Review r
inner join (
select Month, max(Review_ScrapeID) Review_ScrapeID
from ReviewLog
group by Month
) l
on DATE_FORMAT(r.ReviewDate,'%Y-%m') = l.Month
and r.Review_ScrapeID = l.Review_ScrapeID
group by DATE_FORMAT(r.ReviewDate,'%Y-%m')
order by year(ReviewDate), month(ReviewDate)