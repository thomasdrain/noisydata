create table metalarchives.BandAlbumsLog (
    BandAlbums_ScrapeID bigint primary key not null auto_increment,
    BandID bigint, #foreign
    ScrapeDate datetime,
    EndDate datetime,
    Completed varchar(10),
    Active varchar(10)    
);