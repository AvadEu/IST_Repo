# Wyra�enie a) x = (a * b - c) / (a + c)
# Wyra�enie b) x = (b - c) * (a + b) / c
# Wyra�enie c) x= ((a - b) * c + a) / b

.data
menu_text: .asciiz "\n1. x = (a + b - c) / (a * d)\n2. x = (b - c) * (a + b) / c\n3. x = ((a - b) * c + a) / b\n4. x = ((b * a) / (c - a)) - ((c - b) / a)\n"
exp_text:  .asciiz "Podaj numer wyrazenia kt�rego wartosc chcesz obliczyc:\n"
get_nums:  .asciiz "Podaj wartosci zmiennych:\n"
get_a_text:.asciiz "a = "
get_b_text:.asciiz "b = "
get_c_text:.asciiz "c = "
err_input: .asciiz "Wybierz poprawna opcje!\n"
wynik_msg: .asciiz "Wartosc wyrazenia wynosi: "
reszta:    .asciiz " reszta: "
stop_msg:  .asciiz "Czy chcesz kontynuowac? (1 - TAK, 0 - NIE): "
new_line:  .asciiz "\n"
zero_err:  .asciiz "Blad danych. Dzielenie przez 0!\n"


.text

main:
	li $v0, 4 # Wy�wietl dostepne rownania
	la $a0, menu_text
	syscall
	
	la $a0, exp_text # Wyswietl informacje o wyborze rownania
	syscall
	
	li $v0, 5 # Wczytanie wyboru u?ytkownika
  	syscall
  	move $t0, $v0

	la $t1, 1
	beq $t1, $t0, policz1 # Sprawdzenie czy wybrano rownanie 1
	
	la $t1, 2
	beq $t1, $t0, policz2# Sprawdzenie czy wybrano rownanie 2
	
	la $t1, 3
	beq $t1, $t0, policz3 # Sprawdzenie czy wybrano rownanie 3
	
	la $t1, 4
	beq $t1, $t0, policz4 # Sprawdzenie czy wybrano r�wnanie 4
	
	li $v0, 4 # Wyswietlenie komunikatu o niepoprawnych danych
	la $a0, err_input
	syscall
	
	j main # Zacznij main od nowa jezeli nie poprawny wynik
	
wczytaj_zmienne:
	li $v0, 4 # Wyswietl komunikat do wczytywania danych
	la $a0, get_nums
	syscall
	
	la $a0, get_a_text # Wyswietl komunikat do wpisania a
	syscall
	li $v0, 5 # Wczytaj zmienna a do $s0
	syscall
	move $s0, $v0
	
	li $v0, 4 # Wyswietl komunikat do wpisania b
	la $a0, get_b_text
	syscall
	li $v0, 5 # Wczytaj zmienna b do $s2
	syscall
	move $s1, $v0
	
	li $v0, 4 # Wyswietl komunikat do wpisania c
	la $a0, get_c_text
	syscall
	li $v0, 5 # Wczytaj zmienna c do $s2
	syscall
	move $s2, $v0
	
	jr $ra # Powr�t do wykonywania funkcji poprzedniej

finish_program: 
	li $v0, 10 # Zakonczenie programu
	syscall
	
policz1:
	jal wczytaj_zmienne # Przesskakuje do wczytania zmiennych
	mul $t1, $s0, $s1 # Wykonuje dzialanie a * b
	sub $t2, $t1, $s2 # Wykonuje dzilanie [a * b] - c
	add $t3, $s0, $s2 # Wykonuje dzialanie a + c
	
	move $s7, $t3 # Przeniesienie dzielnika do $s7
	jal czy_zero
	div $t2, $t3 # Wykonuje dzialanie (a * b - c) / (a + c)
	
	mflo $s5 # Zapisuje wynik dzielenia w $s5
	mfhi $s6 # Zapisuje reszte z dzielenia w $s6
	
	la $t0, -1
	beq $t0, $s6, reszta_zero
	
	j print_wynik
	
policz2:
	jal wczytaj_zmienne # Przeskakuje do wczytania zmiennych
	sub $t1, $s1, $s2 # Wykonuje b - c
	add $t2, $s0, $s1 # Wykonuje a + b
	mul $t3, $t1, $t2 # Wykonuje (b - c) * (a + b)
	
	move $s7, $s2 # Przeniesienie dzielnika do $s7
	jal czy_zero
	div $t3, $s2
	
	mflo $s5 # Zapisuje wynik dzielenia w $s5
	mfhi $s6 # Zapisuje reszte z dzielenia w $s6
	
	la $t0, -1
	beq $t0, $s6, reszta_zero
	
	j print_wynik
	
policz3:
	jal wczytaj_zmienne 
	sub $t1, $s0, $s1 # Wykonuje a - b
	mul $t2, $t1, $s2 # Wykonuje (a - b) * c
	add $t3, $t2, $s0 # Wykonuje (a - b) * c + a 
	
	move $s7, $s1 # Przeniesienie dzielnika do $s7
	jal czy_zero
	div $t3, $s1
	
	mflo $s5 # Zapisuje wynik dzielenia w $s5
	mfhi $s6 # Zapisuje reszte z dzielenia w $s6
	
	la $t0, -1
	beq $t0, $s6, reszta_zero
	
	j print_wynik
	
print_wynik:
	li $v0, 4 # Wyswietlenie wiadomosci o wniku
	la $a0, wynik_msg
	syscall
	
	li $v0, 1 # Wyswietlenie wyniku
	la $a0, ($s5)
	syscall
	
	li $v0, 4 # Wyswietlenie wiadomosci o reszcie
	la $a0, reszta
	syscall
	
	li $v0, 1 # Wyswietlenie reszty
	la $a0, ($s6)
	syscall
	
	li $v0, 4 # Wyswietlenie nowej linii
	la $a0, new_line
	syscall
	
	j czy_stop
	
czy_stop:
	li $v0, 4 # Wyswietlenie komunikatu czy kontynuowac
	la $a0, stop_msg
	syscall
	
	li $v0, 5 # Wczytanie odpowiedzi uzytkownika
	syscall
	move $t5, $v0

	la $t6, 0 # Sprawdzenie czy program ma sie zakonczyc
	beq $t5, $t6, finish_program
	
	la $t6, 1  # Sprawdzenie czy program ma byc kontynuowany
	beq $t6, $t5, main
	
	li $v0, 4 # Wyswietla komunikat o b��dnych danych
	la $a0, err_input
	syscall
	
	j czy_stop # Resetuje funkcje

czy_zero:
	beq $s7, $zero, zero_output # Sprawdzenie czy dzielnik jest rowny 0
	jr $ra # Powrot to obliczen
	
zero_output:
	li $v0, 4 # Wypisannie komunikatu o dzieleniu przez 0
	la $a0, zero_err
	syscall
	
	j czy_stop # Powrot do poczatku programu 
	
reszta_zero:
	la $s6, 0
	j print_wynik

policz4:
	jal wczytaj_zmienne
	mul $t1, $s1, $s0 # Wykonuje dzia?anie b * a
	sub $t2, $s2, $s0 # Wykonuje dzia?anie c - a
	move $s7, $t2 # Przeniesienie dzielnika do $s7
	jal czy_zero # Sprawdzenie dzielenia przez 0
	
	div $t1, $t2 # Wykonuje dzia?anie (b * a) / (c - a)
	mflo $t4 # Wynik dzielenia
	mfhi $t5 # Reszta
	
	sub $t3, $s2, $s1 # Wykonuje dzia?anie c - b
	move $s7, $s0 # Przenisienie dzielnika do $s7
	jal czy_zero # Sprawdzenie dzielenia przez 0
	
	div $t3, $s0 # Wykonuje dzia?anie (c - b) / a
	mflo $t6 # Wynik dzielenia
	mfhi $t7 # Reszta
	
	abs $t5, $t5
	abs $t7, $t7
	add $t8, $t5, $t7 # Suma reszty
	move $s6, $t8 # Przeniesienie $t8 do $s6
	
	la $t0, -1
	beq $t0, $s6, reszta_zero
	
	sub $s5, $t4, $t6 # Wynik dzia?ania (b * a) / (c - a) - (c - b) / a
	
	j print_wynik