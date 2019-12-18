create table metalarchives.ReviewLog (
    Review_ScrapeID bigint primary key not null auto_increment,
    Month varchar(10),
    ScrapeDate datetime,
    EndDate datetime,
    Completed varchar(10),
    Active varchar(10)    
);