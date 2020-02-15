SELECT * FROM metalarchives.ReviewLog;

update ReviewLog
set Completed = 'N'
where Month in (
"2008-05", 
"2008-08",
"2008-12",
"2009-03",
"2010-01",
"2010-06",
"2012-11",
"2012-12",
"2013-09"
)