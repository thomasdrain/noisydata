create table metalarchives.Review (
    Review_RecordID bigint primary key not null auto_increment,
    ReviewID bigint, #foreign
    BandID bigint, #foreign
    AlbumID bigint, #foreign
    UserID bigint, #foreign, we aren't actively scraping yet
    ReviewDate datetime,
    Link varchar(255),
    Review_ScrapeID bigint #foreign
);