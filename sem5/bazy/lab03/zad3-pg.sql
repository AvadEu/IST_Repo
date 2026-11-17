-- zad7 prominenci i szaraki (NULL w przydziale traktowany jako 0 myszy)
SELECT pseudo                                                                 AS "Pseudonim",
       przydzial_myszy                                                        AS "Zjada",
       nr_bandy                                                               AS "Banda",
       'Prominent'                                                            AS "Typ",
       CASE WHEN przydzial_myszy > 60 THEN 'powyzej 60' ELSE 'ponizej 60' END AS "Ocena"
FROM Kocury
WHERE przydzial_myszy > (SELECT AVG(COALESCE(przydzial_myszy, 0)) FROM Kocury)
UNION ALL
SELECT pseudo,
       przydzial_myszy,
       nr_bandy,
       'Szarak',
       CASE WHEN przydzial_myszy > 60 THEN 'powyzej 60' ELSE 'ponizej 60' END
FROM Kocury k
WHERE NOT EXISTS (SELECT 1
                  FROM Kocury m
                  WHERE m.nr_bandy = k.nr_bandy
                    AND COALESCE(m.przydzial_myszy, 0) < COALESCE(k.przydzial_myszy, 0))
ORDER BY "Typ", "Banda", "Zjada" DESC;

-- zad7 nie sa niczyim szefem: NOT IN -> pusty wynik (szef TYGRYSA = NULL)
SELECT pseudo AS "Nie sa niczyim szefem"
FROM Kocury
WHERE pseudo NOT IN (SELECT szef FROM Kocury)
ORDER BY pseudo;

-- zad7 nie sa niczyim szefem: NOT EXISTS -> poprawny wynik
SELECT pseudo AS "Nie sa niczyim szefem"
FROM Kocury k
WHERE NOT EXISTS (SELECT 1 FROM Kocury p WHERE p.szef = k.pseudo)
ORDER BY pseudo;

-- zad7 nie sa niczyim szefem: NOT IN z odfiltrowanym NULL -> wynik jak NOT EXISTS
SELECT pseudo AS "Nie sa niczyim szefem"
FROM Kocury
WHERE pseudo NOT IN (SELECT szef FROM Kocury WHERE szef IS NOT NULL)
ORDER BY pseudo;


-- zad8 z wyswietleniem sredniej
SELECT k.nr_bandy                                                    AS "Lepsze bandy",
       ROUND(AVG(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)), 1) AS "Sredni przydzial w bandzie",
       ROUND(s.sr, 1)                                                AS "Sredni przydzial"
FROM Kocury k,
     (SELECT AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) AS sr FROM Kocury) s
GROUP BY k.nr_bandy, s.sr
HAVING AVG(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)) > s.sr
ORDER BY 1;

-- zad8 bez wyswietlania sredniej
SELECT nr_bandy                                                  AS "Lepsze bandy",
       ROUND(AVG(przydzial_myszy + COALESCE(myszy_extra, 0)), 1) AS "Sredni przydzial w bandzie"
FROM Kocury
GROUP BY nr_bandy
HAVING AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) >
       (SELECT AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) FROM Kocury)
ORDER BY 1;


-- zad9
SELECT TO_CHAR(w_stadku_od, 'FMMONTH') AS "Miesiac", COUNT(*) AS "Liczba rekrutow"
FROM Kocury
GROUP BY 1
ORDER BY MIN(DATE_PART('month', w_stadku_od));


-- zad10 (koty z bandy o terenie CALOSC tez operuja w sadzie)
SELECT imie AS "IMIE", funkcja AS "FUNKCJA", przydzial_myszy AS "PRZYDZIAL MYSZY"
FROM Kocury
WHERE przydzial_myszy >= ALL (SELECT 3 * przydzial_myszy
                              FROM Kocury
                                       JOIN Bandy USING (nr_bandy)
                              WHERE funkcja = 'MILUSIA'
                                AND teren IN ('SAD', 'CALOSC')
                                AND przydzial_myszy IS NOT NULL)
ORDER BY imie;
