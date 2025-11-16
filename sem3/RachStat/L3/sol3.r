# zad 5
avg <- 170
std <- sqrt(144)
pnorm(q = 180, mean = avg, sd = std, lower.tail = FALSE)
pnorm(q = 165, mean = avg, sd = std)
pnorm(q = 190, mean = avg, sd = std) - pnorm(q = 155, mean = avg, sd = std)
qnorm(p = 0.9, mean = avg, sd = std)

# zad 6
static_prob <- 1 / 6
num_tries <- 180
dbinom(x = 27, size = num_tries, prob = static_prob)
pbinom(q = 31, size = num_tries, prob = static_prob, lower.tail = FALSE)
pbinom(q = 28, size = num_tries, prob = static_prob)
pbinom(q = 33, size = num_tries, prob = static_prob) - pbinom(q = 24, size = num_tries, prob = static_prob)