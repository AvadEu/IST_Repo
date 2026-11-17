# Wyniki AI-tutorial

## Opracowanie

- Alicja Wieczorek 284294
- Wiktor Golimowski 284251

## Zad 1

| Element | Opis |
|---|---|
| Polecenie | Wyświetl koty, które dołączyły do stada w 2008 roku. Wynik powinien zawierać pseudonim kota, imię, funkcję oraz datę dołączenia. |
| Model | Claude Opus 5.5 Medium Effort |
| SQL wygenerowany | ``` SELECT pseudo, imie, funkcja, w_stadku_od AS "Data dołączenia" FROM   Kocury WHERE  w_stadku_od >= DATE '2008-01-01' AND  w_stadku_od <  DATE '2009-01-01' ORDER  BY w_stadku_od;``` |
| Poprawność składniowa | Tak |
| Poprawność logiczna | Tak |
| Zgodność z poleceniem | Tak |
| Wykryty błąd | Brak błędu |
| Kategoria błędu | Klasyfikacja (E1–E8) |
| Weryfikacja | ``` SELECT pseudo, imie, funkcja, w_stadku_od AS "Data dołączenia" FROM   Kocury WHERE extract(YEAR FROM w_stadku_od) = 2008 ORDER  BY w_stadku_od;``` |
| SQL poprawiony | Identyczne jak wgenerowane |
| Wnioski | Zapytanie proste i poprawne |

## Zad 2

| Element | Opis |
|---|---|
| Polecenie | Oblicz sumę przydziału myszy dla kotów, które miały przynajmniej jeden incydent z wrogiem. |
| Model | Claude Opus 5.5 Medium Effort |
| SQL wygenerowany | ```SELECT SUM(k.przydzial_myszy) AS suma_przydzialu FROM   Kocury k WHERE  EXISTS ( SELECT 1 FROM   Wrogowie_kocurow wk WHERE  wk.pseudo = k.pseudo );``` |
| Poprawność składniowa | Tak |
| Poprawność logiczna | Tak |
| Zgodność z poleceniem | Tak |
| Wykryty błąd | Brak |
| Kategoria błędu | Klasyfikacja (E1–E8) |
| Weryfikacja | ``` SELECT k.pseudo, k.przydzial_myszy, COUNT(*) AS liczba_incydentow FROM   Kocury k JOIN   Wrogowie_kocurow wk ON wk.pseudo = k.pseudo GROUP  BY k.pseudo, k.przydzial_myszy ORDER  BY k.pseudo;``` |
| SQL poprawiony | Identyczne jak wgenerowane |
| Wnioski | Zapytanie poprawne, brak powielenia poprzez niewłaściwy `JOIN` |