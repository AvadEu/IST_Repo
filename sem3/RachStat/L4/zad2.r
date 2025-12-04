u <- runif(600)
dice <- ceiling(6 * u)  # przekształcenie na liczby 1–6

mean(dice)
var(dice)

freq <- table(dice)
freq

df <- as.data.frame(freq)
df
var(df$Freq)

dice2 <- sample(1:6, size = 600, replace = TRUE)
table(dice2)
