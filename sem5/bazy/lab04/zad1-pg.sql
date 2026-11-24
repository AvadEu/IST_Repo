-- zad1 (CASE bez ELSE -> NULL tam, gdzie funkcja nie wystepuje w bandzie)
SELECT funkcja                                                                                      AS "FUNKCJA",
       SUM(CASE WHEN nazwa = 'CZARNI RYCERZE' THEN przydzial_myszy + COALESCE(myszy_extra, 0) END) AS "Banda CZARNI RYCERZE",
       SUM(CASE WHEN nazwa = 'BIALI LOWCY' THEN przydzial_myszy + COALESCE(myszy_extra, 0) END)    AS "Banda BIALI LOWCY"
FROM Kocury
         JOIN Bandy USING (nr_bandy)
WHERE funkcja <> 'SZEFUNIO'
GROUP BY funkcja
ORDER BY 1;


-- zad2 (SUM z 1 zamiast COUNT -> pusta komorka zamiast 0, jak w przykladzie)
SELECT funkcja                                                                                      AS "FUNKCJA",
       plec                                                                                         AS "P",
       SUM(CASE WHEN nazwa = 'CZARNI RYCERZE' THEN przydzial_myszy + COALESCE(myszy_extra, 0) END) AS "Banda CZARNI RYCERZE",
       SUM(CASE WHEN nazwa = 'CZARNI RYCERZE' THEN 1 END)                                           AS "Ile",
       SUM(CASE WHEN nazwa = 'BIALI LOWCY' THEN przydzial_myszy + COALESCE(myszy_extra, 0) END)    AS "Banda BIALI LOWCY",
       SUM(CASE WHEN nazwa = 'BIALI LOWCY' THEN 1 END)                                              AS "Ile"
FROM Kocury
         JOIN Bandy USING (nr_bandy)
WHERE funkcja <> 'SZEFUNIO'
GROUP BY funkcja, plec
ORDER BY 1, 2;


-- zad3 z zabezpieczeniem
SELECT f.funkcja                                                                         AS "FUNKCJA",
       COUNT(k.pseudo)                                                                   AS "KOTY",
       COALESCE(SUM(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)), 0)                 AS "RAZEM",
       TRIM_SCALE(ROUND(AVG(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)), 4))                    AS "SREDNIA"
FROM Funkcje f
         LEFT JOIN Kocury k ON f.funkcja = k.funkcja
GROUP BY f.funkcja
ORDER BY 1;

-- zad3 a) bez zabezpieczenia: HONOROWA -> KOTY = 1, RAZEM = NULL
-- COUNT(*) liczy wiersz dolozony przez LEFT JOIN (same NULL-e), SUM z samych NULL-i to NULL
SELECT f.funkcja                                                       AS "FUNKCJA",
       COUNT(*)                                                        AS "KOTY",
       SUM(k.przydzial_myszy + COALESCE(k.myszy_extra, 0))             AS "RAZEM",
       TRIM_SCALE(ROUND(AVG(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)), 4))  AS "SREDNIA"
FROM Funkcje f
         LEFT JOIN Kocury k ON f.funkcja = k.funkcja
GROUP BY f.funkcja
ORDER BY 1;

-- zad3 a) bez zabezpieczenia (INNER JOIN): HONOROWA znika z wyniku
SELECT funkcja                                                  AS "FUNKCJA",
       COUNT(*)                                                 AS "KOTY",
       SUM(przydzial_myszy + COALESCE(myszy_extra, 0))          AS "RAZEM",
       TRIM_SCALE(ROUND(AVG(przydzial_myszy + COALESCE(myszy_extra, 0)), 4)) AS "SREDNIA"
FROM Funkcje
         JOIN Kocury USING (funkcja)
GROUP BY funkcja
ORDER BY 1;


-- zad4 (zlaczenie z JACKIEM zamiast podzapytania)
SELECT k.imie AS "IMIE", k.w_stadku_od AS "POLUJE OD"
FROM Kocury k
         JOIN Kocury j ON j.imie = 'JACEK' AND k.w_stadku_od < j.w_stadku_od
ORDER BY k.w_stadku_od DESC;
