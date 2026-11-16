# CSS_1 – Podstawy programowania w języku CSS3 (cz. 1) – omówienie rozwiązania

Witryna o Kopenhadze składa się z 6 stron:

| Plik | Zawartość |
|---|---|
| `index.html` | strona startowa – kilka akapitów tekstu |
| `atrakcje.html` | listy (zagnieżdżone, numerowane) |
| `informacje.html` | tabele |
| `kontakt.html`, `formularz-osobowy.html`, `formularz-dodatkowy.html` | formularze |
| `css/style.css` | zewnętrzny arkusz stylów |

---

## Wymagania ogólne

> Działanie HTML i CSS należy sprawdzić na trzech przeglądarkach wybranych z listy: Chrome, Edge, Firefox, Opera, Safari.
> Proszę utworzyć witrynę zawierającą minimum 3 strony zgodnych z standardem HTML 5 z odwołaniem do w zewnętrznego arkusza stylów zgodnego z standardem CSS3.
> Wszystkie reguły CSS, z wyjątkiem punktu 2, powinny być umieszczone w zewnętrznym arkuszu stylów.

**Realizacja:**

- Witryna ma 6 stron. Każda zaczyna się od deklaracji HTML5 i dołącza zewnętrzny arkusz stylów:

```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="utf-8">
    ...
    <link rel="stylesheet" href="css/style.css">
</head>
```

- Zgodność sprawdzono walidatorami W3C:
  - **HTML** (https://validator.w3.org/nu/) – wszystkie 6 stron: 0 błędów, 0 ostrzeżeń,
  - **CSS** (https://jigsaw.w3.org/css-validator/, profil „CSS level 3 + SVG”) – „Gratulacje! Nie znaleziono żadnych błędów. Dokument ten jest poprawnie napisanym arkuszem CSS poziom 3 + SVG”.
- Wszystkie reguły są w `css/style.css`. Wyjątkiem są tylko dwie reguły w `index.html`, które demonstrują punkt 2 (styl wewnętrzny i inline).

---

## 1. Strona startowa, kodowanie, tytuły, metadane

> Strona startowa zawiera odnośniki do stron zawierających kolejno: kilka akapitów tekstu, listę odnośników, tabelę oraz formularz. Kodowanie wszystkich stron proszę ustawić jako utf-8. Każda strona, posiada własny, unikatowy tytuł oraz jest opatrzona meta danymi w szczególności opisem oraz słowami kluczowymi (na potrzeby pozycjonowania).

**Realizacja:**

- Każda strona (także startowa) ma menu z odnośnikami do wszystkich podstron (zob. punkt 12). Menu jest zbudowane jako lista `<ul>` odnośników `<a>`, więc spełnia wymóg „listy odnośników”:
  - akapity tekstu – `index.html`,
  - listy – `atrakcje.html`,
  - tabele – `informacje.html`,
  - formularze – `kontakt.html`, `formularz-osobowy.html`, `formularz-dodatkowy.html`.
- Kodowanie, opis, słowa kluczowe i unikatowy tytuł – przykład z `index.html`:

```html
<meta charset="utf-8">
<meta name="description" content="Prezentacja Kopenhagi, stolicy Danii: historia, zabytki, informacje praktyczne i kontakt.">
<meta name="keywords" content="Kopenhaga, Dania, stolica, turystyka, Nyhavn, zwiedzanie">
<title>Kopenhaga – stolica Danii | Strona główna</title>
```

Tytuły pozostałych stron: „Atrakcje Kopenhagi – co zobaczyć”, „Informacje praktyczne o Kopenhadze – klimat i transport”, „Kontakt i formularz – Kopenhaga”, „Formularz osobowy – Kopenhaga”, „Formularz dodatkowy – Kopenhaga”.

---

## 2. Trzy metody osadzania reguł CSS

> Zaprezentuj różne możliwości osadzania reguł CSS na stronie (3 metody).

**Realizacja:**

**Metoda 1 – zewnętrzny arkusz stylów** (wszystkie strony). Style są w osobnym pliku, więc jeden plik obsługuje całą witrynę:

```html
<link rel="stylesheet" href="css/style.css">
```

**Metoda 2 – wewnętrzny arkusz stylów** (`index.html`, sekcja `<head>`). Reguła działa tylko na tej jednej stronie:

```html
<!-- Metoda 2: wewnętrzny arkusz stylów (znacznik <style> w sekcji head) -->
<style>
    /* Reguła działa tylko na tej stronie – kolor nagłówków h3 w artykule */
    article h3 {
        color: #2a6f97;
    }
</style>
```

**Metoda 3 – styl wpisany (inline)** (`index.html`). Styl dotyczy tylko jednego elementu i ma najwyższy priorytet:

```html
<!-- Metoda 3: styl wpisany (atrybut style) – działa tylko na ten jeden element -->
<h4 id="nyhavn" style="color: #b5651d;">Port Nyhavn</h4>
```

---

## 3. Wielkość tekstu (em, px, pt, %)

> Zaprezentuj praktyczne wykorzystanie różnych sposobów zmiany wielkości tekstu na stronie (em, px, pt, %)

**Realizacja** (`css/style.css`, sekcja 1):

```css
/* % – rozmiar względem domyślnego rozmiaru przeglądarki (100% = zwykle 16px). */
html {
    font-size: 100%;
}

/* em – rozmiar względem czcionki rodzica (2.4em = 2,4 razy większy). */
h1 {
    font-size: 2.4em;
}

/* px – rozmiar stały w pikselach ekranu (tekst musi zmieścić się w menu o stałej wysokości). */
.menu a {
    font-size: 15px;
}

/* pt – punkty typograficzne (1pt = 1/72 cala), jednostka typowa dla druku. */
footer {
    font-size: 10pt;
}
```

| Jednostka | Gdzie | Dlaczego tam |
|---|---|---|
| `%` | `html` | szanuje ustawienia przeglądarki użytkownika |
| `em` | `h1`, `aside p` (`0.9em`) | rozmiar skaluje się razem z tekstem rodzica |
| `px` | linki menu | menu ma stałą wysokość 40px |
| `pt` | stopka | jednostka „drukarska” |

---

## 4. Tło strony

> Zaprezentuj różne sposoby ustawienia tła strony - jego pozycji, powtarzalności, ograniczania (np. powtarzanie do połowy wysokości strony) i rozciągania (background-color, background-image, background-repeat, backgroundattachment, background-position, background)

**Realizacja** (`css/style.css`, sekcja 2) – trzy różne tła.

**a) Tło całej strony.** Wykorzystuje `background-color`, `-image`, `-repeat`, `-position` i `-attachment`. Obrazek jest powtarzany tylko w poziomie, a jego wysokość to połowa okna, więc pas obrazków zajmuje tylko górną połowę strony – to jest **ograniczenie** powtarzania:

```css
body {
    background-color: #dfe9f0;
    background-image: url("../images/Nyhavn.jpg");
    background-repeat: repeat-x;
    background-size: auto 50vh;
    background-position: left top;
    background-attachment: fixed;
}
```

**b) Tło nagłówka.** Wszystko zapisane jedną właściwością skrótową `background`; `cover` **rozciąga** obrazek na cały nagłówek:

```css
header {
    background: url("../images/Nyhavn.jpg") center / cover no-repeat;
}
```

**c) Tło ramki `<aside>`.** Mały obrazek bez powtarzania, ustawiony w prawym dolnym rogu (**pozycja**):

```css
aside {
    background-color: #f1f6fa;
    background-image: url("../images/Nyhavn.jpg");
    background-repeat: no-repeat;
    background-position: right bottom;
    background-size: 80px auto;
}
```

---

## 5. Selektory CSS i kiedy ich używać

> Zaprezentuj różne sposoby definiowania selektorów CSS i wraz z ich wykorzystaniem na stronie. Omów w jakich sytuacjach najlepiej je wykorzystywać (identyfikatory, klasy, zagnieżdżenia, > )

**Realizacja** (`css/style.css`, sekcja 3). Omówienie znajduje się w komentarzu na początku sekcji:

| Selektor | Zapis | Kiedy używać |
|---|---|---|
| identyfikator | `#id` | element unikatowy na stronie (`id` występuje raz); ma wysoką specyficzność, więc trudno go nadpisać – używać rzadko |
| klasa | `.klasa` | ten sam wygląd dla wielu elementów, także różnych typów – najczęstszy wybór, style wielokrotnego użytku |
| zagnieżdżenie (potomek) | `A B` | styl zależny od kontekstu, B na dowolnej głębokości w A |
| dziecko | `A > B` | tylko bezpośrednie dzieci – gdy struktura się powtarza (np. menu wielopoziomowe) i styl nie powinien „przeciekać” głębiej |

Przykłady użycia:

```css
/* Identyfikator – główny nagłówek artykułu na stronie startowej */
#gora {
    color: #1d3557;
}

/* Klasa – miniatura obrazka */
.miniatura {
    border-radius: 6px;
}

/* Zagnieżdżenie (potomek) – wszystkie akapity w artykule, na dowolnym poziomie */
article p {
    text-align: justify;
}

/* Dziecko (">") – tylko sekcje będące bezpośrednimi dziećmi <article>
   (sekcja zagnieżdżona "Port Nyhavn" nie zostanie objęta). */
article > section {
    clear: both;
    padding-top: 10px;
}
```

Odpowiadający HTML (`index.html`):

```html
<h2 id="gora">Kopenhaga – przewodnik turysty</h2>
...
<a href="atrakcje.html"><img class="miniatura" src="images/Nyhavn.jpg" width="200" alt="..."></a>
```

Selektor dziecka jest też kluczowy w menu: `.menu > li` (tylko kategorie główne) oraz `.menu li:hover > ul` (tylko bezpośrednie podmenu).

---

## 6. Box model i pozycjonowanie

> Zaprezentuj praktycznie wszystkie właściwości box-model oraz pozycjonowania elementów na stronie (margin, padding, width, height, position:(absolute, relative, static, fixed), left, right, top, bottom, float, clear).

**Realizacja** (`css/style.css`, sekcje 4 i 8):

**margin, padding, width.** Główna treść ma szerokość 80%, jest wyśrodkowana marginesami `auto` i ma odstępy wewnętrzne:

```css
main {
    width: 80%;
    max-width: 900px;
    margin: 20px auto;
    padding: 20px 30px;
    background-color: #fff;
}
```

**height:**

```css
header {
    height: 160px;
}
```

**position: relative + top, left.** Tytuł jest przesunięty względem swojego normalnego miejsca:

```css
header h1 {
    position: relative;
    top: 50px;
    left: 30px;
    ...
}
```

**position: fixed + top, left, right.** Menu jest przyklejone do góry okna:

```css
nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 40px;
    ...
}
```

**position: fixed + right, bottom.** Przycisk „Przewiń na początek” jest w prawym dolnym rogu okna:

```css
.do-gory {
    position: fixed;
    right: 20px;
    bottom: 20px;
    ...
}
```

**position: absolute.** Podmenu jest wyjęte z przepływu i ustawione względem rodzica `li` z `position: relative`:

```css
.menu ul {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    width: 210px;
    ...
}

.menu ul ul {
    top: 0;
    left: 100%;
    ...
}
```

**position: static.** Wartość domyślna – element w normalnym przepływie, a `top`/`left` nie działają:

```css
footer {
    position: static;
    ...
}
```

**float:**

```css
.miniatura {
    float: right;
    margin: 0 0 10px 20px;
}

aside {
    float: right;
    width: 250px;
    ...
}

.menu > li {
    float: left;      /* kategorie menu obok siebie */
    position: relative;
}
```

**clear:**

```css
article > section {
    clear: both;      /* nowa sekcja nie opływa miniatury */
}

main::after {
    content: "";
    display: block;
    clear: both;      /* main obejmuje pływającą ramkę <aside> */
}
```

---

## 7. Formatowanie tekstu

> Zaprezentuj różne sposoby formatowania tekstu oraz ustawianej jego szerokości (font-weight, font-style, font-variant, font-size, line-height, font-family)

**Realizacja** (`css/style.css`, sekcja 5):

```css
/* font-family – lista czcionek; line-height – wysokość linii (interlinia) */
body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.6;
}

/* Nagłówki i menu czcionką bezszeryfową */
h1, h2, h3, h4, nav {
    font-family: Arial, Helvetica, sans-serif;
}

/* font-variant: small-caps – kapitaliki */
h2 {
    font-variant: small-caps;
}

/* font-weight – grubość czcionki (900 = najgrubsza) */
strong {
    font-weight: 900;
}

/* font-style: italic – kursywa; font-size w em */
aside p {
    font-style: italic;
    font-size: 0.9em;
}
```

Właściwość `font-size` pokazano też w punkcie 3 (`%`, `em`, `px`, `pt`).

---

## 8. Obramowanie

> Napisz regułę CSS stosując atrybut: border-width, border-style, border-color.

**Realizacja** (`css/style.css`, sekcja 6). Ramka `<aside>` ma różne wartości dla poszczególnych boków (kolejność: góra, prawo, dół, lewo):

```css
aside {
    border-width: 1px 1px 1px 6px;
    border-style: dotted dotted dotted solid;
    border-color: #457b9d;
}
```

Te same trzy właściwości są użyte także dla komórek tabel (punkt 9).

---

## 9. Stylowanie tabel

> Zaprezentuj różne możliwość stylowania tabel.

**Realizacja** (`css/style.css`, sekcja 7 oraz pseudoklasy z sekcji 9). Tabele są na `informacje.html`, w tym tabela zagnieżdżona:

```css
/* border-collapse: collapse – sąsiednie ramki komórek łączą się w jedną linię */
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 20px;
}

/* Podpis tabeli pod tabelą (caption-side) i kursywą */
caption {
    caption-side: bottom;
    font-style: italic;
    padding: 6px;
}

/* Ramki i odstępy wewnątrz komórek, wyrównanie tekstu */
th, td {
    border-width: 1px;
    border-style: solid;
    border-color: #a8b8c8;
    padding: 6px 10px;
    text-align: left;
    vertical-align: top;
}

/* Wyróżniony nagłówek tabeli (thead) */
thead th {
    background-color: #1d3557;
    color: #fff;
    text-align: center;
}

/* Tabela zagnieżdżona w komórce – szerokość dopasowana do treści */
td table {
    width: auto;
    margin: 0;
}

/* Co drugi wiersz w paski ("zebra") */
tbody tr:nth-child(even) {
    background-color: #f1f6fa;
}
```

---

## 10. Reguła @media

> Zaprezentuj możliwości użycia reguły @media.

**Realizacja** (`css/style.css`, sekcja 10).

**a) Wąskie ekrany (telefony).** Menu przestaje być przyklejone, a kategorie i podmenu układają się jedno pod drugim:

```css
@media (max-width: 700px) {
    body { padding-top: 0; }

    header { height: auto; padding: 20px 10px; }
    header h1 { top: 0; left: 0; font-size: 1.8em; }

    nav { position: static; height: auto; }
    .menu > li { float: none; }
    .menu ul,
    .menu ul ul { position: static; width: auto; padding-left: 20px; }

    main, footer { width: auto; margin: 10px; padding: 10px; }
    aside { float: none; width: auto; margin: 10px 0; }
}
```

**b) Wydruk.** Bez menu, przycisku i tła:

```css
@media print {
    nav,
    .do-gory {
        display: none;
    }

    body {
        background: none;
        padding-top: 0;
        color: #000;
    }
}
```

---

## 11. Pseudoklasy

> Zaprezentuj działanie pseudoklas CSS: :active, :checked, :disabled, :empty, :enabled, :first, :first-child, :focus, :hover, :last-child, :last-of-type, :link, :not(), :nth-child(), :nth-last-child(), :only-child, :required, :target, :visited.

**Realizacja** (`css/style.css`, sekcja 9):

| Pseudoklasa | Reguła | Gdzie widać |
|---|---|---|
| `:link` | `main a:link { color: #1d6fa5; }` | nieodwiedzone linki w treści |
| `:visited` | `main a:visited { color: #7b2cbf; }` | odwiedzone linki w treści |
| `:hover` | `main a:hover, .menu li:hover > a { background-color: #e63946; ... }` | linki i menu pod kursorem; także rozwijanie menu |
| `:active` | `button:active { background-color: #e63946; ... }` | przyciski „Wyślij”/„Wyczyść” w chwili kliknięcia |
| `:focus` | `input:focus, select:focus, textarea:focus { outline: 3px solid #f4a261; }` | aktywne pole formularza |
| `:enabled` | `input:enabled { background-color: #fffdf3; }` | pola, które można edytować |
| `:disabled` | `input:disabled { background-color: #ddd; ... }` | pole „Kraj” w `formularz-osobowy.html` |
| `:required` | `input:required { border-left: 4px solid #e63946; }` | „Nazwisko” i „E-mail” w `formularz-osobowy.html` |
| `:checked` | `input:checked + label { font-weight: bold; color: #2a9d8f; }` | zaznaczone radio/checkbox w `kontakt.html` |
| `:not()` | `input:not([type="radio"]):not([type="checkbox"]) { padding: 4px; }` | wszystkie pola oprócz radio i checkbox |
| `:empty` | `td:empty { background-color: #eeeeee; }` | puste komórki w `formularz-dodatkowy.html` |
| `:first-child` | `td:first-child { font-weight: bold; }` | pierwsza kolumna tabel |
| `:last-child` | `.menu ul li:last-child { border-bottom: none; }` | ostatnia pozycja podmenu |
| `:last-of-type` | `main > h2:last-of-type { border-bottom: 2px dashed #e63946; }` | ostatni `h2` na stronie |
| `:nth-child()` | `tbody tr:nth-child(even) { background-color: #f1f6fa; }` | paski w tabelach |
| `:nth-last-child()` | `main ol > li:nth-last-child(2) { color: #b5651d; }` | przedostatni punkt planu dnia (`atrakcje.html`) |
| `:only-child` | `main li:only-child { font-style: italic; }` | „Mała Syrenka” – jedyna pozycja w kategorii |
| `:target` | `:target { background-color: #ffe8a3; scroll-margin-top: 50px; }` | element wskazany kotwicą, np. `index.html#gora`, `informacje.html#klimat` |
| `:first` | `@page :first { margin-top: 3cm; }` | pierwsza strona wydruku |

Elementy HTML dodane do pokazania pseudoklas:

```html
<!-- formularz-osobowy.html – pole dla :disabled -->
<input type="text" id="kraj" name="kraj" value="Polska" disabled>

<!-- identyfikatory dla :target, np. informacje.html -->
<h2 id="klimat">Klimat w ciągu roku</h2>
<h2 id="transport">Transport i pieniądze</h2>
```

---

## 12. Menu rozwijane (3 poziomy)

> Stwórz szablon strony z menu rozwijanym w oparciu o CSS (3 poziomowe). Menu powinno posiadać co najmniej trzy kategorie, a dla każdej kategorii podkategorię, a dla podkategorii kolejną podkategorię.

**Realizacja.** Każda z 6 stron ma to samo menu, czyli wspólny szablon. Ma ono 3 kategorie, każda z podkategoriami, a każda podkategoria – z kolejną podkategorią:

```
Kopenhaga
├── O mieście ............ Port Nyhavn
└── Materiały ............ Przewodnik (.txt), Lista atrakcji (.txt)
Zwiedzanie
├── Atrakcje ............. Plan zwiedzania, Ocena atrakcji
└── Informacje praktyczne  Klimat, Transport
Formularze
└── Kontakt .............. Formularz osobowy, Formularz dodatkowy
```

Struktura HTML (fragment – zagnieżdżone listy `ul`):

```html
<nav>
    <ul class="menu">
        <li><a href="index.html">Kopenhaga</a>
            <ul>
                <li><a href="index.html#gora">O mieście</a>
                    <ul>
                        <li><a href="index.html#nyhavn">Port Nyhavn</a></li>
                    </ul>
                </li>
                ...
            </ul>
        </li>
        <li><a href="atrakcje.html">Zwiedzanie</a> ... </li>
        <li><a href="kontakt.html">Formularze</a> ... </li>
    </ul>
</nav>
```

CSS (`css/style.css`, sekcja 8). Menu działa wyłącznie na CSS, bez JavaScriptu:

```css
/* Poziom 1 – kategorie obok siebie; punkt odniesienia dla podmenu */
.menu > li {
    float: left;
    position: relative;
}

/* Poziom 2 – ukryty, pod kategorią */
.menu ul {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    width: 210px;
    background-color: #457b9d;
}

/* Poziom 3 – z prawej strony podkategorii */
.menu ul ul {
    top: 0;
    left: 100%;
    background-color: #5f97b8;
}

/* Po najechaniu pokazujemy BEZPOŚREDNIE podmenu danego elementu */
.menu li:hover > ul {
    display: block;
}
```

Mechanizm działania:

1. Podmenu są domyślnie ukryte (`display: none`).
2. Najechanie na pozycję (`:hover`) pokazuje tylko jej bezpośrednie podmenu (`> ul`), dzięki czemu poziom 3 nie pojawia się razem z poziomem 2.
3. Poziom 2 wysuwa się pod kategorią (`top: 100%`), a poziom 3 – z prawej strony podkategorii (`left: 100%`).
