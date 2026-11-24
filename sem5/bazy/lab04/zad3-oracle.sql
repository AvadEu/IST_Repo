-- zad12 a) DECODE + SUM; spozycie liczone raz w tabeli pochodnej,
-- ORDER BY kwalifikowany (k.plec) - samo plec wskazaloby alias "PLEC" (Kotka/Kocor),
-- nazwa bandy tylko w pierwszym wierszu bandy (ROW_NUMBER na wynikach grupowania)
SELECT DECODE(ROW_NUMBER() OVER (PARTITION BY nazwa ORDER BY plec), 1, nazwa, ' ') AS "NAZWA BANDY",
       DECODE(plec, 'D', 'Kotka', 'Kocor')                                         AS "PLEC",
       COUNT(*)                                                                    AS "ILE",
       SUM(DECODE(funkcja, 'SZEFUNIO', zjada, 0))                                  AS "SZEFUNIO",
       SUM(DECODE(funkcja, 'BANDZIOR', zjada, 0))                                  AS "BANDZIOR",
       SUM(DECODE(funkcja, 'LOWCZY', zjada, 0))                                    AS "LOWCZY",
       SUM(DECODE(funkcja, 'LAPACZ', zjada, 0))                                    AS "LAPACZ",
       SUM(DECODE(funkcja, 'KOT', zjada, 0))                                       AS "KOT",
       SUM(DECODE(funkcja, 'MILUSIA', zjada, 0))                                   AS "MILUSIA",
       SUM(DECODE(funkcja, 'DZIELCZY', zjada, 0))                                  AS "DZIELCZY",
       SUM(zjada)                                                                  AS "SUMA"
FROM (SELECT nazwa, plec, funkcja, NVL(przydzial_myszy, 0) + NVL(myszy_extra, 0) AS zjada
      FROM Kocury
               JOIN Bandy USING (nr_bandy)) k
GROUP BY nazwa, plec
ORDER BY k.nazwa, k.plec;


-- zad12 b) PIVOT (PostgreSQL nie ma tabel przestawnych - tylko crosstab z rozszerzenia tablefunc)
-- ILE i SUMA liczone funkcjami okna w zrodle - PIVOT grupuje niejawnie po kolumnach
-- nieuzytych w agregacie (nazwa, plec, ile, suma), a te sa stale w ramach (banda, plec)
SELECT DECODE(ROW_NUMBER() OVER (PARTITION BY nazwa ORDER BY plec), 1, nazwa, ' ') AS "NAZWA BANDY",
       DECODE(plec, 'D', 'Kotka', 'Kocor')                                         AS "PLEC",
       ile                                                                         AS "ILE",
       NVL(szefunio, 0)                                                            AS "SZEFUNIO",
       NVL(bandzior, 0)                                                            AS "BANDZIOR",
       NVL(lowczy, 0)                                                              AS "LOWCZY",
       NVL(lapacz, 0)                                                              AS "LAPACZ",
       NVL(kot, 0)                                                                 AS "KOT",
       NVL(milusia, 0)                                                             AS "MILUSIA",
       NVL(dzielczy, 0)                                                            AS "DZIELCZY",
       suma                                                                        AS "SUMA"
FROM (SELECT nazwa,
             plec,
             funkcja,
             NVL(przydzial_myszy, 0) + NVL(myszy_extra, 0)                                 AS zjada,
             COUNT(*) OVER (PARTITION BY nazwa, plec)                                      AS ile,
             SUM(NVL(przydzial_myszy, 0) + NVL(myszy_extra, 0)) OVER (PARTITION BY nazwa, plec) AS suma
      FROM Kocury
               JOIN Bandy USING (nr_bandy))
    PIVOT (SUM(zjada) FOR funkcja IN ('SZEFUNIO' AS szefunio, 'BANDZIOR' AS bandzior, 'LOWCZY' AS lowczy,
        'LAPACZ' AS lapacz, 'KOT' AS kot, 'MILUSIA' AS milusia, 'DZIELCZY' AS dzielczy)) p
ORDER BY p.nazwa, p.plec;
