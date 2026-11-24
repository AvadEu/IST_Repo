-- zad5 remis na 2. miejscu (DAMA i MAN po 51) rozstrzyga alfabetycznie pseudonim;
-- RANK / DENSE_RANK zamiast ROW_NUMBER zwrocilyby obu remisujacych
SELECT b.nr_bandy AS "NR_BANDY", b.nazwa AS "NAZWA", z.pseudo AS "PSEUDO", z.zjada AS "ZJADA"
FROM Bandy b
         LEFT JOIN (SELECT nr_bandy,
                           pseudo,
                           NVL(przydzial_myszy, 0) + NVL(myszy_extra, 0) AS zjada,
                           ROW_NUMBER() OVER (PARTITION BY nr_bandy
                               ORDER BY NVL(przydzial_myszy, 0) + NVL(myszy_extra, 0) DESC, pseudo) AS nr
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
                           NVL(przydzial_myszy, 0) + NVL(myszy_extra, 0) AS zjada,
                           RANK() OVER (PARTITION BY funkcja
                               ORDER BY NVL(przydzial_myszy, 0) + NVL(myszy_extra, 0) DESC) AS nr
                    FROM Kocury) r ON f.funkcja = r.funkcja AND r.nr = 1
ORDER BY 1;


-- zad7 zagniezdzone funkcje grupowe (AVG(COUNT(*))) -> bez widoku i bez tabeli pochodnej
SELECT TO_CHAR(EXTRACT(YEAR FROM w_stadku_od)) AS "ROK", COUNT(*) AS "LICZBA WSTAPIEN"
FROM Kocury
GROUP BY EXTRACT(YEAR FROM w_stadku_od)
HAVING COUNT(*) IN ((SELECT MAX(COUNT(*))
                     FROM Kocury
                     GROUP BY EXTRACT(YEAR FROM w_stadku_od)
                     HAVING COUNT(*) < (SELECT AVG(COUNT(*)) FROM Kocury GROUP BY EXTRACT(YEAR FROM w_stadku_od))),
                    (SELECT MIN(COUNT(*))
                     FROM Kocury
                     GROUP BY EXTRACT(YEAR FROM w_stadku_od)
                     HAVING COUNT(*) > (SELECT AVG(COUNT(*)) FROM Kocury GROUP BY EXTRACT(YEAR FROM w_stadku_od))))
UNION ALL
SELECT 'Srednia', ROUND(AVG(COUNT(*)), 7)
FROM Kocury
GROUP BY EXTRACT(YEAR FROM w_stadku_od)
ORDER BY 2, 1;


-- zad8 MINUS na poczatku -> ((wszyscy - skrajni) + najstarsi) + najmlodsi, bez nawiasow
SELECT imie AS "IMIE", w_stadku_od AS "WSTAPIL DO STADKA", ' ' AS " "
FROM Kocury
MINUS
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
