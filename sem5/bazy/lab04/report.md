# Lista 4

## Założenia

- Cz. 1 (zad. 1–4) w PostgreSQL i Oracle, cz. 2 (zad. 5–8) w PostgreSQL i Oracle, cz. 3 (zad. 9–12a) w PostgreSQL, zad. 12a dodatkowo i zad. 12b wyłącznie w Oracle (tabele przestawne).
- Cz. 1 bez podzapytań, cz. 2–3 z podzapytaniami, bez widoków (zad. 7, 11).
- Całkowite spożycie = `przydzial_myszy + myszy_extra`; brak dodatku (NULL) liczony jako 0. W cz. 2–3, gdzie wartość służy do porządkowania lub porównań, także NULL w `przydzial_myszy` traktowany jako 0.
- Aliasy w cudzysłowach – nagłówki kolumn zgodne z przykładami.
- Priorytet: jak najkrótsze zapytania.

## Część 1

### **Zad. 1 – funkcje × bandy**
- Przestawienie ręczne: `SUM(CASE WHEN nazwa = ... THEN ... END)` / `SUM(DECODE(nazwa, ...))` – po jednej kolumnie na bandę.
- Brak `ELSE` / wartości domyślnej → NULL, więc pusta komórka tam, gdzie funkcja nie występuje w bandzie (jak w przykładzie), a nie 0.
- Wiersze z kotów wszystkich band (stąd DZIELCZY z pustymi wartościami), bez `SZEFUNIO`; HONOROWA nie pojawia się, bo nikt jej nie pełni.

### **Zad. 2 – dodatkowo płeć i liczba kotów**
- `GROUP BY funkcja, plec`.
- Liczba kotów jako `SUM(CASE ... THEN 1 END)` zamiast `COUNT` – dla pustej komórki zwraca NULL, a nie 0, zgodnie z przykładem.

### **Zad. 3 – statystyki wszystkich funkcji**
- `Funkcje LEFT JOIN Kocury` – pełna lista funkcji, także HONOROWA.
- Zabezpieczenie: `COUNT(k.pseudo)` liczy tylko dopasowane koty, `COALESCE(SUM(...), 0)` zamienia NULL na 0; średnia zostaje NULL (brak kotów = brak średniej).
- **a) bez zabezpieczenia:**
    - `COUNT(*)` liczy wiersz dołożony przez `LEFT JOIN` (same NULL-e) → HONOROWA ma **1 kota**.
    - `SUM` z samych NULL-i to **NULL**, a nie 0.
    - Z `INNER JOIN` HONOROWA w ogóle **znika** z wyniku.
- PostgreSQL: `TRIM_SCALE` usuwa zera końcowe po `ROUND(..., 4)` (90.5 zamiast 90.5000).

### **Zad. 4 – przed JACKIEM**
- Samozłączenie `Kocury k JOIN Kocury j ON j.imie = 'JACEK' AND k.w_stadku_od < j.w_stadku_od` – warunek zamiast podzapytania.

## Część 2

### **Zad. 5 – dwóch żarłoków każdej bandy**
- `ROW_NUMBER() OVER (PARTITION BY nr_bandy ORDER BY zjada DESC, pseudo)` + `nr <= 2`.
- **Remisy:** DAMA i MAN mają po 51 – rozstrzyga drugi klucz sortowania, alfabetycznie pseudonim (DAMA). `RANK` / `DENSE_RANK` zwróciłyby obu kotów.
- Warunek `nr <= 2` w `ON` złączenia `Bandy LEFT JOIN`, nie w `WHERE` – inaczej ROCKERSI (bez kotów) by zniknęli.
- `COALESCE` / `NVL` na obu składnikach – przy `DESC` NULL trafia na początek, więc kot bez przydziału zostałby „żarłokiem”.

### **Zad. 6 – rekordziści funkcji**
- `RANK` w tabeli pochodnej + `Funkcje LEFT JOIN` z `nr = 1` w `ON`; przy remisie wyświetlani wszyscy rekordziści.
- `CASE` bez `ELSE`, ostatnia gałąź `WHEN zjada IS NOT NULL` – dla HONOROWEJ oba porównania dają `UNKNOWN`, więc `ELSE 'W WIDELKACH'` byłby błędny.
- Odrzucona wersja Oracle z `MAX(pseudo) KEEP (DENSE_RANK LAST ORDER BY ...)` (bez podzapytania): `NVL` zamienia NULL-e z `LEFT JOIN` na 0, więc HONOROWA dostawała ZJADA = 0 i ocenę „PONIZEJ WIDELEK”.

### **Zad. 7 – lata najbliższe średniej**
- Lata: 2002, 2004, 2006, 2008, 2009, 2010, 2011 → 18 / 7 ≈ 2,5714286; najbliżej od dołu 2 (cztery lata), od góry 4 (2006).
- PostgreSQL: `AVG(COUNT(*)) OVER ()` na wynikach grupowania, `DENSE_RANK() OVER (PARTITION BY SIGN(ile - sr) ORDER BY ABS(ile - sr))` – osobny ranking po każdej stronie średniej. Wiersz „Srednia” jako `COUNT(*) / COUNT(DISTINCT rok)` – bez podzapytania.
- Oracle: zagnieżdżone funkcje grupowe (`MAX(COUNT(*))`, `AVG(COUNT(*))`) – bez tabel pochodnych.
- Rok jako tekst – wymóg `UNION` z wierszem „Srednia”; `ORDER BY 2, 1` umieszcza średnią między latami.

### **Zad. 8 – najstarsi i najmłodsi stażem**
- Trzy gałęzie: (wszyscy `EXCEPT` / `MINUS` skrajni) `UNION ALL` najstarsi `UNION ALL` najmłodsi.
- Operatory zbiorowe mają równy priorytet i wiążą od lewej – `EXCEPT` na początku działa bez nawiasów; na końcu odjąłby także koty oznaczone.
- `EXCEPT` / `MINUS` porównuje NULL jak wartość – kot bez daty przystąpienia zostałby w wyniku (`NOT IN` by go odrzucił).
- Banda z jednym kotem dałaby go dwukrotnie – jest jednocześnie najstarszy i najmłodszy.
- Oracle: kolumny z `USING` nie wolno kwalifikować, a podzapytanie odwołuje się do `k.nr_bandy` – stąd `JOIN ... ON`.

## Część 3

### **Zad. 9 – koty do przeczołgania**
- `NOT EXISTS` podwładnych, `EXISTS` wrogów, przydział ≥ `min + (max - min) / 3` z `Funkcje`.
- `NOT IN (SELECT szef ...)` dałby pusty wynik – szef TYGRYSA to NULL (jak w liście 3).
- `NUMERIC / 3` daje ułamek (np. 23,33 dla MILUSI) – w T-SQL dzielenie liczb całkowitych obcięłoby wynik do 23.

### **Zad. 10 – skrajne średnie funkcji**
- `HAVING AVG(...) >= ALL (...) OR AVG(...) <= ALL (...)` – bez operatorów zbiorowych; PostgreSQL nie pozwala na `MAX(AVG(...))`.
- `COALESCE` w środku `AVG` – NULL w wyniku podzapytania wyłączyłby `>= ALL`.
- `ROUND` bez miejsc dziesiętnych: 90,5 → 91.

### **Zad. 11 – kocury poniżej średniej bandy**
- a) samozłączenie z kotami tej samej bandy, `GROUP BY k.pseudo` (PK – reszta kolumn wynika funkcyjnie), porównanie w `HAVING`.
- b) średnie band w tabeli pochodnej, złączenie po `nr_bandy`.
- c) dwa podzapytania skorelowane – w `SELECT` (wyświetlenie) i w `WHERE` (filtr).
- Wszystkie trzy dają ten sam wynik; c) liczy średnią dwukrotnie dla każdego kocura.

### **Zad. 12 – spożycie funkcje × bandy × płeć**
- a) `SUM(CASE funkcja WHEN ... THEN zjada ELSE 0 END)` / `SUM(DECODE(funkcja, ..., zjada, 0))` – tu `ELSE 0`, bo przykład pokazuje zera. Spożycie liczone raz w tabeli pochodnej.
- b) Oracle `PIVOT` – PostgreSQL ma tylko `crosstab` z rozszerzenia `tablefunc`. `PIVOT` grupuje niejawnie po kolumnach nieużytych w agregacie, więc `ILE` i `SUMA` policzone wcześniej funkcjami okna (stałe w ramach banda + płeć); `NVL` zamienia brakujące komórki na 0.
- Nazwa bandy tylko w pierwszym wierszu: `ROW_NUMBER() OVER (PARTITION BY nazwa ORDER BY plec) = 1` – działa także dla bandy z kotami jednej płci.
- Oracle: `ORDER BY plec` wskazywał alias `"PLEC"` (Kotka/Kocor) zamiast kolumny – sortowanie Kocor przed Kotką. Naprawa: kwalifikacja `k.plec`. W PostgreSQL `"PLEC"` ≠ `plec`, problem nie występuje.

## Różnice PostgreSQL / Oracle

| | PostgreSQL | Oracle |
|---|---|---|
| wyrażenie warunkowe | `CASE` | `DECODE` |
| zagnieżdżone agregaty | brak – funkcje okna / tabele pochodne | `AVG(COUNT(*))`, `MAX(COUNT(*))` |
| tabela przestawna | `crosstab` (rozszerzenie) | `PIVOT` |
| różnica zbiorów | `EXCEPT` | `MINUS` |
| usunięcie zer końcowych | `TRIM_SCALE` | domyślnie przy wyświetlaniu |
| nazwa w `ORDER BY` | najpierw kolumna wyjściowa, z rozróżnieniem wielkości liter w `"..."` | alias `"PLEC"` przesłania kolumnę `plec` |
| kolumna z `USING` | można kwalifikować | kwalifikacja zabroniona (ORA-25154) |

## Istotne obserwacje

- Przy `LEFT JOIN` + agregacji `COUNT(*)` liczy wiersz bez dopasowania – trzeba liczyć kolumnę z prawej tabeli.
- `COALESCE` / `NVL` w złym miejscu potrafi zamienić „brak kota” w „kot zjadający 0” (KEEP w zad. 6).
- Warunek na prawej tabeli złączenia zewnętrznego musi być w `ON`, nie w `WHERE` – inaczej złączenie staje się wewnętrzne (zad. 5, 6).
- O tym, czy pusta komórka to NULL czy 0, decyduje obecność `ELSE` w `CASE` / wartości domyślnej w `DECODE` (zad. 1–2 vs 12).
- `ROW_NUMBER` vs `RANK` to świadomy wybór sposobu rozstrzygania remisów.

## Podsumowanie

Lista skupiała się na agregacji: przestawianiu wierszy w kolumny, złączeniach zewnętrznych z funkcjami grupowymi i rankingach w grupach.
Najwięcej uwagi wymagała obsługa NULL – wiersze dokładane przez `LEFT JOIN` zachowują się inaczej w `COUNT(*)`, `SUM` i `CASE`, co pokazuje zad. 3a.
Oracle wypada krócej tam, gdzie ma dedykowane konstrukcje (`PIVOT`, zagnieżdżone agregaty), PostgreSQL nadrabia funkcjami okna; wszystkie wyniki zgadzają się z przykładami w obu systemach.
