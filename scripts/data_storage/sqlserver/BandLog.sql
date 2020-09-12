create table metalarchives.dbo.BandLog (
    Band_ScrapeID   BIGINT				NOT NULL		PRIMARY KEY		IDENTITY(1,1),
	Letter			VARCHAR(5)			NOT NULL,
    ScrapeDate      DATETIME
);