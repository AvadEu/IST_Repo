-- zad9 NOT EXISTS zamiast NOT IN (szef TYGRYSA = NULL wyzerowalby NOT IN)
SELECT k.pseudo AS "Do przeczolgania", b.nazwa AS "Nazwa bandy"
FROM Kocury k
         JOIN Bandy b ON k.nr_bandy = b.nr_bandy
         JOIN Funkcje f ON k.funkcja = f.funkcja
WHERE NOT EXISTS (SELECT 1 FROM Kocury p WHERE p.szef = k.pseudo)
  AND EXISTS (SELECT 1 FROM Wrogowie_kocurow wk WHERE wk.pseudo = k.pseudo)
  AND k.przydzial_myszy >= f.min_myszy + (f.max_myszy - f.min_myszy) / 3
ORDER BY 2, 1;


-- zad10 >= ALL / <= ALL zamiast MAX(AVG(...)) - PostgreSQL nie zagniezdza funkcji grupowych
SELECT funkcja                                                                  AS "Funkcja",
       ROUND(AVG(COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0)))      AS "Srednio najw. i najm. myszy"
FROM Kocury
WHERE funkcja <> 'SZEFUNIO'
GROUP BY funkcja
HAVING AVG(COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0)) >= ALL
       (SELECT AVG(COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0))
        FROM Kocury
        WHERE funkcja <> 'SZEFUNIO'
        GROUP BY funkcja)
    OR AVG(COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0)) <= ALL
       (SELECT AVG(COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0))
        FROM Kocury
        WHERE funkcja <> 'SZEFUNIO'
        GROUP BY funkcja)
ORDER BY 2;


-- zad11 a) zlaczenie bez podzapytan: kazdy kocur laczony ze wszystkimi kotami swojej bandy
SELECT k.imie                                                                    AS "IMIE",
       COALESCE(k.przydzial_myszy, 0) + COALESCE(k.myszy_extra, 0)               AS "ZJADA",
       k.nr_bandy                                                                AS "NR BANDY",
       ROUND(AVG(COALESCE(b.przydzial_myszy, 0) + COALESCE(b.myszy_extra, 0)), 2) AS "SREDNIA BANDY"
FROM Kocury k
         JOIN Kocury b ON k.nr_bandy = b.nr_bandy
WHERE k.plec = 'M'
GROUP BY k.pseudo
HAVING COALESCE(k.przydzial_myszy, 0) + COALESCE(k.myszy_extra, 0) <=
       AVG(COALESCE(b.przydzial_myszy, 0) + COALESCE(b.myszy_extra, 0))
ORDER BY 3 DESC;

-- zad11 b) zlaczenie z jedynym podzapytaniem w FROM
SELECT k.imie                                                    AS "IMIE",
       COALESCE(k.przydzial_myszy, 0) + COALESCE(k.myszy_extra, 0) AS "ZJADA",
       k.nr_bandy                                                AS "NR BANDY",
       ROUND(s.sr, 2)                                            AS "SREDNIA BANDY"
FROM Kocury k
         JOIN (SELECT nr_bandy, AVG(COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0)) AS sr
               FROM Kocury
               GROUP BY nr_bandy) s ON k.nr_bandy = s.nr_bandy
WHERE k.plec = 'M'
  AND COALESCE(k.przydzial_myszy, 0) + COALESCE(k.myszy_extra, 0) <= s.sr
ORDER BY 3 DESC;

-- zad11 c) bez zlaczen, podzapytania skorelowane w SELECT i WHERE
SELECT imie                                                    AS "IMIE",
       COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0) AS "ZJADA",
       nr_bandy                                                AS "NR BANDY",
       (SELECT ROUND(AVG(COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0)), 2)
        FROM Kocury
        WHERE nr_bandy = k.nr_bandy)                           AS "SREDNIA BANDY"
FROM Kocury k
WHERE plec = 'M'
  AND COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0) <=
      (SELECT AVG(COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0))
       FROM Kocury
       WHERE nr_bandy = k.nr_bandy)
ORDER BY 3 DESC;


-- zad12 a) CASE + SUM; spozycie liczone raz w tabeli pochodnej,
-- nazwa bandy tylko w pierwszym wierszu bandy (ROW_NUMBER na wynikach grupowania)
SELECT CASE WHEN ROW_NUMBER() OVER (PARTITION BY nazwa ORDER BY plec) = 1 THEN nazwa ELSE ' ' END AS "NAZWA BANDY",
       CASE plec WHEN 'D' THEN 'Kotka' ELSE 'Kocor' END                                        AS "PLEC",
       COUNT(*)                                                                                AS "ILE",
       SUM(CASE funkcja WHEN 'SZEFUNIO' THEN zjada ELSE 0 END)                                 AS "SZEFUNIO",
       SUM(CASE funkcja WHEN 'BANDZIOR' THEN zjada ELSE 0 END)                                 AS "BANDZIOR",
       SUM(CASE funkcja WHEN 'LOWCZY' THEN zjada ELSE 0 END)                                   AS "LOWCZY",
       SUM(CASE funkcja WHEN 'LAPACZ' THEN zjada ELSE 0 END)                                   AS "LAPACZ",
       SUM(CASE funkcja WHEN 'KOT' THEN zjada ELSE 0 END)                                      AS "KOT",
       SUM(CASE funkcja WHEN 'MILUSIA' THEN zjada ELSE 0 END)                                  AS "MILUSIA",
       SUM(CASE funkcja WHEN 'DZIELCZY' THEN zjada ELSE 0 END)                                 AS "DZIELCZY",
       SUM(zjada)                                                                              AS "SUMA"
FROM (SELECT nazwa, plec, funkcja, COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0) AS zjada
      FROM Kocury
               JOIN Bandy USING (nr_bandy)) k
GROUP BY nazwa, plec
ORDER BY nazwa, plec;
