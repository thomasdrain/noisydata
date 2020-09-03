create table metalarchives.dbo.Review (
	Review_RecordID		BIGINT				NOT NULL		PRIMARY KEY		IDENTITY(1,1),
    BandID              BIGINT				NOT NULL,
	AlbumID				BIGINT				NOT NULL,
    Username			VARCHAR(1000),
    ReviewDate			DATE,
    ReviewLink          VARCHAR(1000),
    ReviewScore         INT,
    Genre				VARCHAR(1000),
    Review_ScrapeID		BIGINT
);