DROP TABLE metalarchives.SCRAPING_LOG_BAND;

CREATE TABLE metalarchives.SCRAPING_LOG_BAND (
	Letter varchar(4),
    Last_Scrape datetime null
);

INSERT INTO metalarchives.SCRAPING_LOG_BAND (Letter)
VALUES 
	('NBR'), ('~'), ('A'), ('B'), ('C'), ('D'), ('E'), ('F'), ('G'), ('H'), ('I'), ('J'), 
    ('K'), ('L'), ('M'), ('N'), ('O'), ('P'), ('Q'), ('R'), ('S'), ('T'), ('U'), ('V'), 
    ('W'), ('X'), ('Y'), ('Z');
