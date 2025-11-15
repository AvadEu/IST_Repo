A <- matrix(c(3, 1, 2, 4, 5, 3), nrow = 2, byrow = TRUE)
B <- cbind(c(-1, 3, -5), c(2, -4, 6))
C <- matrix(c(7, 3, 2, 1), nrow = 2, ncol = 2, byrow = TRUE)
D <- rbind(c(1, 2, 4), c(3, 5, 7), c(5, 7, 11))


#A + B # Nie mozna (rózne wymiary macierzy)
A + t(B)
A %*% B
A * A
solve(D)
D %*% solve(D)

X1 <- solve(C) %*% A
X2 <- A %*% solve(D)