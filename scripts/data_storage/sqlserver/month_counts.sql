/* count how many records stored per scrape*/
  select l.ScrapeDate, l.Review_ScrapeID, l.ReviewMonth, count(r.Review_ScrapeID) N
  from metalarchives.dbo.Review r
  full join metalarchives.dbo.ReviewLog l on r.Review_ScrapeID = l.Review_ScrapeID
  group by l.ScrapeDate, l.Review_ScrapeID, l.ReviewMonth
  order by l.ScrapeDate, l.Review_ScrapeID, l.ReviewMonth
  ;
