studenci <- read.csv2("waga1.csv", sep = ";", header = TRUE)

# B
head(studenci, 5)

# C
str(studenci)

# D
mean(studenci$Wzrost)
mean(studenci$Waga_przed)

# E
studenci$Wskaznik_wagi <- (studenci$Waga_przed / (studenci$Wzrost/100)^2)

# F
kobiety_25 <- studenci[studenci$plec == 1 & studenci$Wskaznik_wagi > 25, ]
kobiety_25

# G
mezczyzni <- studenci[studenci$plec == 0, ]

# H
sum(studenci$Wzrost >= 175)