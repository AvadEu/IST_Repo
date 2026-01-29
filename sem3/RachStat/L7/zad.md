

``` r
bakterie <- read.csv("bakteria.csv", sep = ";", dec = ",")
mieszkania <- read.csv("mieszkania.csv", sep = ";", dec = ",")

print("Zadanie 1")
```

```
## [1] "Zadanie 1"
```

``` r
wyniki_obs <- c(171, 200, 168, 213, 226, 222)
n <- sum(wyniki_obs)

p_oczekiwane <- rep(1 / 6, 6)
oczekiwane <- n * p_oczekiwane
print("Oczekiwane frekwencje:")
```

```
## [1] "Oczekiwane frekwencje:"
```

``` r
print(oczekiwane)
```

```
## [1] 200 200 200 200 200 200
```

``` r
chi_sq_stat <- sum((wyniki_obs - oczekiwane)^2 / oczekiwane)
print(paste("Statystyka Chi-kwadrat (wyliczona):", round(chi_sq_stat, 4)))
```

```
## [1] "Statystyka Chi-kwadrat (wyliczona): 15.97"
```

``` r
p_val <- 1 - pchisq(chi_sq_stat, df = 5)
print(paste("Wartość p:", p_val))
```

```
## [1] "Wartość p: 0.00693024925559715"
```

``` r
if(p_val < 0.05) {
  cat("Wniosek: Odrzucamy H0. Kostka NIE jest symetryczna (p < 0.05).\n")
} else {
  cat("Wniosek: Brak podstaw do odrzucenia H0.\n")
}
```

```
## Wniosek: Odrzucamy H0. Kostka NIE jest symetryczna (p < 0.05).
```

``` r
test_chi <- chisq.test(wyniki_obs, p = p_oczekiwane)
print(test_chi$p.value)
```

```
## [1] 0.006930249
```

``` r
print("Zadanie 2")
```

```
## [1] "Zadanie 2"
```

``` r
proba_exp <- rexp(1000, rate = 1)

# Hipoteza i: Czy to rozkład normalny N(1,1)?
ks_norm <- ks.test(proba_exp, "pnorm", mean = 1, sd = 1)
print(ks_norm)
```

```
## 
## 	Asymptotic one-sample Kolmogorov-Smirnov test
## 
## data:  proba_exp
## D = 0.15908, p-value < 2.2e-16
## alternative hypothesis: two-sided
```

``` r
#Odrzucamy H0 z poziomem istotnosci 0.1%

# Hipoteza ii: Czy to rozkład wykładniczy Exp(1)?
ks_exp <- ks.test(proba_exp, "pexp", rate = 1)
print(ks_exp)
```

```
## 
## 	Asymptotic one-sample Kolmogorov-Smirnov test
## 
## data:  proba_exp
## D = 0.018799, p-value = 0.8715
## alternative hypothesis: two-sided
```

``` r
#Brak podstaw do odrzucenia H0

proba_gamma <- rgamma(1000, shape = 100, scale = 1)

#H0: dane pochodza z rozkladu normalnego N(100,10)
ks_gamma_norm <- ks.test(proba_gamma, "pnorm", mean = 100, sd = 10)
ks_gamma_norm
```

```
## 
## 	Asymptotic one-sample Kolmogorov-Smirnov test
## 
## data:  proba_gamma
## D = 0.035064, p-value = 0.1709
## alternative hypothesis: two-sided
```

``` r
#Brak podstaw do odrzucenia H0

#H0: dane pochodza z rozkladu gamma z parametrami 100 1
ks_gamma_gamma <- ks.test(proba_gamma, "pgamma", shape = 100, scale = 1)
ks_gamma_gamma
```

```
## 
## 	Asymptotic one-sample Kolmogorov-Smirnov test
## 
## data:  proba_gamma
## D = 0.021774, p-value = 0.7302
## alternative hypothesis: two-sided
```

``` r
#Brak podstaw do odrzucenia H0
```

``` r
print("Zadanie 3")
```

```
## [1] "Zadanie 3"
```

``` r
mieszkania$Cena_za_m2 <- mieszkania$Cena / mieszkania$Metraz

# a)
shapiro_cena <- shapiro.test(mieszkania$Cena_za_m2)
print(shapiro_cena)
```

```
## 
## 	Shapiro-Wilk normality test
## 
## data:  mieszkania$Cena_za_m2
## W = 0.88837, p-value < 2.2e-16
```

``` r
#Odrzucam H0 z poziomem istotnosci 0.1% 

# b)
shapiro_metraz <- shapiro.test(mieszkania$Metraz)
print(shapiro_metraz)
```

```
## 
## 	Shapiro-Wilk normality test
## 
## data:  mieszkania$Metraz
## W = 0.96485, p-value = 3.272e-16
```

``` r
#Odrzucam H0 z poziomem istotnosci 0.1% 
```

``` r
print("Zadanie 4")
```

```
## [1] "Zadanie 4"
```

``` r
# a)
linreg <- lm(mieszkania$Cena ~ mieszkania$Metraz, data = mieszkania)
beta0 <- linreg$coefficients["(Intercept)"]
beta1 <- linreg$coefficients["dane$Metraz"]


# b)
plot(mieszkania$Metraz, mieszkania$Cena,
    main = "Regresja: Cena vs Metraż",
    xlab = "Metraż [m^2]", ylab = "Cena [PLN]",
    pch = 19, col = "blue")
abline(linreg, col = "red", lwd = 2)
```

![plot of chunk unnamed-chunk-4](figure/unnamed-chunk-4-1.png)

``` r
# c)
reszty <- residuals(linreg)
shapiro_reszty <- shapiro.test(reszty)
print(shapiro_reszty)
```

```
## 
## 	Shapiro-Wilk normality test
## 
## data:  reszty
## W = 0.87814, p-value < 2.2e-16
```

``` r
#Odrzucam H0 z poziomem istotnosci 0.1%

# d)
nowe_dane <- data.frame(metraz = 80)
przewidywana_cena <- predict(linreg, nowe_dane)
```

```
## Warning: 'newdata' had 1 row but variables found have 1170 rows
```

``` r
# print(paste("Szacowana cena dla 80 m2:", round(przewidywana_cena, 2), "PLN"))
```

``` r
print("Zadanie 5")
```

```
## [1] "Zadanie 5"
```

``` r
# a)
plot(bakterie$czas, bakterie$masa,
    main = "Wzrost masy bakterii",
    xlab = "Czas", ylab = "Masa",
    pch = 19, col = "darkgreen")
```

![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-1.png)

``` r
# b)
model_bakterie <- lm(log(masa) ~ czas, data = bakterie)
print(summary(model_bakterie))
```

```
## 
## Call:
## lm(formula = log(masa) ~ czas, data = bakterie)
## 
## Residuals:
##       Min        1Q    Median        3Q       Max 
## -0.011269 -0.001837  0.000391  0.003866  0.007437 
## 
## Coefficients:
##              Estimate Std. Error t value Pr(>|t|)    
## (Intercept) 3.1020679  0.0039599   783.4   <2e-16 ***
## czas        0.2004343  0.0006382   314.1   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 0.005797 on 8 degrees of freedom
## Multiple R-squared:  0.9999,	Adjusted R-squared:  0.9999 
## F-statistic: 9.864e+04 on 1 and 8 DF,  p-value: < 2.2e-16
```

``` r
# c)
wspolczynniki <- coef(model_bakterie)
param_a <- exp(wspolczynniki[1])
param_b <- wspolczynniki[2]

cat(paste0("\nModel wykładniczy: Masa = ", round(param_a, 4), " * e^(", round(param_b, 4), " * czas)\n"))
```

```
## 
## Model wykładniczy: Masa = 22.2439 * e^(0.2004 * czas)
```

