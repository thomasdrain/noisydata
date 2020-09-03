create table metalarchives.dbo.ReviewLog (
    Review_ScrapeID		BIGINT				NOT NULL		PRIMARY KEY		IDENTITY(1,1),
	ReviewMonth			VARCHAR(100)		NOT NULL,
    ScrapeDate			DATE
);