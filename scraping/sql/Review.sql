create table metalarchives.Review (
    Review_RecordID bigint primary key not null auto_increment,
    ReviewID bigint, #foreign
    BandID bigint, #foreign
    AlbumID bigint, #foreign
    UserID bigint, #foreign, we aren't actively scraping yet
/*
variables I'm getting from the scrape, e.g. review itself, title, rating
*/
    Review_ScrapeID bigint #foreign
);