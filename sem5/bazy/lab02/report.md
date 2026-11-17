# Lista 2 – część 1

## Założenia

- Wyłącznie `SELECT` bez podzapytań i złączeń, funkcje SQL, grupowanie.
- Zad. 1–7 w PostgreSQL, zad. 8–10 w PostgreSQL i Oracle.
- Aliasy w cudzysłowach – nagłówki kolumn zgodne z przykładami.
- Priorytet: jak najkrótsze zapytania.

## Rozwiązania

### **Zad. 1 – incydenty z 2009 r.**
- `DATE_PART('year', data_incydentu) = 2009` – krótsze niż przedział dat.
- Bez `DISTINCT` – jeden wiersz to jeden incydent (KAZIO występuje dwukrotnie).

### **Zad. 2 – kotki w przedziale dat**
- `plec = 'D'` + `BETWEEN` na datach (granice włącznie).

### **Zad. 3 – nieprzekupni wrogowie**
- Nieprzekupny = `lapowka IS NULL`, sortowanie rosnąco wg `stopien_wrogosci`.

### **Zad. 4 – kocury w jednej kolumnie**
- Konkatenacja `||` – liczby i daty konwertowane automatycznie.
- `ORDER BY w_stadku_od DESC, pseudo`.

### **Zad. 5 – pozycje liter A i L**
- `POSITION` do wyszukania, `LIKE` do filtrowania.
- `TRANSLATE(pseudo, 'AL', '#%')` – jedna funkcja zamiast zagnieżdżonego `REPLACE`.

### **Zad. 6 – staż i podwyżka**
- Staż: `AGE(DATE '2024-07-17', w_stadku_od) >= INTERVAL '15 years'`.
- Miesiąc przystąpienia: `DATE_PART('month', ...) BETWEEN 3 AND 9`.
- Podwyżka: `w_stadku_od + INTERVAL '6 months'`, rzutowane na `DATE`; nowy przydział `ROUND(przydzial_myszy * 1.1)`.

### **Zad. 7 – przydziały kwartalne**
- `COALESCE(myszy_extra, 0)` – brak dodatku liczony jako 0, wartości mnożone przez 3.

### **Zad. 8 – roczne spożycie**
- `SIGN(spożycie - 660)` rozróżnia trzy przypadki jednym wyrażeniem.
- PostgreSQL: `CASE` + `::TEXT`; Oracle: `DECODE` + `TO_CHAR`.
- Wyrażenie spożycia powtórzone – bez podzapytań nie da się go nazwać.

### **Zad. 9 – unikalność PSEUDO i SZEF**
- `GROUP BY` + `COUNT(*) = 1`.
- Dla `SZEF` filtr `szef IS NOT NULL` – inaczej NULL utworzyłby własną grupę.

### **Zad. 10 – co najmniej dwóch wrogów**
- `COUNT(DISTINCT imie_wroga)` w `HAVING` – kilka incydentów z tym samym wrogiem liczy się raz.

## Różnice PostgreSQL / Oracle

| | PostgreSQL | Oracle |
|---|---|---|
| wyrażenie warunkowe | `CASE` | `DECODE` |
| NULL → wartość | `COALESCE` | `NVL` |
| liczba → tekst | `::TEXT` | `TO_CHAR` |
| dodanie miesięcy | `+ INTERVAL '6 months'` | `ADD_MONTHS` |
| różnica dat | `AGE` | `MONTHS_BETWEEN` |

## Istotne obserwacje

- NULL w arytmetyce i konkatenacji daje NULL – konieczne `COALESCE` / `NVL`.
- `DATE + INTERVAL` w PostgreSQL zwraca `timestamp` – wymaga rzutowania na `DATE`.
- Gałęzie `CASE` / `DECODE` muszą zwracać ten sam typ.
- Zakaz podzapytań wymusza powtarzanie wyrażeń, co wydłuża zapytania.

## Podsumowanie

Wszystkie zadania dało się rozwiązać pojedynczym `SELECT` na jednej tabeli.
Główna trudność to nie logika, lecz zwięzłość – dobór funkcji (`TRANSLATE`, `SIGN`, `AGE`) skraca zapytania.
Oracle wypada nieco krócej dzięki `DECODE` i `NVL`, PostgreSQL – dzięki `::` i `INTERVAL`; różnice nadal są marginalne.
