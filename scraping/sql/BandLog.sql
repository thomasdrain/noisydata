create table metalarchives.BandLog (
    Band_ScrapeID bigint primary key not null auto_increment,
    Letter varchar(10),
    ScrapeDate datetime,
    EndDate datetime,
    Completed varchar(10),
    Active varchar(10)
);

insert into metalarchives.BandLog (Letter)
values
	('NBR'),
	('~'),
	('A'),
	('B'),
	('C'),
	('D'),
	('E'),
	('F'),
	('G'),
	('H'),
	('I'),
	('J'),
	('K'),
	('L'),
	('M'),
	('N'),
	('O'),
	('P'),
	('Q'),
	('R'),
	('S'),
	('T'),
	('U'),
	('V'),
	('W'),
	('X'),
	('Y'),
	('Z')
;