create table BandLog (
    Band_ScrapeID bigint primary key not null auto_increment,
    Letter varchar(5) not null,
    ScrapeDate datetime,
    Completed varchar(1)
);

insert into BandLog (Letter)
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