create table metalarchives.dbo.Band (
	Band_RecordID		BIGINT				NOT NULL		PRIMARY KEY		IDENTITY(1,1),
    BandID              BIGINT				NOT NULL,
	Letter				VARCHAR(5)			NOT NULL,
    BandName			VARCHAR(1000),
    BandLink			VARCHAR(1000),
    BandStatus          VARCHAR(1000),
    Country             VARCHAR(1000),
    Genre				VARCHAR(1000),
    Band_ScrapeID		BIGINT
);