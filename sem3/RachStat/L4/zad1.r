set.seed(131)

u <- runif(5000, min = 0, max = 1)

hist(u, probability = FALSE, main = "Histogram U(0,1)")

dens_u <- density(u)
plot(dens_u, main = "Estymator jadrowy dla U(0,1)")

x <- rnorm(3000, mean = 100, sd = 15)

hist(x, probability = FALSE, main="Histogram N(100,15)")
dens_x <- density(x)
plot(dens_x, main="Estymator jadrowy dla N(100,15)")