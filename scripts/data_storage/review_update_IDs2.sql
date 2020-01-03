# a one-to-one mapping between reviewlog and review
# only works when there's only one scrape per month 
# (as is the case when I ran this first time)
update Review r
inner join ReviewLog l
on DATE_FORMAT(r.ReviewDate,'%Y-%m') = l.Month
and r.Review_ScrapeID is null
set r.Review_ScrapeID = l.Review_ScrapeID;

select *
from Review
where Review_ScrapeID is null;