a <- seq(300, 0, by = -3)
b <- c("one", "two", "three", "four", 5)
c <- c("one", "two", "three", "four", "5")
d <- rep(c(3, 1, 6), times = 4)
e <- rep(c(3, 1, 6), each = 4)
f <- c(5, 1, 4, 7)


length(a)
min(a)
max(a)
sum(a)
typeof(a)

length(b)
min(b)
max(b)
# sum(b)
typeof(b)

length(c)
min(c)
max(c)
# sum(c)
typeof(c)

length(d)
min(d)
max(d)
sum(d)
typeof(d)

length(e)
min(e)
max(e)
sum(e)
typeof(e)

length(f)
min(f)
max(f)
sum(f)
typeof(f)

sort(b)
sort(e)

d + f
sum(d * e)
a[35]
a[67:85]

which(a < 100)
length(which(a < 100))