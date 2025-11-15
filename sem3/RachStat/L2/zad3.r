mieszkania <- read.csv2("mieszkania.csv", sep = ";", header = TRUE)

# B
head(mieszkania)

# C
str(mieszkania)

# D
mean(mieszkania$Metraz)
mean(mieszkania$Cena)

# E
mieszkania$Cena_za_metr <- (mieszkania$Cena / mieszkania$Metraz)

# F
psie_pole_ponizej_400tys <- mieszkania[mieszkania$Dzielnica == "Psie Pole" & mieszkania$Cena < 400000, ]

# G
srodmiescie_powyzej_60m <- mieszkania[mieszkania$Dzielnica == "Srodmiescie" & mieszkania$Metraz > 60, ]

# G
sum(mieszkania$Metraz > 60 & mieszkania$Cena < 350000)

# I
mieszkania$smdc <- (mieszkania$Metraz / mieszkania$Pokoje) / mieszkania$Cena
najlepsze <- mieszkania[which.max(mieszkania$smdc), ]
najlepsze

# J
odchylenia_dzielnic <- tapply(mieszkania$Cena_za_metr, mieszkania$Dzielnica, sd)

odchylenia_dzielnic <- data.frame(
    dzielnica = names(odchylenia_dzielnic),
    odchylenie = odchylenia_dzielnic,
    row.names = NULL
)

stabilna <- odchylenia_dzielnic[which.min(odchylenia_dzielnic$odchylenie), ]

zroznicowana <- odchylenia_dzielnic[which.max(odchylenia_dzielnic$odchylenie), ]

stabilna
zroznicowana