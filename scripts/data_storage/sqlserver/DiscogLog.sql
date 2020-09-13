create table metalarchives.dbo.DiscogLog (
    Discog_ScrapeID		BIGINT		NOT NULL		PRIMARY KEY		IDENTITY(1,1),
	BandID				BIGINT		NOT NULL,
    ScrapeDate			DATETIME
);