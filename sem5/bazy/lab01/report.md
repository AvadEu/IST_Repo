# Lista 1

## Zadanie 1 – schema

### **Kolejność:** `Funkcje` -> `Wrogowie` -> `Bandy` -> `Kocury` -> `Wrogowie_kocurow` -> `ALTER TABLE Bandy`.

### **Decyzje:**
- Cykl FK `Bandy.szef_bandy` ↔ `Kocury.nr_bandy` – FK szefa bandy dodany jedynym dopuszczalnym `ALTER TABLE`.
- Ograniczenia kolumnowe wszędzie, gdzie to możliwe. Tabelaryczne tylko:
    - PK `Wrogowie_kocurow (pseudo, imie_wroga)` – dwie kolumny (realizuje regułę „tylko pierwszy incydent”),
    - `max_myszy >= min_myszy` – odwołanie do innej kolumny.
- Nazwane ograniczenia (`<tabela>_<kolumna>_<typ>`) – czytelne błędy, łatwe zarządzanie.
- Kolejność kolumn zgodna ze schematem – umożliwia `INSERT` bez listy kolumn.

### **Modyfikacje względem Oracle:**

| | PostgreSQL | SQL Server |
|---|---|---|
| `VARCHAR2` / `NUMBER(p)` | `VARCHAR` / `NUMERIC(p)` | `VARCHAR` / `NUMERIC(p)` |
| `SYSDATE` | `CURRENT_DATE` | `GETDATE()` |
| `CONSTRAINT x NOT NULL` | bez zmian | niedozwolone – samo `NOT NULL` |

### Istotne obserwacje 
- `DATE` w Oracle zawiera czas 
- SQL Server w `UNIQUE` dopuszcza tylko jeden NULL
- PostgreSQL toleruje wielokolumnowy CHECK kolumnowy.

## Zadanie 2 – inject

### **Problemy i rozwiązania:**
- **Hierarchia kotów** – na liście podwładni występują przed szefami (FK `szef`). Kocury wstawiono poziomami hierarchii (1–4).
- **Cykl Bandy <-> Kocury:**
    - Oracle, PostgreSQL: bandy z `szef_bandy = NULL` -> kocury -> `UPDATE` szefów band,
    - SQL Server: powyższe niemożliwe (kilka NULL w `UNIQUE`) -> `NOCHECK CONSTRAINT` na FK
- **Daty w Oracle** -> literały `DATE '...'`.
- **Składnia:** Oracle – `INSERT ALL ... SELECT * FROM dual`; PostgreSQL / SQL Server – wiele krotek w `VALUES`.

### **Potencjalne pułapki**: 
- cykliczne klucze obce
- kolejność wstawiania
- różnice w obsłudze NULL w `UNIQUE` i formatów dat.

### **Ocena SZBD:**

Zdecydowanie zbyt wcześnie na ocenę najpopularniejszych narzędzi, z których każde od dłuższego czasu z powodzeniem rozwiązuje problemy biznesowe.
Na tym etapie różnice są marginalne.