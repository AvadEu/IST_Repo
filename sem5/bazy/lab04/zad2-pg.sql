-- zad5 remis na 2. miejscu (DAMA i MAN po 51) rozstrzyga alfabetycznie pseudonim;
-- RANK / DENSE_RANK zamiast ROW_NUMBER zwrocilyby obu remisujacych
SELECT b.nr_bandy AS "NR_BANDY", b.nazwa AS "NAZWA", z.pseudo AS "PSEUDO", z.zjada AS "ZJADA"
FROM Bandy b
         LEFT JOIN (SELECT nr_bandy,
                           pseudo,
                           COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0) AS zjada,
                           ROW_NUMBER() OVER (PARTITION BY nr_bandy
                               ORDER BY COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0) DESC, pseudo) AS nr
                    FROM Kocury) z ON b.nr_bandy = z.nr_bandy AND z.nr <= 2
ORDER BY 1, 4 DESC;


-- zad6 RANK -> przy remisie wszyscy rekordzisci; CASE bez ELSE -> HONOROWA bez oceny
SELECT f.funkcja AS "FUNKCJA",
       r.pseudo  AS "PSEUDO",
       r.zjada   AS "ZJADA",
       CASE
           WHEN r.zjada < f.min_myszy THEN 'PONIZEJ WIDELEK'
           WHEN r.zjada > f.max_myszy THEN 'POWYZEJ WIDELEK'
           WHEN r.zjada IS NOT NULL THEN 'W WIDELKACH'
           END   AS "OCENA"
FROM Funkcje f
         LEFT JOIN (SELECT funkcja,
                           pseudo,
                           COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0) AS zjada,
                           RANK() OVER (PARTITION BY funkcja
                               ORDER BY COALESCE(przydzial_myszy, 0) + COALESCE(myszy_extra, 0) DESC) AS nr
                    FROM Kocury) r ON f.funkcja = r.funkcja AND r.nr = 1
ORDER BY 1;


-- zad7 srednia liczona funkcja okna na wynikach GROUP BY; w kazdej "stronie" sredniej
-- (SIGN) wybierane lata o najmniejszej odleglosci od niej
SELECT rok AS "ROK", ile AS "LICZBA WSTAPIEN"
FROM (SELECT rok, ile, DENSE_RANK() OVER (PARTITION BY SIGN(ile - sr) ORDER BY ABS(ile - sr)) AS nr
      FROM (SELECT DATE_PART('year', w_stadku_od)::TEXT AS rok, COUNT(*) AS ile, AVG(COUNT(*)) OVER () AS sr
            FROM Kocury
            GROUP BY 1) l) t
WHERE nr = 1
UNION ALL
SELECT 'Srednia', ROUND(COUNT(*)::NUMERIC / COUNT(DISTINCT DATE_PART('year', w_stadku_od)), 7)
FROM Kocury
ORDER BY 2, 1;


-- zad8 EXCEPT na poczatku -> ((wszyscy - skrajni) + najstarsi) + najmlodsi, bez nawiasow
SELECT imie AS "IMIE", w_stadku_od AS "WSTAPIL DO STADKA", ' ' AS " "
FROM Kocury
EXCEPT
SELECT imie, w_stadku_od, ' '
FROM Kocury k
WHERE w_stadku_od IN ((SELECT MIN(w_stadku_od) FROM Kocury WHERE nr_bandy = k.nr_bandy),
                      (SELECT MAX(w_stadku_od) FROM Kocury WHERE nr_bandy = k.nr_bandy))
UNION ALL
SELECT imie, w_stadku_od, '<--- NAJSTARSZY STAZEM W BANDZIE ' || nazwa
FROM Kocury k
         JOIN Bandy b ON k.nr_bandy = b.nr_bandy
WHERE w_stadku_od = (SELECT MIN(w_stadku_od) FROM Kocury WHERE nr_bandy = k.nr_bandy)
UNION ALL
SELECT imie, w_stadku_od, '<--- NAJMLODSZY STAZEM W BANDZIE ' || nazwa
FROM Kocury k
         JOIN Bandy b ON k.nr_bandy = b.nr_bandy
WHERE w_stadku_od = (SELECT MAX(w_stadku_od) FROM Kocury WHERE nr_bandy = k.nr_bandy)
ORDER BY 1;
