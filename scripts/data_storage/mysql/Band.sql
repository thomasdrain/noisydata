create table metalarchives.Band (
    Band_RecordID bigint primary key not null auto_increment,
    BandID bigint not null, #foreign
    Name varchar(255),
    Link varchar(255),
    Status varchar(255),
    Country varchar(255),
    Genre varchar(255),
    Letter varchar(5) not null,
    Band_ScrapeID bigint
);