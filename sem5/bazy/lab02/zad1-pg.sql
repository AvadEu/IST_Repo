-- zad1
SELECT imie_wroga AS "WROG", opis_incydentu AS "PRZEWINA"
FROM Wrogowie_kocurow
WHERE DATE_PART('year', data_incydentu) = 2009;

-- zad2
SELECT imie AS "IMIE", funkcja AS "FUNKCJA", w_stadku_od AS "Z NAMI OD"
FROM Kocury
WHERE plec = 'D'
  AND w_stadku_od BETWEEN '2005-09-01' AND '2007-07-31';

-- zad3
SELECT imie_wroga       AS "WROG",
       gatunek          AS "GATUNEK",
       stopien_wrogosci AS "STOPIEN WROGOSCI"
FROM Wrogowie
WHERE lapowka IS NULL
ORDER BY stopien_wrogosci;

-- zad4
SELECT imie || ' zwany ' || pseudo || ' (fun. ' || funkcja ||
       ') lowi myszki w bandzie ' || nr_bandy ||
       ' od ' || w_stadku_od AS "WSZYSTKO O KOCURACH"
FROM Kocury
WHERE plec = 'M'
ORDER BY w_stadku_od DESC, pseudo;

-- zad5
SELECT pseudo                  AS "PSEUDO",
       POSITION('A' IN pseudo) AS "A",
       POSITION('L' IN pseudo) AS "L",
       REGEXP_REPLACE(REGEXP_REPLACE(pseudo, 'A', '#'), 'L', '%')
                               AS "Po wymianie A na # oraz L na %"
FROM Kocury
WHERE pseudo LIKE '%A%'
  AND pseudo LIKE '%L%'
ORDER BY pseudo;


-- zad6
SELECT imie                                      AS "IMIE",
       w_stadku_od                               AS "W stadku",
       przydzial_myszy                           AS "Zjadal",
       (w_stadku_od + INTERVAL '6 months')::DATE AS "Podwyzka",
       ROUND(przydzial_myszy * 1.1)              AS "Zjada"
FROM Kocury
WHERE AGE(w_stadku_od) >= INTERVAL '15 years'
  AND DATE_PART('month', w_stadku_od) BETWEEN 3 AND 9
ORDER BY przydzial_myszy DESC;


-- zad7
SELECT imie                         AS "IMIE",
       przydzial_myszy * 3          AS "MYSZY KWARTALNIE",
       COALESCE(myszy_extra, 0) * 3 AS "KWARTALNE DODATKI"
FROM Kocury
WHERE przydzial_myszy > 2 * COALESCE(myszy_extra, 0)
  AND przydzial_myszy >= 55
ORDER BY przydzial_myszy DESC;


-- zad8
SELECT imie    AS "IMIE",
       CASE SIGN(12 * (przydzial_myszy + COALESCE(myszy_extra, 0)) - 660)
           WHEN 1 THEN (12 * (przydzial_myszy + COALESCE(myszy_extra, 0)))::TEXT
           WHEN 0 THEN 'Limit'
           WHEN -1 THEN 'Ponizej 660'
           END AS "Zjada rocznie"
FROM Kocury
ORDER BY imie;


-- zad9 PSEUDO
SELECT pseudo || ' - ' ||
       CASE WHEN COUNT(*) = 1 THEN 'Unikalny' ELSE 'nieunikalny' END
           AS "Unikalnosc atr. PSEUDO"
FROM Kocury
GROUP BY pseudo
ORDER BY pseudo;

-- zad 9 szef
SELECT szef || ' - ' ||
       CASE WHEN COUNT(*) = 1 THEN 'Unikalny' ELSE 'nieunikalny' END
           AS "Unikalnosc atr. SZEF"
FROM Kocury
WHERE szef IS NOT NULL
GROUP BY szef
ORDER BY szef;


-- zad10
SELECT pseudo AS "Pseudonim", COUNT(DISTINCT imie_wroga) AS "Liczba wrogow"
FROM Wrogowie_kocurow
GROUP BY pseudo
HAVING COUNT(DISTINCT imie_wroga) >= 2
ORDER BY pseudo;

select sign(22);