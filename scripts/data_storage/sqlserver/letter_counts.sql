/* count how many records stored per scrape*/
  select l.ScrapeDate, l.Band_ScrapeID, l.Letter, count(b.Band_ScrapeID) N
  from metalarchives.dbo.Band b
  full join metalarchives.dbo.bandlog l on b.Band_ScrapeID = l.Band_ScrapeID
  group by l.ScrapeDate, l.Band_ScrapeID, l.Letter 
  order by l.ScrapeDate, l.Band_ScrapeID, l.Letter
  ;
