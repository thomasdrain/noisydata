DROP TABLE REVIEW;
DROP SEQUENCE REVIEW_SEQ;

CREATE SEQUENCE review_seq START WITH 1;

CREATE TABLE REVIEW (
    REVIEW_RECORDID     NUMBER(10)      NOT NULL,
    BANDID              NUMBER(10)      NOT NULL,
    ALBUMID             NUMBER(10)      NOT NULL,
    USERNAME            VARCHAR2(255)   NOT NULL,
    REVIEWDATE          DATE            NOT NULL,
    REVIEWLINK          VARCHAR2(255),
    REVIEWSCORE         INT,
    REVIEW_SCRAPEID     NUMBER(10)
);

ALTER TABLE REVIEW ADD (
    CONSTRAINT REVIEW_RECORDID PRIMARY KEY (REVIEW_RECORDID)
);

CREATE OR REPLACE TRIGGER review_trg
BEFORE INSERT ON REVIEW
FOR EACH ROW

BEGIN
    SELECT review_seq.NEXTVAL
    INTO :new.Review_RecordID
    FROM Dual;
END;