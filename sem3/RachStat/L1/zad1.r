a <- c(1, 4, 6, 13, -10, 8)
b <- seq(1, 101, by = 2)
c <- rep(c(4, 7, 9), each = 3)
d <- c("czy", "to", "jest", "wektor", NA)
e <- c("czy", "to", "jest", "wektor", "NA")
f <- rep(c(4, 7, 9), times = 6)


# Zad 1.2
length(a)
min(a)
max(a)
sum(a)
typeof(a)

length(b)
min(b)
max(b)
sum(b)
typeof(b)

length(c)
min(c)
max(c)
sum(c)
typeof(c)

length(d)
min(d, na.rm = TRUE)
max(d, na.rm = TRUE)
# sum(d) # Nie działa na znakach
typeof(d)

length(e)
min(e)
max(e)
# sum(e) # Nie działa na znakach
typeof(e)

length(f)
min(f)
max(f)
sum(f)
typeof(f)

# Zad 1.3
sort(d)
sort(e)

# Zad 1.4
a + f
a * f
a + c
a + 10
15 * a
b[26]
f[6:10]
which(b > 50)
length(which(b > 50))