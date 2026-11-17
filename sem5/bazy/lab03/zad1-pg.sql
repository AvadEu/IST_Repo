SELECT k2.imie "W stadzie przed szefem lub bez incydentu",
       CASE
           WHEN (k2.w_stadku_od > k1.w_stadku_od) and k1.imie = 'JACEK' THEN 'TAK'
           ELSE 'NIE'
           END "CZY PRZED JACKIEM"
FROM Kocury k1
         inner join kocury k2 on k1.pseudo = k2.szef
         left join wrogowie_kocurow wk on k2.pseudo = wk.pseudo
where k2.w_stadku_od < k1.w_stadku_od
   or wk.pseudo is NULL and lower(right(wk.imie_wroga, 1)) = 'a';


-- zad2
SELECT COALESCE(p.pseudo, 'Brak przelozonego') AS "Przelozony",
       COALESCE(k.pseudo, 'Brak podwladnego')  AS "Podwladny"
FROM Kocury p
         FULL JOIN Kocury k ON p.pseudo = k.szef
WHERE COALESCE(p.plec, 'M') = 'M'
  AND COALESCE(k.plec, 'M') = 'M'
ORDER BY 1, 2;


-- zad3
-- grupa = (kot, wrog) -> brak duplikatow czlonkow bandy w SUM;
-- DISTINCT ON scala wiersze kota z kilkoma wrogami
SELECT DISTINCT ON (k.nr_bandy, k.pseudo) k.pseudo                                                AS "PSEUDO",
                                          k.przydzial_myszy                                       AS "PRZYDZIAL_MYSZY",
                                          SUM(m.przydzial_myszy)                                  AS "SUM_W_BANDZIE",
                                          ROUND(100 * k.przydzial_myszy / SUM(m.przydzial_myszy)) AS "PROC_W_BANDZIE"
FROM Kocury k
         JOIN Bandy b ON k.nr_bandy = b.nr_bandy
         JOIN Wrogowie_kocurow wk ON k.pseudo = wk.pseudo
         JOIN Wrogowie w ON wk.imie_wroga = w.imie_wroga
         JOIN Kocury m ON k.nr_bandy = m.nr_bandy
WHERE b.teren IN ('POLE', 'CALOSC')
  AND w.stopien_wrogosci BETWEEN 6 AND 10
GROUP BY k.pseudo, wk.imie_wroga
ORDER BY k.nr_bandy, k.pseudo;
