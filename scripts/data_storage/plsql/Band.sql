DROP TABLE BAND;
DROP SEQUENCE BAND_SEQ;

CREATE SEQUENCE band_seq START WITH 1;

CREATE TABLE BAND (
    Band_RecordID   NUMBER(10)          NOT NULL,
    BandID          NUMBER(10)          NOT NULL, --foreign
    Name            VARCHAR2(255),
    Link            VARCHAR2(255),
    Status          VARCHAR2(255),
    Country         VARCHAR2(255),
    Genre           VARCHAR2(255),
    Letter          VARCHAR2(5)      NOT NULL,
    Band_ScrapeID   NUMBER(10)
);

ALTER TABLE BAND ADD (
    CONSTRAINT Band_RecordID PRIMARY KEY (Band_RecordID));
    
CREATE OR REPLACE TRIGGER band_trg
BEFORE INSERT ON BAND
FOR EACH ROW

BEGIN
    SELECT band_seq.NEXTVAL
    INTO :new.Band_RecordID
    FROM Dual;
END;