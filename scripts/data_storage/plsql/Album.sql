DROP TABLE ALBUM;
DROP SEQUENCE ALBUM_SEQ;

CREATE SEQUENCE album_seq START WITH 1;

CREATE TABLE ALBUM (
    Album_RecordID      NUMBER(10)          NOT NULL,
    AlbumID             NUMBER(10)          NOT NULL,
    BandID              NUMBER(10)          NOT NULL,
    AlbumName           VARCHAR2(255),
    AlbumType           VARCHAR2(255),
    AlbumYear           VARCHAR2(255),
    Reviews             NUMBER(10),
    Rating              NUMBER(10),
    AlbumLink           VARCHAR2(500)       NOT NULL,
    Discog_ScrapeID     NUMBER(10)
);

ALTER TABLE ALBUM ADD (
    CONSTRAINT Album_RecordID PRIMARY KEY (Album_RecordID));
    
CREATE OR REPLACE TRIGGER album_trg
BEFORE INSERT ON ALBUM
FOR EACH ROW

BEGIN
    SELECT album_seq.NEXTVAL
    INTO :new.Album_RecordID
    FROM Dual;
END;