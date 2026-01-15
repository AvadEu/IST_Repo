

``` r
interpretuj_wynik <- function(p_val) {
  cat("Wartość p =", format(p_val, scientific = FALSE), "\n")
  
  if (p_val > 0.05) {
    cat("Wniosek: Nie odrzucamy hipotezy zerowej na poziomie istotności 5%.\nNie mamy dowodów przeciwko H0.\n") 
  } else if (p_val > 0.01) {
    cat("Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 5%.\nMamy dowody przeciwko H0.\n")
  } else if (p_val > 0.001) {
    cat("Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 1%.\nMamy mocne dowody przeciwko H0.\n")
  } else {
    cat("Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 0,1%.\nMamy bardzo mocne dowody przeciwko H0.\n")
  }
}

cat("Zadanie 1 \n")
```

```
## Zadanie 1
```

``` r
n_kobiet <- 520
n_kobiet_studia <- 220
n_mezczyzn <- 480
n_mezczyzn_studia <- 165

cat("i) Ręczny test \n")
```

```
## i) Ręczny test
```

``` r
p1 <- n_kobiet_studia / n_kobiet
p2 <- n_mezczyzn_studia / n_mezczyzn
p_pool <- (n_kobiet_studia + n_mezczyzn_studia) / (n_kobiet + n_mezczyzn)

Z_stat <- (p1 - p2) / sqrt(p_pool * (1 - p_pool) * (1/n_kobiet + 1/n_mezczyzn))

p_val_Z <- 2 * (1 - pnorm(abs(Z_stat)))

cat("\n")
```

``` r
interpretuj_wynik(p_val_Z)
```

```
## Wartość p = 0.01000722 
## Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 5%.
## Mamy dowody przeciwko H0.
```

``` r
cat("\n")
```

``` r
cat("ii) Prop test \n")
```

```
## ii) Prop test
```

``` r
res_prop <- prop.test(x = c(n_kobiet_studia, n_mezczyzn_studia), n = c(n_kobiet, n_mezczyzn), correct = FALSE)
interpretuj_wynik(res_prop$p.value)
```

```
## Wartość p = 0.01000722 
## Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 5%.
## Mamy dowody przeciwko H0.
```

``` r
cat("\nPodpunkt B \n")
```

```
## 
## Podpunkt B
```

``` r
dane_tab <- matrix(c(165, 220, 480-165, 520-220), nrow = 2, byrow = TRUE)
dimnames(dane_tab) <- list(Plec = c("Kobieta", "Mezczyzna"), Wyksztalcenie = c("0", "1"))
print(dane_tab)
```

```
##            Wyksztalcenie
## Plec          0   1
##   Kobieta   165 220
##   Mezczyzna 315 300
```

``` r
cat("\nPodpunkt C \n")
```

```
## 
## Podpunkt C
```

``` r
cat("\ni) Test Chi-kwadrat\n")
```

```
## 
## i) Test Chi-kwadrat
```

``` r
test_chi <- chisq.test(dane_tab, correct = FALSE)
print(test_chi$p.value)
```

```
## [1] 0.01000722
```

``` r
interpretuj_wynik(test_chi$p.value)
```

```
## Wartość p = 0.01000722 
## Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 5%.
## Mamy dowody przeciwko H0.
```

``` r
cat("ii) Test fishera \n")
```

```
## ii) Test fishera
```

``` r
test_fisher <- fisher.test(dane_tab)
print(test_fisher$p.value)
```

```
## [1] 0.01117571
```

``` r
interpretuj_wynik(test_chi$p.value)
```

```
## Wartość p = 0.01000722 
## Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 5%.
## Mamy dowody przeciwko H0.
```

``` r
mean_k <- 166; 
var_k <- 100;
mean_m <- 174;
var_m <- 121;

se_diff <- sqrt(var_k/n_kobiet + var_m/n_mezczyzn)
Z_wzrost <- (mean_k - mean_m) / se_diff
p_val_wzrost <- 2 * pnorm(abs(Z_wzrost), lower.tail = FALSE)

cat("Statystyka Z (wzrost):", Z_wzrost, "\nP-value:", p_val_wzrost, "\n")
```

```
## Statystyka Z (wzrost): -12.00072 
## P-value: 3.522138e-33
```

``` r
interpretuj_wynik(p_val_wzrost)
```

```
## Wartość p = 0.000000000000000000000000000000003522138 
## Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 0,1%.
## Mamy bardzo mocne dowody przeciwko H0.
```

