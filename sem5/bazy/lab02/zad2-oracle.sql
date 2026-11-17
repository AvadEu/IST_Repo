-- zad11 (dzis = 29 X 2024)
SELECT pseudo      AS "PSEUDO",
       w_stadku_od AS "W STADKU",
       NEXT_DAY(LAST_DAY(NEXT_DAY(CASE
                                      WHEN EXTRACT(DAY FROM w_stadku_od) > 15
                                          THEN LAST_DAY(DATE '2024-10-29') + 1
                                      ELSE DATE '2024-10-29' END - 1, 'WEDNESDAY')) - 7,
                'WEDNESDAY') AS "WYPLATA"
FROM Kocury
START WITH szef IS NULL
CONNECT BY PRIOR pseudo = szef
ORDER BY w_stadku_od;

-- zad11 (dzis = 31 X 2024)
SELECT pseudo      AS "PSEUDO",
       w_stadku_od AS "W STADKU",
       NEXT_DAY(LAST_DAY(NEXT_DAY(CASE
                                      WHEN EXTRACT(DAY FROM w_stadku_od) > 15
                                          THEN LAST_DAY(DATE '2024-10-31') + 1
                                      ELSE DATE '2024-10-31' END - 1, 'WEDNESDAY')) - 7,
                'WEDNESDAY') AS "WYPLATA"
FROM Kocury
START WITH szef IS NULL
CONNECT BY PRIOR pseudo = szef
ORDER BY w_stadku_od;


-- zad12
SELECT 'Liczba kotow=' || LPAD(COUNT(*), 3) ||
       ' lowi jako ' || RPAD(funkcja, 10) ||
       ' i zjada max.' || TO_CHAR(MAX(przydzial_myszy + NVL(myszy_extra, 0)), '999.99') ||
       ' myszy miesiecznie' AS "ZAD 12"
FROM Kocury
WHERE funkcja <> 'SZEFUNIO'
  AND plec <> 'M'
GROUP BY funkcja
HAVING AVG(przydzial_myszy + NVL(myszy_extra, 0)) > 50
ORDER BY funkcja;


-- zad13
SELECT nr_bandy             AS "Nr bandy",
       plec                 AS "Plec",
       MIN(przydzial_myszy) AS "Minimalny przydzial"
FROM Kocury
GROUP BY nr_bandy, plec
ORDER BY nr_bandy, plec;
