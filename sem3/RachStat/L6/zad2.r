interpretuj_wynik <- function(p_val) {
  cat("Wartość p =", format(p_val, scientific = FALSE), "\n")
  
  if (p_val > 0.05) {
    cat("Wniosek: Nie odrzucamy hipotezy zerowej na poziomie istotności 5%.\nNie mamy dowodów przeciwko H0.\n") 
  } else if (p_val > 0.01) {
    cat("Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 5%.\nMamy dowody przeciwko H0.\n")
  } else if (p_val > 0.001) {
    cat("Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 1%.\nMamy mocne dowody przeciwko H0.\n")
  } else {
    cat("Wniosek: Odrzucamy hipotezę zerową na poziomie istotności 0,1%.\nMamy bardzo mocne dowody przeciwko H0.\n")
  }
}

dane <- read.csv("waga1.csv", header=TRUE, sep=";")

waga_diff <- na.omit(dane$Waga_po - dane$Waga_przed)


cat("\nZadanie 2\n")
result <- t.test(waga_diff, mu = 2)
result$p.value
interpretuj_wynik(result$p.value)

cat("\nZadanie 3\n")
kobiety <- nrow(dane[dane$plec == 1,])
kobiety_ponad_70 <- nrow(dane[dane$plec ==1 & dane$Waga_po > 70, ])
kobiety_ponizej_70 <- kobiety - kobiety_ponad_70

mezczyzni <- nrow(dane[dane$plec == 0,])
mezczyzni_ponad_70 <- nrow(dane[dane$plec ==0 & dane$Waga_po > 70, ])
mezczyzni_ponizej_70 <- mezczyzni - mezczyzni_ponad_70

tablica <- matrix(c(kobiety_ponad_70, mezczyzni_ponad_70, kobiety_ponizej_70, mezczyzni_ponizej_70), nrow = 2, byrow = TRUE)
colnames(tablica) <- c("kobiety", "Mężczyźni")
rownames(tablica) <- c("Ponad 70kg", "70kg i mniej")
tablica

result<-chisq.test(tablica)
interpretuj_wynik(result$p.value)
result$p.value

cat("\nZadanie 4\n")

wzrost_m <- dane$Wzrost[dane$plec == 0]
wzrost_k <- dane$Wzrost[dane$plec == 1]

result4 <- t.test(wzrost_m, wzrost_k, mu = 5)
result4$p.value
interpretuj_wynik(result4$p.value)


cat("\nZadanie 5\n")

liczba_przytyli <- sum(waga_diff > 0)
liczba_wszystkich <- nrow(dane)

result5 <- prop.test(liczba_przytyli, n = liczba_wszystkich, p = 0.8)

result5$p.value
interpretuj_wynik(result5$p.value)


cat("\nZadanie 6\n")

roznica_m <- waga_diff[dane$plec == 0]
result6 <- t.test(roznica_m, mu = 4)

result6$p.value
interpretuj_wynik(result6$p.value)