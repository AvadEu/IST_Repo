n <- 100 # Liczba studentów
x <- 109 # Średnie IQ w próbie
s2 <- 225 # Wariancja z próby
s <- sqrt(s2) # Odchylenie standardowe = 15
liczba_wyzszych <- 30 # Liczba studentów z IQ > 115
p <- liczba_wyzszych / n # Proporcja z próby = 0.3

cat("Podpunkt A\n")
# Hipotezy:
# H0: p = 0.35 (35% studentów ma IQ > 115)
# H1: p != 0.35

# i

p0 <- 0.35
SE_p <- sqrt(p0 * (1 - p0) / n) # Błąd standardowy
Z <- (p - p0) / SE_p
p_value_Z <- 2 * pnorm(-abs(Z))

round(Z, 4)
round(p_value_Z, 4)

# Na podstawie p = 0.2945 > 0.05, nie odrzucamy Hipotezy zerowej,
#nie mamy dowodów, że proporcja studentów z IQ > 115 różni się od 35%


# ii
prop.test(30, 100, p = 0.35, correct = FALSE)$p.value

cat("Podpunkt B\n")
# i

z_99 <- qnorm(0.995) # Wartość krytyczna dla 99%: 1 - a/2 = 0.995
margines_norm <- sqrt(p * (1 - p) / n)
przedzial_norm <- c(p - z_99 * margines_norm, p + z_99 * margines_norm)
cat("Przedział ufności 99% = [", round(przedzial_norm[1], 4), ";", round(przedzial_norm[2], 4), "]\n")

# ii
prop.test(liczba_wyzszych, n, conf.level = 0.99, correct = FALSE)


cat("Podpunkt C\n")

z_90 <- qnorm(0.95)  # 90%: 1 - α/2 = 0.95
margines_z <- z_90 * s / sqrt(n)
przedzial_z <- c(x - margines_z, x + margines_z)
cat("Przedział ufności 90%: [", round(przedzial_z[1], 2), ";", round(przedzial_z[2], 2), "]\n")

cat("Podpunkt D\n")

t_90 <- qt(0.95, df = n - 1)  # df = n-1 = 99
margines_t <- t_90 * s / sqrt(n)
przedzial_t <- c(x - margines_t, x + margines_t)
cat("Przedział ufności 90%, rozkład studenta: [", round(przedzial_t[1], 2), ";", round(przedzial_t[2], 2), "]\n")

cat("Podpunkt E\n")
# H0: Średnie IQ wynosi 115
# H1: Średnie IQ NIE wynosi 115

mu0 <- 115

# i) Test Z dla średniej
z_iq <- (x - mu0) / (s / sqrt(n))
p_value_z_iq <- 2 * pnorm(-abs(z_iq))
p_value_z_iq

# ii) Test t-Studenta dla średniej
p_value_t_iq <- 2 * pt(-abs(z_iq), df = n - 1)
p_value_t_iq

# Wniosek:

# Dla Z
# Skoro p < 0.0001
# To odrzucamy H0 na poziomie istotności 0.01%

# Dla t-studenta
# Skoro p < 0.001
# To odrzucamy H0 na poziomie istotności 0.1%