generuj_rozklad <- function(n) {
    u <- runif(n)
    res <- numeric(n)
    res[u >= 0.75 & u < 0.9] <- 0 # 15%
    res[u >= 0.5 & u < 0.75] <- 1 # 25%
    res[u < 0.5] <- 2 # 50%
    res[u >= 0.9] <- 3 # 10%

    return(res)
}

dane <- generuj_rozklad(1000)
dane