CREATE TABLE Funkcje
(
    funkcja VARCHAR2(10) CONSTRAINT fu_funkcja_pk PRIMARY KEY,
    min_myszy NUMBER(3) CONSTRAINT fu_min_myszy_ch CHECK (min_myszy > 5),
    max_myszy NUMBER(3) CONSTRAINT fu_max_myszy_ch CHECK (max_myszy < 200),
    CONSTRAINT fu_max_min_ch CHECK (max_myszy >= min_myszy)
);

CREATE TABLE Wrogowie
(
    imie_wroga VARCHAR2(15) CONSTRAINT wr_imie_wroga_pk PRIMARY KEY,
    stopien_wrogosci NUMBER(2) CONSTRAINT wr_stopien_ch CHECK (stopien_wrogosci BETWEEN 1 AND 10),
    gatunek VARCHAR2(15),
    lapowka VARCHAR2(20)
);

CREATE TABLE Bandy
(
    nr_bandy NUMBER(2) CONSTRAINT ba_nr_bandy_pk PRIMARY KEY,
    nazwa VARCHAR2(20) CONSTRAINT ba_nazwa_nn NOT NULL,
    teren VARCHAR2(15) CONSTRAINT ba_teren_uq UNIQUE,
    szef_bandy VARCHAR2(15) CONSTRAINT ba_szef_bandy_uq UNIQUE
);

CREATE TABLE Kocury
(
    imie VARCHAR2(15) CONSTRAINT ko_imie_nn NOT NULL,
    plec VARCHAR2(1)  CONSTRAINT ko_plec_ch CHECK (plec IN ('M', 'D')),
    pseudo VARCHAR2(15) CONSTRAINT ko_pseudo_pk PRIMARY KEY,
    funkcja VARCHAR2(10) CONSTRAINT ko_funkcja_fk REFERENCES Funkcje(funkcja),
    szef VARCHAR2(15) CONSTRAINT ko_szef_fk REFERENCES Kocury(pseudo),
    w_stadku_od DATE DEFAULT SYSDATE,
    przydzial_myszy NUMBER(3),
    myszy_extra NUMBER(3),
    nr_bandy NUMBER(2) CONSTRAINT ko_nr_bandy_fk REFERENCES Bandy(nr_bandy)
);

CREATE TABLE Wrogowie_kocurow
(
    pseudo VARCHAR2(15) CONSTRAINT wk_pseudo_fk REFERENCES Kocury(pseudo),
    imie_wroga VARCHAR2(15) CONSTRAINT wk_imie_wroga_fk REFERENCES Wrogowie(imie_wroga),
    data_incydentu DATE CONSTRAINT wk_data_nn NOT NULL,
    opis_incydentu VARCHAR2(50),
    CONSTRAINT wk_pk PRIMARY KEY (pseudo, imie_wroga)
);

ALTER TABLE Bandy
    ADD CONSTRAINT ba_szef_bandy_fk FOREIGN KEY (szef_bandy) REFERENCES Kocury(pseudo);