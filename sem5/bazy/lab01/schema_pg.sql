BEGIN;

CREATE TABLE Funkcje
(
    funkcja VARCHAR(10) CONSTRAINT fu_funkcja_pk PRIMARY KEY,
    min_myszy NUMERIC(3) CONSTRAINT fu_min_myszy_ch CHECK (min_myszy > 5),
    max_myszy NUMERIC(3) CONSTRAINT fu_max_myszy_ch CHECK (max_myszy < 200),
    CONSTRAINT fu_max_min_ch CHECK (max_myszy >= min_myszy)
);

CREATE TABLE Wrogowie
(
    imie_wroga VARCHAR(15) CONSTRAINT wr_imie_wroga_pk PRIMARY KEY,
    stopien_wrogosci NUMERIC(2) CONSTRAINT wr_stopien_ch CHECK (stopien_wrogosci BETWEEN 1 AND 10),
    gatunek VARCHAR(15),
    lapowka VARCHAR(20)
);

CREATE TABLE Bandy
(
    nr_bandy NUMERIC(2) CONSTRAINT ba_nr_bandy_pk PRIMARY KEY,
    nazwa      VARCHAR(20) CONSTRAINT ba_nazwa_nn NOT NULL,
    teren      VARCHAR(15) CONSTRAINT ba_teren_uq UNIQUE,
    szef_bandy VARCHAR(15) CONSTRAINT ba_szef_bandy_uq UNIQUE
);

CREATE TABLE Kocury
(
    imie VARCHAR(15) CONSTRAINT ko_imie_nn NOT NULL,
    plec VARCHAR(1) CONSTRAINT ko_plec_ch CHECK (plec IN ('M', 'D')),
    pseudo VARCHAR(15) CONSTRAINT ko_pseudo_pk PRIMARY KEY,
    funkcja VARCHAR(10) CONSTRAINT ko_funkcja_fk REFERENCES Funkcje (funkcja),
    szef VARCHAR(15) CONSTRAINT ko_szef_fk REFERENCES Kocury (pseudo),
    w_stadku_od DATE DEFAULT CURRENT_DATE,
    przydzial_myszy NUMERIC(3),
    myszy_extra NUMERIC(3),
    nr_bandy NUMERIC(2) CONSTRAINT ko_nr_bandy_fk REFERENCES Bandy (nr_bandy)
);

CREATE TABLE Wrogowie_kocurow
(
    pseudo VARCHAR(15) CONSTRAINT wk_pseudo_fk REFERENCES Kocury (pseudo),
    imie_wroga     VARCHAR(15) CONSTRAINT wk_imie_wroga_fk REFERENCES Wrogowie (imie_wroga),
    data_incydentu DATE CONSTRAINT wk_data_nn NOT NULL,
    opis_incydentu VARCHAR(50),
    CONSTRAINT wk_pk PRIMARY KEY (pseudo, imie_wroga)
);

ALTER TABLE Bandy
    ADD CONSTRAINT ba_szef_bandy_fk FOREIGN KEY (szef_bandy) REFERENCES Kocury (pseudo);

COMMIT;