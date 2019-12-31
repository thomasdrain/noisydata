create table metalarchives.Review (
    Review_RecordID bigint primary key not null auto_increment,
    #ReviewID bigint, #foreign it appears there isnt a review ID as such...
    BandID bigint, #foreign
    AlbumID bigint, #foreign
    Username varchar(255), #foreign
    ReviewDate datetime,
    ReviewLink varchar(500),
    ReviewScore int,
    #not storing these in sql currently
    #ReviewTitle varchar(255),
    #ReviewContent varchar(255),
    Review_ScrapeID bigint #foreign
);