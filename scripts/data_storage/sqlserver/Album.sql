create table metalarchives.dbo.Album (
	Album_RecordID      BIGINT				NOT NULL		PRIMARY KEY		IDENTITY(1,1),
    AlbumID             BIGINT				NOT NULL,
    BandID              BIGINT				NOT NULL,
    AlbumName           VARCHAR(1000),
    AlbumType           VARCHAR(100),
    AlbumYear           VARCHAR(100),
    Reviews             BIGINT,
    Rating              BIGINT,
    AlbumLink           VARCHAR(1000)		NOT NULL,
    Discog_ScrapeID     BIGINT
);