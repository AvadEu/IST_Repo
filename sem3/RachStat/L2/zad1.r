oceny <- data.frame(
    Imie = c("Krzysztof", "Maria", "Henryk", "Anna"),
    Plec = c("m", "k", "m", "k"),
    Analiza = c(3.5, 4.5, 5.0, 4.5),
    Algebra = c(4.0, 5.0, 4.0, 3.5)
)

print(oceny)

# B
head(oceny, 2)

# C
str(oceny)

# D
mean(oceny$Analiza)

# E
oceny$Srednia <- (oceny$Analiza + oceny$Algebra) / 2
print(oceny)

# F
kobiety <- oceny[oceny$Plec == "k", "Analiza"]
print(kobiety)

# G
co_najmniej_4_5 <- subset(oceny, Analiza >= 4.5 | Algebra >= 4.5)
print(co_najmniej_4_5)

# H
liczba_osob <- sum(oceny$Analiza >= 4.5)
print(liczba_osob)