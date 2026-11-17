-- zad8
SELECT imie                  AS "IMIE",
       DECODE(SIGN(12 * (przydzial_myszy + NVL(myszy_extra, 0)) - 660),
              1, TO_CHAR(12 * (przydzial_myszy + NVL(myszy_extra, 0))),
              0, 'Limit',
              'Ponizej 660') AS "Zjada rocznie"
FROM Kocury
ORDER BY imie;


-- zad9
-- a) atrybut PSEUDO
SELECT pseudo || ' - ' || DECODE(COUNT(*), 1, 'Unikalny', 'nieunikalny')
           AS "Unikalnosc atr. PSEUDO"
FROM Kocury
GROUP BY pseudo
ORDER BY pseudo;

-- b) atrybut SZEF
SELECT szef || ' - ' || DECODE(COUNT(*), 1, 'Unikalny', 'nieunikalny')
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