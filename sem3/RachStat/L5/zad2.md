

``` r
dane <- read.csv2("waga1.csv")

# Zad 2
# H0: mu = 170
# H1: mu != 170
cat("Zadanie 2\n")
```

```
## Zadanie 2
```

``` r
t.test(dane$Wzrost, mu = 170)$p.value
```

```
## [1] 0.0003244236
```

``` r
# Ponieważ p = 0.0003244 < 0.001, to:
# Odrzucamy H0 na poziomie istotności 0.1% i przyjmujemy H1

# Zad 3
# Przedział ufności 90%
cat("Zadanie 3\n")
```

```
## Zadanie 3
```

``` r
t.test(dane$Wzrost, conf.level = 0.90)$conf.int
```

```
## [1] 162.6116 167.1662
## attr(,"conf.level")
## [1] 0.9
```

``` r
# Zad 4
# H0: mu_kobiet = 160
# H1: mu_kobiet != 160

cat("Zadanie 4\n")
```

```
## Zadanie 4
```

``` r
kobiety <- dane$Wzrost[dane$plec == 1]
t.test(kobiety, mu = 160)$p.value
```

```
## [1] 0.3574295
```

``` r
# Ponieważ p = 0.3574 > 0.05, to:
# Nie odrzucamy H0 na poziomie istotności 5%.
# Nie mamy dowodów, że średni wzrost studentek różni się od 160 cm

# Zad 5
cat("Zadanie 5\n")
```

```
## Zadanie 5
```

``` r
t.test(kobiety, conf.level = 0.98)$conf.int
```

```
## [1] 154.0376 162.6432
## attr(,"conf.level")
## [1] 0.98
```

``` r
# Zad 6
# H0: proporcja studentów (mężczyzn) wyższych niż 180 cm = 25%: p = 0.25
# H1: proporcja studentów (mężczyzn) wyższych niż 180 cm != 25%: p != 0.25
cat("Zadanie 6\n")
```

```
## Zadanie 6
```

``` r
mezczyzni <- dane$Wzrost[dane$plec == 0]
liczba_m <- length(mezczyzni)
ponad_180 <- sum(mezczyzni > 180)

prop.test(ponad_180, liczba_m, p = 0.25, correct = FALSE)$p.value
```

```
## [1] 0.5218394
```

``` r
# Ponieważ p = 0.5218 > 0.05, to:
# Nie odrzucamy H0 na poziomie istotności 5%
# Nie mamy dowodów, że proporcja mężczyzn wyższych niż 180 cm różni się od 25%

# zad7
cat("Zadanie 7\n")
```

```
## Zadanie 7
```

``` r
prop.test(ponad_180, liczba_m, conf.level = 0.96, correct = FALSE)$conf.int
```

```
## [1] 0.1192414 0.3471206
## attr(,"conf.level")
## [1] 0.96
```

