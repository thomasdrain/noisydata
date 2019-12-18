create table metalarchives.Band (
    Band_RecordID bigint primary key not null auto_increment,
    BandID bigint, #foreign
    Name varchar(255),
    Link varchar(255),
    Status varchar(255),
    Country varchar(255),
    Genre varchar(255),
    Band_ScrapeID bigint
);