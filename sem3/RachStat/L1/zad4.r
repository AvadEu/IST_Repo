A <- matrix(c(-3, 1, -2, 4, -5, 3), nrow = 2, byrow = TRUE)
B <- cbind(c(1, 3, 5), c(2, 4, 6))
C <- matrix(c(7, -3, -2, 1), nrow = 2, ncol = 2, byrow = TRUE)
D <- rbind(c(1, 2, 4), c(3, 5, 7), c(2, 3, 2))


#A + B # Nie mozna (rózne wymiary macierzy)
t(A) + B
B %*% A
B * B
solve(C)
C %*% solve(C)

X1 <- B %*% solve(C)
X2 <- solve(D) %*% B