# Zad 1

dbinom(x = 5, size = 6, prob = 0.5)
1 - pbinom(q = 3, size = 6, prob = 0.5)
sum(dbinom(x = 2:4, size = 6, prob = 0.5))

x_vals <- 0:10
y_vals <- dbinom(x = x_vals, size = 10, prob = 0.5)

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
1 - ppois(q = 4, lambda = 6)
sum(dpois(x = 3:5, lambda = 6))
x_vals <- 0:30
y_vals <- dpois(x = x_vals, lambda = 6)
plot(
    x = x_vals,
    y = y_vals,
    type = "h",
    main = "Rozklad Poissona zad 2",
    lwd = 4,
    xlab = "Liczba zdarzen",
    ylab = "P(X = x)",
    col = "red"
)