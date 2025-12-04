my_inv <- function() {
    u <- runif(1)
    x <- 2 * sqrt(u)
    return(x)
}

inv_samples <- replicate(200, my_inv())
hist(inv_samples, probability = TRUE)

my_rejection <- function() {
    repeat {
        x <- runif(1, 0, 2) # próbka z rozkładu pomocniczego
        u <- runif(1)
        if (u < (0.5 * x) / 1) { # M = 1 bo max g(x)=1
            return(x)
        }
    }
}

rej_samples <- replicate(200, my_rejection())
hist(rej_samples, probability = TRUE)
