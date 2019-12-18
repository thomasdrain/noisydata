create table metalarchives.Album (
    Album_RecordID bigint primary key not null auto_increment,
    AlbumID bigint, #foreign
    BandID bigint, #foreign
/*
variables I'm getting from the scrape, e.g. name, genre, art
*/
    BandAlbums_ScrapeID bigint #foreign
);