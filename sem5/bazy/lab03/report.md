# Lista 3

## Założenia

- Cz. 1 (zad. 1–3) w PostgreSQL, cz. 2 (zad. 4–6) w PostgreSQL i Oracle, cz. 3 (zad. 7–10) w PostgreSQL, cz. 4 (zad. 11–13) wyłącznie w Oracle.
- Cz. 1–2 bez podzapytań, cz. 4 bez podzapytań i złączeń (poza 13a).
- Aliasy w cudzysłowach – nagłówki kolumn zgodne z przykładami.
- Priorytet: jak najkrótsze zapytania, złączenia tylko tam, gdzie bez nich brakuje danych.

## Część 1

### **Zad. 1 – przed szefem lub bez incydentu**
- `INNER JOIN` kota (`k2`) z jego bezpośrednim szefem (`k1`) – porównanie dat `k2.w_stadku_od < k1.w_stadku_od`.
- `LEFT JOIN` incydentów – brak incydentu rozpoznawany po `wk.pseudo IS NULL`.
- Wróg na literę A: `lower(right(wk.imie_wroga, 1)) = 'a'`.
- Kolumna `CZY PRZED JACKIEM` wyznaczana przez `CASE` na podstawie dat przystąpienia.

### **Zad. 2 – męscy przełożeni i podwładni**
- `FULL JOIN` kotów z ich podwładnymi: lewa strona bez pary = brak podwładnego, prawa = brak przełożonego.
- `COALESCE(plec, 'M') = 'M'` – filtr płci przepuszcza wiersze z NULL po stronie bez pary.
- Filtr po złączeniu odpowiada przykładowi: ZOMBI (ma tylko podwładne) nie występuje, a ZERO (szefowa KURKA) nie dostaje wiersza „Brak przelozonego” – „brak” oznacza faktyczny brak, a nie brak kota płci męskiej.

### **Zad. 3 – koty z pola z groźnymi wrogami**
- Teren `IN ('POLE', 'CALOSC')` – szefostwo poluje na całym terenie.
- Suma w bandzie przez ponowne złączenie z `Kocury m` (członkowie bandy) – funkcja okna liczyłaby tylko koty po filtrze `WHERE`.
- Kot z kilkoma wrogami mnożyłby członków bandy w `SUM` → grupowanie po `(kot, wróg)`, a `DISTINCT ON` scala wiersze tego samego kota.

## Część 2

### **Zad. 4 – koty z wrogami w bandach**
- `COUNT(DISTINCT pseudo)` – jeden kot ma wiele incydentów.
- `JOIN ... USING` – krótsze i identyczne w obu SZBD.

### **Zad. 5 – więcej niż jeden wróg / człowiek i pies**
- a) `HAVING COUNT(*) > 1` – PK `(pseudo, imie_wroga)` gwarantuje, że to liczba różnych wrogów.
- b) `WHERE gatunek IN ('CZLOWIEK', 'PIES')` + `HAVING COUNT(DISTINCT gatunek) = 2`.
- Oba warunki dają te same trzy koty.

### **Zad. 6 – bandy bez członków**
- a) `LEFT JOIN` + `k.pseudo IS NULL` (anti-join).
- b) wszystkie bandy `EXCEPT` / `MINUS` bandy ze złączenia z kotami.

## Część 3

### **Zad. 7 – prominenci, szaraki, „nie-szefowie”**
- Dwie gałęzie `UNION ALL` z kolumną `Typ`; kot może trafić do obu grup.
- Szarak: `NOT EXISTS` kota z tej samej bandy o mniejszym przydziale; remis (UCHO, MALY) daje dwóch szaraków.
- NULL w przydziale traktowany jako 0 (`COALESCE` po obu stronach i w `AVG`).
- **`NOT IN` vs `NOT EXISTS`:**
    - `NOT IN (SELECT szef ...)` zwraca **pusty wynik** – wśród szefów jest NULL (TYGRYS). `x NOT IN (a, NULL)` = `x <> a AND x <> NULL` → `UNKNOWN`, więc żaden wiersz nie spełnia warunku.
    - `NOT EXISTS` porównuje `p.szef = k.pseudo` wiersz po wierszu; NULL daje `UNKNOWN` tylko dla swojego wiersza i nie „psuje” całości → poprawne 13 kotów.
    - Naprawa `NOT IN`: `WHERE szef IS NOT NULL` w podzapytaniu.

### **Zad. 8 – bandy powyżej średniej**
- Z wyświetleniem: średnia stada liczona raz w tabeli pochodnej, używana w `SELECT` i `HAVING`.
- Bez wyświetlania: podzapytanie skalarne w `HAVING`.

### **Zad. 9 – rekruci w miesiącach**
- `TO_CHAR(..., 'FMMONTH')` – pełna nazwa wielkimi literami, `FM` usuwa dopełnienie spacjami.
- `ORDER BY MIN(DATE_PART('month', ...))` – kolejność kalendarzowa bez dodatkowej kolumny grupującej.

### **Zad. 10 – trzykrotność najwyższego przydziału MILUŚ z sadu**
- Zamiast `MAX` – `>= ALL (...)`.
- MILUSIE z bandy o terenie `CALOSC` też operują w sadzie – to daje 3 × 25 = 75, zgodnie z przykładem.
- `przydzial_myszy IS NOT NULL` w podzapytaniu – jeden NULL sprawiłby, że `>= ALL` nigdy nie byłby prawdziwy.

## Część 4

### **Zad. 11 – kocury pod bandziorem**
- `START WITH` bandziora płci męskiej, `WHERE plec = 'M'` filtruje dopiero wynik – kotki zostają w drzewie, więc ZERO (pod KURKĄ) ma poziom 3.
- `ORDER SIBLINGS BY` – sortowanie bez psucia hierarchii.

### **Zad. 12 – droga służbowa**
- Drzewo budowane w górę (`PRIOR szef = pseudo`) od kotów spełniających warunki w `START WITH`.
- Staż: `MONTHS_BETWEEN(DATE '2024-07-17', w_stadku_od) > 180`.
- Wcięcie: `LPAD(' ', 4 * LEVEL - 4)` – dla poziomu 1 daje NULL, a NULL `||` tekst w Oracle to tekst.

### **Zad. 13 – szefowie KOT i MILUŚ**
- a) trzy `LEFT JOIN` – liczba kolumn sztywna (maks. 3 poziomy), `LEFT` bo nie każdy ma trzech szefów.
- b) drzewo w górę, wiersz liścia (`CONNECT_BY_ISLEAF = 1`) niesie całą drogę; `CONNECT_BY_ROOT` zwraca imię i funkcję kota startowego, `SUBSTR` odcina z `SYS_CONNECT_BY_PATH` segment korzenia.
- Separatory `|` jako osobne kolumny z aliasem `" "`.

## Różnice PostgreSQL / Oracle

| | PostgreSQL | Oracle |
|---|---|---|
| różnica zbiorów | `EXCEPT` | `MINUS` |
| jeden wiersz na grupę | `DISTINCT ON` | – |
| hierarchia | rekurencyjne CTE | `CONNECT BY`, `LEVEL`, `SYS_CONNECT_BY_PATH` |
| kolumna z `USING` | można kwalifikować | kwalifikacja zabroniona (ORA-25154) |
| zależność funkcyjna w `GROUP BY` | grupowanie po PK wystarcza | każda kolumna jawnie |

## Istotne obserwacje

- NULL w `NOT IN` i `>= ALL` potrafi wyzerować cały wynik – `NOT EXISTS` jest odporny.
- Złączenie 1:N (wrogowie) przed agregacją mnoży wiersze – trzeba grupować po kluczu złączenia lub liczyć `DISTINCT`.
- `WHERE` w zapytaniu hierarchicznym działa po zbudowaniu drzewa, `START WITH` – przed.
- Funkcje okna liczone są po `WHERE` / `HAVING`, więc bez podzapytań nie zastąpią agregatu po pełnej bandzie.

## Podsumowanie

Lista wymagała przejścia od pojedynczej tabeli do złączeń zewnętrznych, podzapytań i drzew.
Najwięcej pracy kosztowała poprawna interpretacja przykładów (zad. 2, 10) oraz unikanie mnożenia wierszy przy złączeniach (zad. 3).
`CONNECT BY` w Oracle rozwiązuje zadania hierarchiczne wyraźnie krócej niż złączenia – zad. 13b działa dla dowolnej głębokości, 13a tylko dla trzech poziomów.
