-- zad11
SELECT LEVEL AS "Poziom", pseudo AS "Pseudonim", funkcja AS "Funkcja", nr_bandy AS "Nr bandy"
FROM Kocury
WHERE plec = 'M'
START WITH funkcja = 'BANDZIOR' AND plec = 'M'
CONNECT BY PRIOR pseudo = szef
ORDER SIBLINGS BY pseudo;


-- zad12 (dzis = 17 VII 2024)
SELECT LPAD(' ', 4 * LEVEL - 4) || pseudo AS "Droga sluzbowa"
FROM Kocury
START WITH plec = 'M'
       AND MONTHS_BETWEEN(DATE '2024-07-17', w_stadku_od) > 180
       AND myszy_extra IS NULL
CONNECT BY PRIOR szef = pseudo
ORDER SIBLINGS BY pseudo;


-- zad13 a) tylko zlaczenia (maks. 3 poziomy przelozonych)
SELECT k.imie   AS "Imie",   '|' AS " ",
       k.funkcja AS "Funkcja", '|' AS " ",
       s1.imie  AS "Szef 1", '|' AS " ",
       s2.imie  AS "Szef 2", '|' AS " ",
       s3.imie  AS "Szef 3"
FROM Kocury k
         LEFT JOIN Kocury s1 ON k.szef = s1.pseudo
         LEFT JOIN Kocury s2 ON s1.szef = s2.pseudo
         LEFT JOIN Kocury s3 ON s2.szef = s3.pseudo
WHERE k.funkcja IN ('KOT', 'MILUSIA');

-- zad13 b) drzewo; SUBSTR odcina z drogi segment korzenia (' | ' + 10 znakow)
SELECT CONNECT_BY_ROOT imie    AS "Imie",    '|' AS " ",
       CONNECT_BY_ROOT funkcja AS "Funkcja",
       SUBSTR(SYS_CONNECT_BY_PATH(RPAD(imie, 10), ' | '), 14) AS "Imiona kolejnych szefow"
FROM Kocury
WHERE CONNECT_BY_ISLEAF = 1
START WITH funkcja IN ('KOT', 'MILUSIA')
CONNECT BY PRIOR szef = pseudo;
