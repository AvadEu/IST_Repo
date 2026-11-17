-- zad11 (dzis = 29 X 2024)
SELECT pseudo      AS "PSEUDO",
       w_stadku_od AS "W STADKU",
       (DATE_TRUNC('week',
                   DATE_TRUNC('month',
                              DATE_TRUNC('week',
                                         CASE
                                             WHEN EXTRACT(DAY FROM w_stadku_od) > 15
                                                 THEN DATE_TRUNC('month', DATE '2024-10-29') + INTERVAL '1 month'
                                             ELSE DATE '2024-10-29' END + INTERVAL '4 days'
                              ) + INTERVAL '2 days'
                   ) + INTERVAL '1 month - 3 days'
        ) + INTERVAL '2 days')::DATE AS "WYPLATA"
FROM Kocury
ORDER BY w_stadku_od;

-- zad11 (dzis = 31 X 2024)
SELECT pseudo      AS "PSEUDO",
       w_stadku_od AS "W STADKU",
       (DATE_TRUNC('week',
                   DATE_TRUNC('month',
                              DATE_TRUNC('week',
                                         CASE
                                             WHEN EXTRACT(DAY FROM w_stadku_od) > 15
                                                 THEN DATE_TRUNC('month', DATE '2024-10-31') + INTERVAL '1 month'
                                             ELSE DATE '2024-10-31' END + INTERVAL '4 days'
                              ) + INTERVAL '2 days'
                   ) + INTERVAL '1 month - 3 days'
        ) + INTERVAL '2 days')::DATE AS "WYPLATA"
FROM Kocury
ORDER BY w_stadku_od;


-- zad12
SELECT 'Liczba kotow=' || LPAD(COUNT(*)::TEXT, 3) ||
       ' lowi jako ' || RPAD(funkcja, 10) ||
       ' i zjada max.' || TO_CHAR(MAX(przydzial_myszy + COALESCE(myszy_extra, 0)), '999.99') ||
       ' myszy miesiecznie' AS "ZAD 12"
FROM Kocury
WHERE funkcja <> 'SZEFUNIO'
  AND plec <> 'M'
GROUP BY funkcja
HAVING AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) > 50
ORDER BY funkcja;


-- zad13
SELECT nr_bandy             AS "Nr bandy",
       plec                 AS "Plec",
       MIN(przydzial_myszy) AS "Minimalny przydzial"
FROM Kocury
GROUP BY nr_bandy, plec
ORDER BY nr_bandy, plec;
