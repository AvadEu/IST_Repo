# Zad 1

dbinom(x = 5, size = 6, prob = 0.5)
1 - pbinom(q = 2, size = 6, prob = 0.5)
pbinom(4, size=6, prob=0.5) - pbinom(1, size=6, prob=0.5)

x_vals <- 0:6
y_vals <- dbinom(x = x_vals, size = 6, prob = 0.5)

plot(
    x = x_vals,
    y = y_vals,
    type="h",
    main="Rozklad dwumianowy zad 1",
    lwd = 4,
    xlab = "Liczba reszek",
    ylab = "P(X = x)",
    col = "blue"
)

# Zad 2
dpois(x = 5, lambda = 6)
1 - ppois(q = 3, lambda = 6)
ppois(5, lambda = 6) - ppois(2, lambda = 6)
x_vals <- 0:30
y_vals <- dpois(x = x_vals, lambda = 6)
plot(
    x = x_vals,
    y = y_vals,
    type = "h",
    main = "Rozklad Poissona zad 2",
    lwd = 4,
    xlab = "Liczba sprzedanych samochodów",
    ylab = "P(X = x)",
    col = "red"
)