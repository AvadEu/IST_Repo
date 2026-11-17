-- zad4
SELECT b.nazwa AS "Nazwa bandy", COUNT(DISTINCT pseudo) AS "Koty z wrogami"
FROM Kocury
         JOIN Bandy b USING (nr_bandy)
         JOIN Wrogowie_kocurow USING (pseudo)
GROUP BY b.nazwa
ORDER BY b.nazwa;


-- zad5 a) wiecej niz jeden wrog
SELECT funkcja AS "Funkcja", pseudo AS "Pseudonim kota", COUNT(*) AS "Liczba wrogow"
FROM Kocury
         JOIN Wrogowie_kocurow USING (pseudo)
GROUP BY pseudo, funkcja
HAVING COUNT(*) > 1
ORDER BY pseudo;

-- zad5 b) wrog CZLOWIEK i wrog PIES
SELECT funkcja AS "Funkcja", pseudo AS "Pseudonim kota"
FROM Kocury
         JOIN Wrogowie_kocurow USING (pseudo)
         JOIN Wrogowie USING (imie_wroga)
WHERE gatunek IN ('CZLOWIEK', 'PIES')
GROUP BY pseudo, funkcja
HAVING COUNT(DISTINCT gatunek) = 2
ORDER BY pseudo;


-- zad6 a) bez podzapytan i operatorow zbiorowych
SELECT b.nr_bandy AS "NR BANDY", b.nazwa AS "NAZWA", b.teren AS "TEREN"
FROM Bandy b
         LEFT JOIN Kocury k ON b.nr_bandy = k.nr_bandy
WHERE k.pseudo IS NULL;

-- zad6 b) operatory zbiorowe
SELECT nr_bandy AS "NR BANDY", nazwa AS "NAZWA", teren AS "TEREN"
FROM Bandy
EXCEPT
SELECT nr_bandy, nazwa, teren
FROM Bandy
         JOIN Kocury USING (nr_bandy);
