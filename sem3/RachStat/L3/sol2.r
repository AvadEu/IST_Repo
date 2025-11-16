# Zad 3

punif(q = 7, min = 4, max = 12)
punif(q = 11, min = 4, max = 12) - punif(q = 5, min = 4, max = 12)
1 - punif(q = 10, min = 4, max = 12)
qunif(p = 0.6, min = 4, max = 12)

# Zad 4
lambda <- 1 / 15
pexp(q = 30, rate = lambda, lower.tail = FALSE)
pexp(q = 20, rate = lambda)
pexp(q = 80, rate = lambda) - pexp(q = 40, rate = 1 / 15)
qexp(p = 0.2, rate = lambda, lower.tail = FALSE)
x_vals <- seq(0, 120, by = 0.5)
y_vals <- dexp(x_vals, rate = lambda)
plot(
    x = x_vals,
    y = y_vals,
    type = "l",
    main = "Funkcja gestosci rozkladu wykladniczego",
    col = "red",
    xlab = "Czas (s)",
    ylab = "Gestosc f(t)"
)