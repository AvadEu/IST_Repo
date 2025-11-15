.data
X: 			.byte 'X'
O: 			.byte 'O'
wall: 			.byte '|'
space: 			.byte ' '
newLine: 		.byte '\n'
plansza: 		.space 9

gamer_x_move_txt: 	.asciiz "\nTwoj ruch! Podaj numer dostepnego pola w ktore chcesz wstawic X"
gamer_o_move_txt: 	.asciiz "\nTwoj ruch! Podaj numer dostepnego pola w ktore chcesz wstawic O"
new_game_prompt: 	.asciiz "Czy chcesz zaczac gre od nowa? (1 - TAK, 0 - NIE)\nWybor" 
err_input_prompt: 	.asciiz "Wybrano niepoprawna opcje. Sprobuj ponownie!\n" 
rounds_num_prompt: 	.asciiz "\nWpisz ile rund chcesz rozegrac (od 1 do 5)"
next_move_prompt: 	.asciiz "Nacisnij ENTER, aby zobaczyc nastepny ruch"
gameover2_prompt: 	.asciiz "GAMEOVER! GRA KONCZY SIE REMISEM!"	
draw_prompt: 		.asciiz "Remis! Obaj gracze otrzymuja punkt"
bad_move_prompt: 	.asciiz "\nBledny ruch! Wybierz inne pole"	
char_err_txt:	  	.asciiz "\nPodaj poprawny znak [X lub O]\n"
znakPrompt: 		.asciiz "Wybierz swoj znak (X lub O): "
comp_move_prompt: 	.asciiz "\nKomputer wykonal ruch!\n"
gameover_prompt: 	.asciiz "KONIEC GRY! WYGRYWA "
score_prompt: 		.asciiz "Aktualny wynik"
round_win_prompt: 	.asciiz "Runde wygrywa "
floor: 			.asciiz "-----------"
round: 			.asciiz "RUNDA NR "
inputIndicator: 	.asciiz ": "

.text
main:
    move $s1, $zero                     # Wynik gracza X ($s1) ustawiony na 0
    move $s2, $zero                     # Wynik gracza O ($s2) ustawiony na 0
    move $s3, $zero                     # Licznik rund ($s3) ustawiony na 0

    j wybierzZnak                       # Skok do etykiety wyboru znaku przez gracza
	
return_val:
		jr $ra			                # Powrót z funkcji (skok do adresu w rejestrze $ra)
		
	exit:
		li $v0, 10		                # Wczytanie kodu syscall 10 (zakończenie programu) do $v0
		syscall			                # Wywołanie systemowe kończące program
		
err_input_prompt_link:
		li $v0, 4		                # Wczytanie kodu syscall 4 (wypisanie tekstu) do $v0
		la $a0, err_input_prompt        # Wczytanie adresu komunikatu o błędzie do $a0
		syscall			                # Wywołanie systemowe wypisujące tekst

		j return_val	                # Powrót z funkcji
		
	wyswietlPlansze_link:
		move $t0, $zero		            # Zerowanie licznika wierszy ($t0)
		
		subi $sp, $sp, 4	            # Przesunięcie wskaźnika stosu, aby zrobić miejsce
	sw $ra, 0($sp)		                # Zapisanie adresu powrotu na stosie
	jal petlaWyswietlPlansze_link       # Wywołanie funkcji pętli wyświetlającej planszę
	lw $ra, 0($sp)		                # Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	                # Przywrócenie wskaźnika stosu
	
		j return_val		            # Powrót z funkcji
	petlaWyswietlPlansze_link:
		move $t1, $zero		            # Zerowanie licznika kolumn ($t1)
		
		li $v0, 11		                # Wczytanie kodu syscall 11 (wypisanie znaku) do $v0
		lb $a0, space		            # Wczytanie znaku spacji do $a0
		syscall			                # Wywołanie systemowe wypisujące znak
		
		subi $sp, $sp, 4	            # Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		                # Zapisanie adresu powrotu na stosie
	jal petlaWyswietlPlanszeRzad_link   # Wywołanie funkcji pętli wyświetlającej rząd
	lw $ra, 0($sp)		                # Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	                # Przywrócenie wskaźnika stosu
	
		addi $t0, $t0, 1	            # Inkrementacja licznika wierszy
		
		li $v0, 11		                # Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, newLine		            # Wczytanie znaku nowej linii do $a0
		syscall			                # Wywołanie systemowe wypisujące znak
		
		beq $t0, 3, return_val          # Jeśli wyświetlono 3 wiersze, zakończ
		
		li $v0, 4		                # Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, floor		            # Wczytanie adresu separatora wierszy do $a0
		syscall			                # Wywołanie systemowe wypisujące tekst
		li $v0, 11		                # Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, newLine		            # Wczytanie znaku nowej linii
		syscall			                # Wywołanie systemowe wypisujące znak
		j petlaWyswietlPlansze_link     # Skok do początku pętli wyświetlającej wiersz
	
	petlaWyswietlPlanszeRzad_link:
		mul $t2, $t0, 3		            # Obliczenie offsetu wiersza (wiersz * 3)
		add $t2, $t2, $t1	            # Obliczenie indeksu pola (offset + kolumna)
		li $v0, 11		                # Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, plansza($t2)	        # Wczytanie znaku z planszy pod obliczonym indeksem
		syscall			                # Wywołanie systemowe wypisujące znak
		
		addi $t1, $t1, 1	# Inkrementacja licznika kolumn
		beq $t1, 3, return_val	# Jeśli wyświetlono 3 kolumny, zakończ
		lb $a0, space		# Wczytanie znaku spacji
		syscall			# Wywołanie systemowe
		lb $a0, wall		# Wczytanie znaku '|'
		syscall			# Wywołanie systemowe
		lb $a0, space		# Wczytanie znaku spacji
		syscall			# Wywołanie systemowe
		j petlaWyswietlPlanszeRzad_link # Skok do początku pętli wyświetlającej kolumnę

resetPlansza_link:
	addi $t0, $zero, 1	# Inicjalizacja licznika ($t0) wartością 1
	la $t1, plansza		# Wczytanie adresu planszy do $t1
	
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	jal petlaResetPlansza_link # Wywołanie pętli resetującej planszę
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	
	j return_val		# Powrót z funkcji
	
petlaResetPlansza_link:
	bgt $t0, 10, return_val	# Jeśli licznik > 10, zakończ pętlę
	addi $t2, $t0, 48	# Konwersja liczby (1-9) na jej kod ASCII ('1'-'9')
	sb $t2, 0($t1)		# Zapisanie znaku (cyfry) na planszy
	addi $t1, $t1, 1	# Przesunięcie wskaźnika na następne pole planszy
	addi $t0, $t0, 1	# Inkrementacja licznika
	j petlaResetPlansza_link # Skok do początku pętli

#! ----- Uzytkownik wybiera znak -------
wybierzZnak:
    li $v0, 4					# Wczytanie kodu syscall 4 (wypisanie tekstu)
    la $a0, znakPrompt			# Wczytanie adresu tekstu z prośbą o wybór znaku
    syscall					# Wywołanie systemowe

    li $v0, 12       			# Wczytanie kodu syscall 12 (wczytanie znaku)
    syscall					# Wywołanie systemowe
    move $t6, $v0    			# Przeniesienie wczytanego znaku z $v0 do $t6

    li $t7, 'X'					# Wczytanie znaku 'X' do $t7 w celu porównania
    beq $t6, $t7, graczJestX	# Jeśli wczytany znak to 'X', skocz do graczJestX

    li $t7, 'O'					# Wczytanie znaku 'O' do $t7 w celu porównania
    beq $t6, $t7, graczJestO	# Jeśli wczytany znak to 'O', skocz do graczJestO

    li $v0, 4					# Wczytanie kodu syscall 4 (wypisanie tekstu)
    la $a0, char_err_txt		# Wczytanie adresu komunikatu o błędzie
    syscall					# Wywołanie systemowe
    j wybierzZnak				# Skok z powrotem do wyboru znaku

graczJestX:
    li $t4, 1     # Ustawienie wskaźnika tury ($t4) na 1 (tura gracza)
	li $s7, 1     # Ustawienie wskaźnika znaku gracza ($s7) na 1 (gracz to X)
    j liczbaRund				# Skok do wyboru liczby rund

graczJestO:
    li $t4, -1    # Ustawienie wskaźnika tury ($t4) na -1 (tura komputera)
	li $s7, 0     # Ustawienie wskaźnika znaku gracza ($s7) na 0 (gracz to O)
    j liczbaRund				# Skok do wyboru liczby rund

# Organizacja gry
liczbaRund:
	li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, rounds_num_prompt # Wczytanie adresu tekstu z prośbą o liczbę rund
		syscall			# Wywołanie systemowe
		la $a0, inputIndicator	# Wczytanie adresu wskaźnika do wprowadzenia danych
		syscall			# Wywołanie systemowe
		li $v0, 5		# Wczytanie kodu syscall 5 (wczytanie liczby całkowitej)
		syscall			# Wywołanie systemowe
		move $s0, $v0		# Przeniesienie wczytanej liczby rund do $s0
		blt $s0, 1, err_input_print # Jeśli liczba rund < 1, skocz do błędu
		bgt $s0, 5, err_input_print # Jeśli liczba rund > 5, skocz do błędu
		bgt $s0, 0, trybGry	# Jeśli liczba rund jest poprawna, skocz do trybu gry
		jal err_input_prompt_link # Wywołanie funkcji wyświetlającej błąd
		j liczbaRund		# Skok z powrotem do wyboru liczby rund

err_input_print:
	li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
	la $a0, err_input_prompt # Wczytanie adresu komunikatu o błędzie
	syscall			# Wywołanie systemowe
	j liczbaRund		# Skok z powrotem do wyboru liczby rund

trybGry:
		j trybGracz		# Skok do trybu gry gracz vs komputer
		
	trybGracz:
		bge $s3, $s0, wyniki	# Jeśli aktualna runda >= liczba rund, skocz do wyników
		addi $s3, $s3, 1	# Inkrementacja licznika rund
		
		jal resetPlansza_link	# Wywołanie funkcji resetującej planszę
		
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, round		# Wczytanie adresu tekstu "RUNDA NR"
		syscall			# Wywołanie systemowe
		li $v0, 1		# Wczytanie kodu syscall 1 (wypisanie liczby całkowitej)
		move $a0, $s3		# Przeniesienie numeru rundy do $a0
		syscall			# Wywołanie systemowe
		li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, newLine		# Wczytanie znaku nowej linii
		syscall			# Wywołanie systemowe
		
		move $t3, $zero		# Wyzerowanie stanu rundy ($t3=0 oznacza w toku)
		li $t4, 1		# Ustawienie tury na gracza X (X zawsze zaczyna rundę)
		jal rundaGracz_link	# Wywołanie głównej pętli rundy
		
		j trybGracz		# Skok do następnej rundy
		
	punktX:
		subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	jal wyswietlPlansze_link # Wywołanie funkcji wyświetlającej planszę
		addi $s1, $s1, 1	# Dodanie punktu dla gracza X
		
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, round_win_prompt # Wczytanie adresu tekstu o wygranej w rundzie
		syscall			# Wywołanie systemowe
		li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, X		# Wczytanie znaku 'X'
		syscall			# Wywołanie systemowe
		lb $a0, newLine		# Wczytanie znaku nowej linii
		syscall			# Wywołanie systemowe
		
	jal aktualnyWynik_link	# Wywołanie funkcji wyświetlającej aktualny wynik
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
		
		j return_val		# Powrót z funkcji
	punktO:
		subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	jal wyswietlPlansze_link # Wywołanie funkcji wyświetlającej planszę
		addi $s2, $s2, 1	# Dodanie punktu dla gracza O
		
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, round_win_prompt # Wczytanie adresu tekstu o wygranej w rundzie
		syscall			# Wywołanie systemowe
		li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, O		# Wczytanie znaku 'O'
		syscall			# Wywołanie systemowe
		lb $a0, newLine		# Wczytanie znaku nowej linii
		syscall			# Wywołanie systemowe
		
	jal aktualnyWynik_link	# Wywołanie funkcji wyświetlającej aktualny wynik
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
		
		j return_val		# Powrót z funkcji
	remis:
		subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	jal wyswietlPlansze_link # Wywołanie funkcji wyświetlającej planszę
		addi $s1, $s1, 1	# Dodanie punktu dla gracza X
		addi $s2, $s2, 1	# Dodanie punktu dla gracza O
		
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, draw_prompt	# Wczytanie adresu tekstu o remisie
		syscall			# Wywołanie systemowe
		li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, newLine		# Wczytanie znaku nowej linii
		syscall			# Wywołanie systemowe
		
	jal aktualnyWynik_link	# Wywołanie funkcji wyświetlającej aktualny wynik
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
		
		j return_val		# Powrót z funkcji
		
	aktualnyWynik_link:
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, score_prompt	# Wczytanie adresu tekstu "Aktualny wynik"
		syscall			# Wywołanie systemowe
		la $a0, inputIndicator	# Wczytanie adresu wskaźnika
		syscall			# Wywołanie systemowe
		li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, newLine		# Wczytanie znaku nowej linii
		syscall			# Wywołanie systemowe
		lb $a0, X		# Wczytanie znaku 'X'
		syscall			# Wywołanie systemowe
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, inputIndicator	# Wczytanie adresu wskaźnika
		syscall			# Wywołanie systemowe
		li $v0, 1		# Wczytanie kodu syscall 1 (wypisanie liczby)
		move $a0, $s1		# Przeniesienie wyniku gracza X do $a0
		syscall			# Wywołanie systemowe
		li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, newLine		# Wczytanie znaku nowej linii
		syscall			# Wywołanie systemowe
		lb $a0, O		# Wczytanie znaku 'O'
		syscall			# Wywołanie systemowe
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, inputIndicator	# Wczytanie adresu wskaźnika
		syscall			# Wywołanie systemowe
		li $v0, 1		# Wczytanie kodu syscall 1 (wypisanie liczby)
		move $a0, $s2		# Przeniesienie wyniku gracza O do $a0
		syscall			# Wywołanie systemowe
		li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, newLine		# Wczytanie znaku nowej linii
		syscall			# Wywołanie systemowe
		j return_val		# Powrót z funkcji
	
	wyniki:
		sub $s3, $s1, $s2	# Obliczenie różnicy wyników (X - O)
		beqz $s3, wynikRemis	# Jeśli różnica wynosi 0, skocz do remisu
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, gameover_prompt	# Wczytanie adresu tekstu o końcu gry
		syscall			# Wywołanie systemowe
		li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
		bgezal $s3, markPlayer	# Jeśli X >= O, wywołaj markPlayer (błędna logika)
		bltzal $s3, markComputer # Jeśli O > X, wywołaj markComputer (błędna logika)
		syscall			# Wywołanie systemowe w celu wypisania znaku zwycięzcy
		lb $a0, newLine		# Wczytanie znaku nowej linii
		syscall			# Wywołanie systemowe
	
	newGame:
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, new_game_prompt	# Wczytanie adresu pytania o nową grę
		syscall			# Wywołanie systemowe
		la $a0, inputIndicator	# Wczytanie adresu wskaźnika
		syscall			# Wywołanie systemowe
		li $v0, 5		# Wczytanie kodu syscall 5 (wczytanie liczby)
		syscall			# Wywołanie systemowe
		beq $v0, 1, main	# Jeśli wpisano 1, zacznij od nowa (skok do main)
		beq $v0, $zero, exit	# Jeśli wpisano 0, zakończ program
		
		la $a0, err_input_prompt # Wczytanie adresu komunikatu o błędzie
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		syscall			# Wywołanie systemowe
		j newGame		# Skok z powrotem do pytania o nową grę
	
	wynikRemis:
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, gameover2_prompt # Wczytanie adresu tekstu o remisie w grze
		syscall			# Wywołanie systemowe
		li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
		lb $a0, newLine		# Wczytanie znaku nowej linii
		syscall			# Wywołanie systemowe
		j newGame		# Skok do pytania o nową grę

sprawdzStanPlanszy_link:
	la $t5, plansza		# Wczytanie adresu planszy do $t5
	
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	
	# Rzad 1
	lb $t0,0($t5)		# Wczytanie pola 0 do $t0
	lb $t1,1($t5)		# Wczytanie pola 1 do $t1
	lb $t2,2($t5)		# Wczytanie pola 2 do $t2
	jal sprawdzLinie_link	# Wywołanie funkcji sprawdzającej linię
	
	# Rzad 2
	lb $t0,3($t5)		# Wczytanie pola 3 do $t0
	lb $t1,4($t5)		# Wczytanie pola 4 do $t1
	lb $t2,5($t5)		# Wczytanie pola 5 do $t2
	jal sprawdzLinie_link	# Wywołanie funkcji sprawdzającej linię
	
	# Rzad 3
	lb $t0,6($t5)		# Wczytanie pola 6 do $t0
	lb $t1,7($t5)		# Wczytanie pola 7 do $t1
	lb $t2,8($t5)		# Wczytanie pola 8 do $t2
	jal sprawdzLinie_link	# Wywołanie funkcji sprawdzającej linię
	
	# Kolumna 1
	lb $t0,0($t5)		# Wczytanie pola 0 do $t0
	lb $t1,3($t5)		# Wczytanie pola 3 do $t1
	lb $t2,6($t5)		# Wczytanie pola 6 do $t2
	jal sprawdzLinie_link	# Wywołanie funkcji sprawdzającej linię
	
	# Kolumna 2
	lb $t0,1($t5)		# Wczytanie pola 1 do $t0
	lb $t1,4($t5)		# Wczytanie pola 4 do $t1
	lb $t2,7($t5)		# Wczytanie pola 7 do $t2
	jal sprawdzLinie_link	# Wywołanie funkcji sprawdzającej linię
	
	# Kolumna 3
	lb $t0,2($t5)		# Wczytanie pola 2 do $t0
	lb $t1,5($t5)		# Wczytanie pola 5 do $t1
	lb $t2,8($t5)		# Wczytanie pola 8 do $t2
	jal sprawdzLinie_link	# Wywołanie funkcji sprawdzającej linię
	
	# Przekatna 1
	lb $t0,0($t5)		# Wczytanie pola 0 do $t0
	lb $t1,4($t5)		# Wczytanie pola 4 do $t1
	lb $t2,8($t5)		# Wczytanie pola 8 do $t2
	jal sprawdzLinie_link	# Wywołanie funkcji sprawdzającej linię
	
	# Przekatna 2
	lb $t0,2($t5)		# Wczytanie pola 2 do $t0
	lb $t1,4($t5)		# Wczytanie pola 4 do $t1
	lb $t2,6($t5)		# Wczytanie pola 6 do $t2
	jal sprawdzLinie_link	# Wywołanie funkcji sprawdzającej linię
	
	# Remis
	move $t0, $zero		# Zerowanie licznika zajętych pól ($t0)
	move $t1, $zero		# Zerowanie licznika sprawdzonych pól ($t1)
	jal sprawdzRemis_link	# Wywołanie funkcji sprawdzającej remis
	
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji

sprawdzLinie_link:
	beq $t0, $t1, sprawdzDrugie # Jeśli pierwsze pole równe drugiemu, sprawdzaj dalej
	j return_val		# W przeciwnym wypadku wróć

sprawdzDrugie:
	beq $t0, $t2, sprawdzZnak # Jeśli pierwsze pole równe trzeciemu, sprawdź znak
	j return_val		# W przeciwnym wypadku wróć

sprawdzZnak:
	beq $t0, 'X', pktX	# Jeśli znakiem jest 'X', skocz do przyznania punktu dla X
	beq $t0, 'O', pktO	# Jeśli znakiem jest 'O', skocz do przyznania punktu dla O
	j return_val		# W przeciwnym wypadku wróć

podliczLinie:
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	
	move $t7, $zero		# Zerowanie licznika 'X' w linii ($t7)
	move $t8, $zero		# Zerowanie licznika 'O' w linii ($t8)
	move $t9, $zero		# Zerowanie licznika wolnych pól w linii ($t9)
	move $s4, $t0		# Przeniesienie pierwszego znaku z linii do analizy
	jal zliczaj		# Wywołanie funkcji zliczającej
	move $s4, $t1		# Przeniesienie drugiego znaku z linii do analizy
	jal zliczaj		# Wywołanie funkcji zliczającej
	move $s4, $t2		# Przeniesienie trzeciego znaku z linii do analizy
	jal zliczaj		# Wywołanie funkcji zliczającej
	
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji

zliczaj:
	beq $s4, 'X', dodajX	# Jeśli znak to 'X', skocz do dodajX
	beq $s4, 'O', dodajO	# Jeśli znak to 'O', skocz do dodajO
	j dodajWolne		# W przeciwnym wypadku (wolne pole) skocz do dodajWolne

dodajX:
	addi $t7, $t7, 1	# Zwiększ licznik 'X'
	j return_val		# Powrót z funkcji

dodajO:
	addi $t8, $t8, 1	# Zwiększ licznik 'O'
	j return_val		# Powrót z funkcji

dodajWolne:
	addi $t9, $t9, 1	# Zwiększ licznik wolnych pól
	j return_val		# Powrót z funkcji

pktX:
	li $t3, 1		# Ustaw stan rundy na 1 (X wygrywa)
	j return_val		# Powrót z funkcji

pktO:
	li $t3, 2		# Ustaw stan rundy na 2 (O wygrywa)
	j return_val		# Powrót z funkcji

ustawRemis:
	li $t3, 3		# Ustaw stan rundy na 3 (remis)
	j return_val		# Powrót z funkcji

sprawdzRemis_link:
	beq $t0, 9, ustawRemis	# Jeśli 9 pól jest zajętych, ustaw remis
	beq $t1, 9, return_val	# Jeśli sprawdzono 9 pól, wróć
	lb $t2, 0($t5)		# Wczytaj znak z bieżącego pola planszy
	addi $t5, $t5, 1	# Przesuń wskaźnik na następne pole
	addi $t1, $t1, 1	# Zwiększ licznik sprawdzonych pól
	beq $t2, 'X', dolicz	# Jeśli pole to 'X', dolicz je
	beq $t2, 'O', dolicz	# Jeśli pole to 'O', dolicz je
	j sprawdzRemis_link	# Sprawdzaj następne pole

dolicz:
	addi $t0, $t0, 1	# Zwiększ licznik zajętych pól
	j sprawdzRemis_link	# Wróć do pętli sprawdzającej
	# Gra
	rundaGracz_link:
		beq $t3, 1, punktX	# Jeśli stan rundy=1 (X wygrał), skocz do punktX
		beq $t3, 2, punktO	# Jeśli stan rundy=2 (O wygrał), skocz do punktO
		beq $t3, 3, remis	# Jeśli stan rundy=3 (remis), skocz do remis
		
		subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
		jal wyswietlPlansze_link # Wywołanie funkcji wyświetlającej planszę
	
	bgezal $t4, TG_ruchGracza # Jeśli tura X ($t4 >= 0), wykonaj ruch gracza (błędna logika)
		bltzal $t4, TG_ruchKomputera # Jeśli tura O ($t4 < 0), wykonaj ruch komputera (błędna logika)
		mul $t4, $t4, -1	# Zmień turę (pomnóż przez -1)
		
		jal sprawdzStanPlanszy_link # Sprawdź stan planszy po ruchu
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
		j rundaGracz_link	# Skok do następnej tury w rundzie
	rundaKomputer_link:
		beq $t3, 1, punktX	# Jeśli stan rundy=1 (X wygrał), skocz do punktX
		beq $t3, 2, punktO	# Jeśli stan rundy=2 (O wygrał), skocz do punktO
		beq $t3, 3, remis	# Jeśli stan rundy=3 (remis), skocz do remis
		
		subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
		jal wyswietlPlansze_link # Wywołanie funkcji wyświetlającej planszę
	jal TK_ruch		# Wykonaj ruch komputera
		mul $t4, $t4, -1	# Zmień turę
		
		jal sprawdzStanPlanszy_link # Sprawdź stan planszy po ruchu
		li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
		la $a0, next_move_prompt # Wczytanie adresu prośby o naciśnięcie ENTER
		syscall			# Wywołanie systemowe
		li $v0, 8		# Wczytanie kodu syscall 8 (wczytanie tekstu) do pauzy
		syscall			# Wywołanie systemowe
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
		j rundaKomputer_link	# Skok do następnej tury w rundzie

TG_ruchGracza:
	li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
	li $s6, 1		# Wczytanie 1 do $s6 w celu porównania
	beq $s7, $s6, player_prompt_x # Jeśli gracz to X ($s7=1), pokaż monit dla X
	beq $s7, $zero, player_prompt_o # Jeśli gracz to O ($s7=0), pokaż monit dla O
	
	carry_on_ruch_gracza:
		la $a0, inputIndicator	# Wczytanie adresu wskaźnika
		syscall			# Wywołanie systemowe
		li $v0, 5		# Wczytanie kodu syscall 5 (wczytanie liczby)
		syscall			# Wywołanie systemowe
		move $t6, $v0		# Przeniesienie wczytanej liczby do $t6
		subi $t6, $t6, 1	# Zmniejszenie liczby o 1, aby uzyskać indeks (0-8)
		subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
		sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
		jal zaznaczPole		# Wywołanie funkcji zaznaczającej pole
		lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
		addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
		j return_val		# Powrót z funkcji

player_prompt_x:
	la $a0, gamer_x_move_txt # Wczytanie adresu monitu dla gracza X
	syscall			# Wywołanie systemowe
	j carry_on_ruch_gracza	# Kontynuuj, aby wczytać ruch gracza

player_prompt_o:
	la $a0, gamer_o_move_txt # Wczytanie adresu monitu dla gracza O
	syscall			# Wywołanie systemowe
	j carry_on_ruch_gracza	# Kontynuuj, aby wczytać ruch gracza

TG_ruchKomputera: # strategia: jesli mozesz wygrac, zrob to -> jesli gracz moze wygrac, zablokuj -> zajmij srodek -> zajmij rogi -> zajmij boczne pole
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	jal wyznaczOptymalnePole# Wywołaj AI, aby znalazło najlepszy ruch (w $t6)
	jal zaznaczPole		# Zaznacz pole wybrane przez AI
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
	la $a0, comp_move_prompt # Wczytanie adresu komunikatu o ruchu komputera
	syscall			# Wywołanie systemowe
	li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
	lb $a0, newLine		# Wczytanie znaku nowej linii
	syscall			# Wywołanie systemowe
	j return_val		# Powrót z funkcji

TK_ruch:
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	jal wyznaczOptymalnePole# Wywołaj AI, aby znalazło najlepszy ruch
	jal zaznaczPole		# Zaznacz pole wybrane przez AI
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji

wyznaczOptymalnePole:
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	subi $t6, $zero, 1	# Inicjalizacja $t6 na -1 (brak znalezionego ruchu)
	
	bltzal $t6, sprobujWygrac # Jeśli nie znaleziono ruchu, spróbuj wygrać
	bltzal $t6, sprobujZablokowac # Jeśli nie, spróbuj zablokować przeciwnika
	bltzal $t6, sprobujZajacSrodek # Jeśli nie, spróbuj zająć środek
	bltzal $t6, sprobujZajacRogi # Jeśli nie, spróbuj zająć róg
	bltzal $t6, zajmijLosoweMiejsce # Jeśli nie, zajmij dowolne wolne miejsce
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji

sprobujWygrac:
	la $t5, plansza		# Wczytanie adresu planszy
	
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	
	# Rzad 1
	lb $t0,0($t5)		# Wczytanie pola 0
	lb $t1,1($t5)		# Wczytanie pola 1
	lb $t2,2($t5)		# Wczytanie pola 2
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszWygrac # Sprawdź, czy można wygrać w tej linii
	
	# Rzad 2
	lb $t0,3($t5)		# Wczytanie pola 3
	lb $t1,4($t5)		# Wczytanie pola 4
	lb $t2,5($t5)		# Wczytanie pola 5
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszWygrac # Sprawdź, czy można wygrać w tej linii
	
	# Rzad 3
	lb $t0,6($t5)		# Wczytanie pola 6
	lb $t1,7($t5)		# Wczytanie pola 7
	lb $t2,8($t5)		# Wczytanie pola 8
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszWygrac # Sprawdź, czy można wygrać w tej linii
	
	# Kolumna 1
	lb $t0,0($t5)		# Wczytanie pola 0
	lb $t1,3($t5)		# Wczytanie pola 3
	lb $t2,6($t5)		# Wczytanie pola 6
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszWygrac # Sprawdź, czy można wygrać w tej linii
	
	# Kolumna 2
	lb $t0,1($t5)		# Wczytanie pola 1
	lb $t1,4($t5)		# Wczytanie pola 4
	lb $t2,7($t5)		# Wczytanie pola 7
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszWygrac # Sprawdź, czy można wygrać w tej linii
	
	# Kolumna 3
	lb $t0,2($t5)		# Wczytanie pola 2
	lb $t1,5($t5)		# Wczytanie pola 5
	lb $t2,8($t5)		# Wczytanie pola 8
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszWygrac # Sprawdź, czy można wygrać w tej linii
	
	# Przekatna 1
	lb $t0,0($t5)		# Wczytanie pola 0
	lb $t1,4($t5)		# Wczytanie pola 4
	lb $t2,8($t5)		# Wczytanie pola 8
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszWygrac # Sprawdź, czy można wygrać w tej linii
	
	# Przekatna 2
	lb $t0,2($t5)		# Wczytanie pola 2
	lb $t1,4($t5)		# Wczytanie pola 4
	lb $t2,6($t5)		# Wczytanie pola 6
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszWygrac # Sprawdź, czy można wygrać w tej linii
	
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji

zaznaczPole:
	bltz $t6, blednyRuch	# Jeśli indeks < 0, to błędny ruch
	bge $t6, 9, blednyRuch	# Jeśli indeks >= 9, to błędny ruch
	lb $t7, plansza($t6)	# Wczytaj znak z wybranego pola
	beq $t7, 'X', blednyRuch	# Jeśli pole jest już zajęte przez 'X', to błędny ruch
	beq $t7, 'O', blednyRuch	# Jeśli pole jest już zajęte przez 'O', to błędny ruch
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie

	bgezal  $t4, markPlayer 		# Jeśli tura gracza, pobierz jego znak
	bltzal  $t4, markComputer		# Jeśli tura komputera, pobierz jego znak
	sb $a0, plansza($t6)	# Zapisz znak ($a0) na planszy w wybranym miejscu ($t6)
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji

blednyRuch:
	li $v0, 4		# Wczytanie kodu syscall 4 (wypisanie tekstu)
	la $a0, bad_move_prompt	# Wczytanie adresu komunikatu o błędnym ruchu
	syscall			# Wywołanie systemowe
	li $v0, 11		# Wczytanie kodu syscall 11 (wypisanie znaku)
	lb $a0, newLine		# Wczytanie znaku nowej linii
	syscall			# Wywołanie systemowe
	
	j TG_ruchGracza		# Wróć do ruchu gracza, aby mógł spróbować ponownie

markPlayer:
	li $s6, 1		# Wczytaj 1 do $s6 do porównania
	beq $s7, $s6, markX					# Jeśli gracz to X ($s7=1), skocz do markX
	beq $s7, $zero, markO				# Jeśli gracz to O ($s7=0), skocz do markO

markComputer:
	li $s6, 1		# Wczytaj 1 do $s6 do porównania
	beq $s7, $s6, markO					# Jeśli gracz to X ($s7=1), komputer jest O
	beq $s7, $zero, markX				# Jeśli gracz to O ($s7=0), komputer jest X

markX:
	lb $a0, X		# Wczytaj znak 'X' do $a0
	j return_val		# Powrót z funkcji

markO:
	lb $a0, O		# Wczytaj znak 'O' do $a0
	j return_val		# Powrót z funkcji

sprawdzCzyMozeszWygrac:
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	move $s4, $zero		# Wyzeruj flagę/licznik $s4
	bgezal $t4, sprawdzCzyDwaX # Jeśli AI jest X, sprawdź czy są dwa 'X'
	bltzal $t4, sprawdzCzyDwaO # Jeśli AI jest O, sprawdź czy są dwa 'O'
	jal sprawdzCzyJednoWolne # Sprawdź czy jest jedno wolne pole
	beq $s4, 2, toTutaj	# Jeśli oba warunki spełnione ($s4=2), to jest to miejsce
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji
znalezionoPole:
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji
sprawdzCzyDwaX:
	beq $t7, 2, incrementS4	# Jeśli licznik 'X' ($t7) wynosi 2, zwiększ flagę $s4
	j return_val		# Powrót z funkcji
sprawdzCzyDwaO:
	beq $t8, 2, incrementS4	# Jeśli licznik 'O' ($t8) wynosi 2, zwiększ flagę $s4
	j return_val		# Powrót z funkcji
sprawdzCzyJednoWolne:
	beq $t9, 1, incrementS4	# Jeśli licznik wolnych pól ($t9) wynosi 1, zwiększ flagę $s4
	j return_val		# Powrót z funkcji
toTutaj:
	move $s4, $t0		# Przenieś pierwszy znak z linii do $s4
	blt $s4, 'A', setT6toS4	# Jeśli znak to cyfra (wolne pole), ustaw je jako ruch
	move $s4, $t1		# Przenieś drugi znak z linii do $s4
	blt $s4, 'A', setT6toS4	# Jeśli znak to cyfra, ustaw je jako ruch
	move $s4, $t2		# Przenieś trzeci znak z linii do $s4
	j setT6toS4		# Ustaw ten znak jako ruch (musi być wolnym polem)
incrementS4:
	addi $s4, $s4, 1	# Zwiększ flagę/licznik $s4 o 1
	j return_val		# Powrót z funkcji
setT6toS4:
	subi $t6, $s4, '0'	# Zamień znak cyfry na jej wartość liczbową
	subi $t6, $t6, 1	# Zmień numer pola (1-9) na indeks (0-8)
	j return_val		# Powrót z funkcji

sprobujZablokowac:
	la $t5, plansza		# Wczytanie adresu planszy
	
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	
	# Rzad 1
	lb $t0,0($t5)		# Wczytanie pola 0
	lb $t1,1($t5)		# Wczytanie pola 1
	lb $t2,2($t5)		# Wczytanie pola 2
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszZablokowac # Sprawdź czy można zablokować w tej linii
	
	# Rzad 2
	lb $t0,3($t5)		# Wczytanie pola 3
	lb $t1,4($t5)		# Wczytanie pola 4
	lb $t2,5($t5)		# Wczytanie pola 5
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszZablokowac # Sprawdź czy można zablokować w tej linii
	
	# Rzad 3
	lb $t0,6($t5)		# Wczytanie pola 6
	lb $t1,7($t5)		# Wczytanie pola 7
	lb $t2,8($t5)		# Wczytanie pola 8
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszZablokowac # Sprawdź czy można zablokować w tej linii
	
	# Kolumna 1
	lb $t0,0($t5)		# Wczytanie pola 0
	lb $t1,3($t5)		# Wczytanie pola 3
	lb $t2,6($t5)		# Wczytanie pola 6
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszZablokowac # Sprawdź czy można zablokować w tej linii
	
	# Kolumna 2
	lb $t0,1($t5)		# Wczytanie pola 1
	lb $t1,4($t5)		# Wczytanie pola 4
	lb $t2,7($t5)		# Wczytanie pola 7
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszZablokowac # Sprawdź czy można zablokować w tej linii
	
	# Kolumna 3
	lb $t0,2($t5)		# Wczytanie pola 2
	lb $t1,5($t5)		# Wczytanie pola 5
	lb $t2,8($t5)		# Wczytanie pola 8
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszZablokowac # Sprawdź czy można zablokować w tej linii
	
	# Przekatna 1
	lb $t0,0($t5)		# Wczytanie pola 0
	lb $t1,4($t5)		# Wczytanie pola 4
	lb $t2,8($t5)		# Wczytanie pola 8
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszZablokowac # Sprawdź czy można zablokować w tej linii
	
	# Przekatna 2
	lb $t0,2($t5)		# Wczytanie pola 2
	lb $t1,4($t5)		# Wczytanie pola 4
	lb $t2,6($t5)		# Wczytanie pola 6
	jal podliczLinie		# Zlicz znaki w linii
	jal sprawdzCzyMozeszZablokowac # Sprawdź czy można zablokować w tej linii
	
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji
sprawdzCzyMozeszZablokowac:
	subi $sp, $sp, 4	# Przesunięcie wskaźnika stosu
	sw $ra, 0($sp)		# Zapisanie adresu powrotu na stosie
	move $s4, $zero		# Wyzeruj flagę/licznik $s4
	bgezal $t4, sprawdzCzyDwaO # Jeśli AI jest X, sprawdź czy przeciwnik ma dwa 'O'
	bltzal $t4, sprawdzCzyDwaX # Jeśli AI jest O, sprawdź czy przeciwnik ma dwa 'X'
	jal sprawdzCzyJednoWolne # Sprawdź czy jest jedno wolne pole
	beq $s4, 2, toTutaj	# Jeśli oba warunki spełnione, to jest to miejsce do blokady
	lw $ra, 0($sp)		# Przywrócenie adresu powrotu ze stosu
	addi $sp, $sp, 4	# Przywrócenie wskaźnika stosu
	j return_val		# Powrót z funkcji
sprobujZajacSrodek:
	li $s5, 4		# Wczytaj indeks środka (4) do $s5
	lb $s4, plansza($s5)	# Wczytaj znak ze środkowego pola
	blt $s4, 'A', setT6toS4	# Jeśli pole jest wolne (cyfra), ustaw je jako ruch
	j return_val		# Powrót z funkcji
sprobujZajacRogi:
	li $s5, 0		# Wczytaj indeks rogu (0)
	lb $s4, plansza($s5)	# Wczytaj znak z rogu
	blt $s4, 'A', setT6toS4	# Jeśli róg jest wolny, ustaw go jako ruch
	li $s5, 2		# Wczytaj indeks rogu (2)
	lb $s4, plansza($s5)	# Wczytaj znak z rogu
	blt $s4, 'A', setT6toS4	# Jeśli róg jest wolny, ustaw go jako ruch
	li $s5, 6		# Wczytaj indeks rogu (6)
	lb $s4, plansza($s5)	# Wczytaj znak z rogu
	blt $s4, 'A', setT6toS4	# Jeśli róg jest wolny, ustaw go jako ruch
	li $s5, 8		# Wczytaj indeks rogu (8)
	lb $s4, plansza($s5)	# Wczytaj znak z rogu
	blt $s4, 'A', setT6toS4	# Jeśli róg jest wolny, ustaw go jako ruch
	j return_val		# Powrót z funkcji
zajmijLosoweMiejsce:
	la $t5, plansza		# Wczytanie adresu planszy
petlaZajmijLosoweMiejsce:
	lb $s4, 0($t5)		# Wczytaj znak z bieżącego pola
	blt $s4, 'A', setT6toS4	# Jeśli pole jest wolne (cyfra), ustaw je jako ruch
	addi $t5, $t5, 1	# Przejdź do następnego pola
	j petlaZajmijLosoweMiejsce # Kontynuuj pętlę