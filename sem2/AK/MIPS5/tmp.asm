# WYKAZ UZYWANYCH REJESTROW

# $a0 - argument przy zaznaczaniu pola
# $a1 - 
# $a2 - 
# $a3 - 

# $t0 - resetPlanszy(iterator petli) | wyswietlanie planszy iterator dla rzedow | sprawdzanie wyniku pole1
# $t1 - resetPlanszy(container na byte) | wyswietlanie planszy iterator w rzedzie | sprawdzanie wyniku pole2
# $t2 - wyswietlanie planszy index pola | sprawdzanie wyniku pole3
# $t3 - wynik danej rundy
# $t4 - 1/-1 czyja kolej aktulnie 1: X | -1: O || 1 - gracz | -1 - komputer
# $t5 - przy sprawdzaniu tymczasowo przechowuje plansze
# $t6 - przechowuje pole do oznaczenia znakiem X/O
# $t7 - analiza linii (podlicza X)
# $t8 - analiza linii (podlicza O)
# $t9 - analiza linii (podlicza wolne)

# $s0 - liczba rund
# $s1 - wynik gracza X
# $s2 - wynik gracza O
# $s3 - nr rundy | wynik gry na sam koniec
# $s4 - 
# $s5 - 
# $s6 - 
# $s7 - Gracz gra o => 0 gracz gra X => 1

.data
X: 					.byte 'X'
O: 					.byte 'O'
wall: 				.byte '|'
space: 				.byte ' '
newLine: 			.byte '\n'
plansza: 			.space 9

floor: 				.asciiz "-----------"
inputIndicator: 	.asciiz ": "
rounds_num_prompt: 	.asciiz "\nWpisz ile rund chcesz rozegrac"
err_input_prompt: 	.asciiz "Wybrano niepoprawna opcje. Sprobuj ponownie!\n"
round: 				.asciiz "RUNDA NR "
round_win_prompt: 	.asciiz "Runde wygrywa "
score_prompt: 		.asciiz "Aktualny wynik"
gameover_prompt: 	.asciiz "KONIEC GRY! WYGRYWA "
draw_prompt: 		.asciiz "Remis! Obaj gracze otrzymuja punkt"
bad_move_prompt: 	.asciiz "\nBledny ruch! Wybierz inne pole"
new_game_prompt: 	.asciiz "Czy chcesz zaczac gre od nowa? (0 - TAK, 1 - NIE)\nWybor"
gameover2_prompt: 	.asciiz "KONIEC GRY! PARTIA ZAKONCZONA REMISEM"
comp_move_prompt: 	.asciiz "\nKomputer wykonal ruch!\n"
next_move_prompt: 	.asciiz "Nacisnij ENTER, aby zobaczyc nastepny ruch"
znakPrompt: 		.asciiz "Wybierz swoj znak (X lub O): "
gamer_x_move_txt: 	.asciiz "\nTwoj ruch! Postaw X w wybranym miejscu wpisujac numer dostepnego pola"
gamer_o_move_txt: 	.asciiz "\nTwoj ruch! Postaw O w wybranym miejscu wpisujac numer dostepnego pola"
char_err_txt:	  	.asciiz "Podaj poprawny znak [X lub O]\n"

# prompt3: .asciiz "Twoj ruch! Postaw X w wybranym miejscu wpisujac numer dostepnego pola"
# Inne
#domyslnaPlansza: .asciiz "123456789"
.text
# Ogolne
main:
    move $s1, $zero       # Wynik gracza X
    move $s2, $zero       # Wynik gracza O
    move $s3, $zero       # Licznik rund

    j wybierzZnak         # Dodany krok: wybór znaku gracza
	
return_val:
		jr $ra
		
	exit:
		li $v0, 10
		syscall
		
err_input_prompt_link:
		li $v0, 4
		la $a0, err_input_prompt
		syscall
		j return_val
		
	# Plansza
	wyswietlPlansze_link:
		move $t0, $zero
		
		subi $sp, $sp, 4
	sw $ra, 0($sp)
	jal petlaWyswietlPlansze_link
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	
		j return_val
	petlaWyswietlPlansze_link:
		move $t1, $zero
		
		li $v0, 11
		lb $a0, space
		syscall
		
		subi $sp, $sp, 4
	sw $ra, 0($sp)
	jal petlaWyswietlPlanszeRzad_link
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	
		addi $t0, $t0, 1
		
		li $v0, 11
		lb $a0, newLine
		syscall
		
		beq $t0, 3, return_val
		
		li $v0, 4
		la $a0, floor
		syscall
		li $v0, 11
		lb $a0, newLine
		syscall
		j petlaWyswietlPlansze_link
	
	petlaWyswietlPlanszeRzad_link:
		mul $t2, $t0, 3
		add $t2, $t2, $t1
		li $v0, 11
		lb $a0, plansza($t2)
		syscall
		
		addi $t1, $t1, 1
		beq $t1, 3, return_val
		lb $a0, space
		syscall
		lb $a0, wall
		syscall
		lb $a0, space
		syscall
		j petlaWyswietlPlanszeRzad_link

resetPlansza_link:
	addi $t0, $zero, 1
	la $t1, plansza
	
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	jal petlaResetPlansza_link
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	
	j return_val
	
petlaResetPlansza_link:
	bgt $t0, 10, return_val
	addi $t2, $t0, 48
	sb $t2, 0($t1)
	addi $t1, $t1, 1
	addi $t0, $t0, 1
	j petlaResetPlansza_link

#! ----- Uzytkownik wybiera znak -------
wybierzZnak:
    li $v0, 4					# Wyświetlenie komunikatu o wyborze znaku
    la $a0, znakPrompt
    syscall

    li $v0, 12       			# Wczytanie znaku
    syscall
    move $t6, $v0    			# Przeniesienie znaku z $v0 do $t6

    li $t7, 'X'					# Sprawdzenie czy wprowadzono X
    beq $t6, $t7, graczJestX

    li $t7, 'O'					# Sprawdzenie czy wprowadzono O
    beq $t6, $t7, graczJestO

    li $v0, 4					# Jezeli wprowadzono nie poprawny znak ponow probe
    la $a0, char_err_txt
    syscall
    j wybierzZnak

graczJestX:
    li $t4, 1     # Gracz gra jako X
	li $s7, 1
    j liczbaRund

graczJestO:
    li $t4, -1    # Gracz gra jako O
	li $s7, 0
    j liczbaRund

# Organizacja gry
liczbaRund:
	li $v0, 4
		la $a0, rounds_num_prompt
		syscall
		la $a0, inputIndicator
		syscall
		li $v0, 5
		syscall
		move $s0, $v0
		bgt $s0, 0, trybGry
		jal err_input_prompt_link
		j liczbaRund
		
trybGry:
		j trybGracz
		
	trybGracz:
		bge $s3, $s0, wyniki
		addi $s3, $s3, 1
		
		jal resetPlansza_link
		
		li $v0, 4
		la $a0, round
		syscall
		li $v0, 1
		move $a0, $s3
		syscall
		li $v0, 11
		lb $a0, newLine
		syscall
		
		move $t3, $zero
		li $t4, 1
		jal rundaGracz_link
		
		j trybGracz
		
	punktX:
		subi $sp, $sp, 4
	sw $ra, 0($sp)
	jal wyswietlPlansze_link
		addi $s1, $s1, 1
		
		li $v0, 4
		la $a0, round_win_prompt
		syscall
		li $v0, 11
		lb $a0, X
		syscall
		lb $a0, newLine
		syscall
		
	jal aktualnyWynik_link
	lw $ra, 0($sp)
	addi $sp, $sp, 4
		
		j return_val
	punktO:
		subi $sp, $sp, 4
	sw $ra, 0($sp)
	jal wyswietlPlansze_link
		addi $s2, $s2, 1
		
		li $v0, 4
		la $a0, round_win_prompt
		syscall
		li $v0, 11
		lb $a0, O
		syscall
		lb $a0, newLine
		syscall
		
	jal aktualnyWynik_link
	lw $ra, 0($sp)
	addi $sp, $sp, 4
		
		j return_val
	remis:
		subi $sp, $sp, 4
	sw $ra, 0($sp)
	jal wyswietlPlansze_link
		addi $s1, $s1, 1
		addi $s2, $s2, 1
		
		li $v0, 4
		la $a0, draw_prompt
		syscall
		li $v0, 11
		lb $a0, newLine
		syscall
		
	jal aktualnyWynik_link
	lw $ra, 0($sp)
	addi $sp, $sp, 4
		
		j return_val
		
	aktualnyWynik_link:
		li $v0, 4
		la $a0, score_prompt
		syscall
		la $a0, inputIndicator
		syscall
		li $v0, 11
		lb $a0, newLine
		syscall
		lb $a0, X
		syscall
		li $v0, 4
		la $a0, inputIndicator
		syscall
		li $v0, 1
		move $a0, $s1
		syscall
		li $v0, 11
		lb $a0, newLine
		syscall
		lb $a0, O
		syscall
		li $v0, 4
		la $a0, inputIndicator
		syscall
		li $v0, 1
		move $a0, $s2
		syscall
		li $v0, 11
		lb $a0, newLine
		syscall
		j return_val
	
	wyniki:
		sub $s3, $s1, $s2
		beqz $s3, wynikRemis
		li $v0, 4
		la $a0, gameover_prompt
		syscall
		li $v0, 11
		bgezal $s3, markPlayer
		bltzal $s3, markComputer
		syscall
		lb $a0, newLine
		syscall
	
	newGame:
		li $v0, 4
		la $a0, new_game_prompt
		syscall
		la $a0, inputIndicator
		syscall
		li $v0, 5
		syscall
		beq $v0, 1, main
		j exit
	
	wynikRemis:
		li $v0, 4
		la $a0, gameover2_prompt
		syscall
		li $v0, 11
		lb $a0, newLine
		syscall
		j newGame

sprawdzStanPlanszy_link:
	la $t5, plansza
	
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	
	# Rzad 1
	lb $t0,0($t5)
	lb $t1,1($t5)
	lb $t2,2($t5)
	jal sprawdzLinie_link
	
	# Rzad 2
	lb $t0,3($t5)
	lb $t1,4($t5)
	lb $t2,5($t5)
	jal sprawdzLinie_link
	
	# Rzad 3
	lb $t0,6($t5)
	lb $t1,7($t5)
	lb $t2,8($t5)
	jal sprawdzLinie_link
	
	# Kolumna 1
	lb $t0,0($t5)
	lb $t1,3($t5)
	lb $t2,6($t5)
	jal sprawdzLinie_link
	
	# Kolumna 2
	lb $t0,1($t5)
	lb $t1,4($t5)
	lb $t2,7($t5)
	jal sprawdzLinie_link
	
	# Kolumna 3
	lb $t0,2($t5)
	lb $t1,5($t5)
	lb $t2,8($t5)
	jal sprawdzLinie_link
	
	# Przekatna 1
	lb $t0,0($t5)
	lb $t1,4($t5)
	lb $t2,8($t5)
	jal sprawdzLinie_link
	
	# Przekatna 2
	lb $t0,2($t5)
	lb $t1,4($t5)
	lb $t2,6($t5)
	jal sprawdzLinie_link
	
	# Remis
	move $t0, $zero
	move $t1, $zero
	jal sprawdzRemis_link
	
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val

sprawdzLinie_link:
	beq $t0, $t1, sprawdzDrugie
	j return_val

sprawdzDrugie:
	beq $t0, $t2, sprawdzZnak
	j return_val

sprawdzZnak:
	beq $t0, 'X', pktX
	beq $t0, 'O', pktO
	j return_val

podliczLinie:
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	
	move $t7, $zero
	move $t8, $zero
	move $t9, $zero
	move $s4, $t0
	jal zliczaj
	move $s4, $t1
	jal zliczaj
	move $s4, $t2
	jal zliczaj
	
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val

zliczaj:
	beq $s4, 'X', dodajX
	beq $s4, 'O', dodajO
	j dodajWolne

dodajX:
	addi $t7, $t7, 1
	j return_val

dodajO:
	addi $t8, $t8, 1
	j return_val

dodajWolne:
	addi $t9, $t9, 1
	j return_val

pktX:
	li $t3, 1
	j return_val

pktO:
	li $t3, 2
	j return_val

ustawRemis:
	li $t3, 3
	j return_val

sprawdzRemis_link:
	beq $t0, 9, ustawRemis
	beq $t1, 9, return_val
	lb $t2, 0($t5)
	addi $t5, $t5, 1
	addi $t1, $t1, 1
	beq $t2, 'X', dolicz
	beq $t2, 'O', dolicz
	j sprawdzRemis_link

dolicz:
	addi $t0, $t0, 1
	j sprawdzRemis_link
	# Gra
	rundaGracz_link:
		beq $t3, 1, punktX
		beq $t3, 2, punktO
		beq $t3, 3, remis
		
		subi $sp, $sp, 4
	sw $ra, 0($sp)
		jal wyswietlPlansze_link
	
	bgezal $t4, TG_ruchGracza
		bltzal $t4, TG_ruchKomputera
		mul $t4, $t4, -1
		
		jal sprawdzStanPlanszy_link
	lw $ra, 0($sp)
	addi $sp, $sp, 4
		j rundaGracz_link
	rundaKomputer_link:
		beq $t3, 1, punktX
		beq $t3, 2, punktO
		beq $t3, 3, remis
		
		subi $sp, $sp, 4
	sw $ra, 0($sp)
		jal wyswietlPlansze_link
	jal TK_ruch
		mul $t4, $t4, -1
		
		jal sprawdzStanPlanszy_link
		li $v0, 4
		la $a0, next_move_prompt
		syscall
		li $v0, 8
		syscall
	lw $ra, 0($sp)
	addi $sp, $sp, 4
		j rundaKomputer_link

TG_ruchGracza:
	li $v0, 4
	# la $a0, prompt3
	li $s6, 1
	beq $s7, $s6, player_prompt_x
	beq $s7, $zero, player_prompt_o
	
	carry_on_ruch_gracza:
		la $a0, inputIndicator
		syscall
		li $v0, 5
		syscall
		move $t6, $v0
		subi $t6, $t6, 1
		subi $sp, $sp, 4
		sw $ra, 0($sp)
		jal zaznaczPole
		lw $ra, 0($sp)
		addi $sp, $sp, 4
		j return_val

player_prompt_x:
	la $a0, gamer_x_move_txt
	syscall
	j carry_on_ruch_gracza

player_prompt_o:
	la $a0, gamer_o_move_txt
	syscall
	j carry_on_ruch_gracza

TG_ruchKomputera: # strategia: jesli mozesz wygrac, zrob to -> jesli gracz moze wygrac, zablokuj -> zajmij srodek -> zajmij rogi -> zajmij boczne pole
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	jal wyznaczOptymalnePole# wyznaczy nr pola 0-8 w $t6
	jal zaznaczPole# zaznaczy w wyznaczonym polu znak zgodnie z wartoscia $t4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	li $v0, 4
	la $a0, comp_move_prompt
	syscall
	li $v0, 11
	lb $a0, newLine
	syscall
	j return_val

TK_ruch:
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	jal wyznaczOptymalnePole# wyznaczy nr pola 0-8 w $t6
	jal zaznaczPole# zaznaczy w wyznaczonym polu znak zgodnie z wartoscia $t4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val

wyznaczOptymalnePole:
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	#bgezal  $t4, markPlayer
	#bltzal  $t4, markComputer# w $a0 jest aktualny znak komputera
	subi $t6, $zero, 1 # ustawia $t6 na -1 jako poczatkowa wartosc
	
	bltzal $t6, sprobujWygrac
	bltzal $t6, sprobujZablokowac
	bltzal $t6, sprobujZajacSrodek
	bltzal $t6, sprobujZajacRogi
	bltzal $t6, zajmijLosoweMiejsce
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val

sprobujWygrac:
	la $t5, plansza
	
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	
	# Rzad 1
	lb $t0,0($t5)
	lb $t1,1($t5)
	lb $t2,2($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszWygrac
	# Rzad 2
	lb $t0,3($t5)
	lb $t1,4($t5)
	lb $t2,5($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszWygrac
	# Rzad 3
	lb $t0,6($t5)
	lb $t1,7($t5)
	lb $t2,8($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszWygrac
	# Kolumna 1
	lb $t0,0($t5)
	lb $t1,3($t5)
	lb $t2,6($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszWygrac
	# Kolumna 2
	lb $t0,1($t5)
	lb $t1,4($t5)
	lb $t2,7($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszWygrac
	# Kolumna 3
	lb $t0,2($t5)
	lb $t1,5($t5)
	lb $t2,8($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszWygrac
	# Przekatna 1
	lb $t0,0($t5)
	lb $t1,4($t5)
	lb $t2,8($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszWygrac
	# Przekatna 2
	lb $t0,2($t5)
	lb $t1,4($t5)
	lb $t2,6($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszWygrac
	
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val

zaznaczPole:
	bltz $t6, blednyRuch
	bge $t6, 9, blednyRuch
	lb $t7, plansza($t6)
	beq $t7, 'X', blednyRuch
	beq $t7, 'O', blednyRuch
	subi $sp, $sp, 4
	sw $ra, 0($sp)

	bgezal  $t4, markPlayer 		# Zaznacz pole wybrane przez gracza
	bltzal  $t4, markComputer		# Zaznacz pole wybrane przez komputer
	sb $a0, plansza($t6)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val

blednyRuch:
	li $v0, 4
	la $a0, bad_move_prompt
	syscall
	li $v0, 11
	lb $a0, newLine
	syscall
	
	j TG_ruchGracza

markPlayer:
	li $s6, 1
	beq $s7, $s6, markX					# Sprawdzenie czy gracz gra X
	beq $s7, $zero, markO				# Sprawdzenie czy gracz gra O

markComputer:
	li $s6, 1
	beq $s7, $s6, markO					# Sprawdzenie czy komputer gra O
	beq $s7, $zero, markX				# Sprawdzenie czy komputer gra X

markX:
	lb $a0, X
	j return_val

markO:
	lb $a0, O
	j return_val

sprawdzCzyMozeszWygrac:
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	move $s4, $zero
	bgezal $t4, sprawdzCzyDwaX
	bltzal $t4, sprawdzCzyDwaO
	jal sprawdzCzyJednoWolne
	beq $s4, 2, toTutaj
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val
znalezionoPole:
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val
sprawdzCzyDwaX:
	beq $t7, 2, incrementS4
	j return_val
sprawdzCzyDwaO:
	beq $t8, 2, incrementS4
	j return_val
sprawdzCzyJednoWolne:
	beq $t9, 1, incrementS4
	j return_val
toTutaj:
	move $s4, $t0
	blt $s4, 'A', setT6toS4
	move $s4, $t1
	blt $s4, 'A', setT6toS4
	move $s4, $t2
	j setT6toS4
incrementS4:
	addi $s4, $s4, 1
	j return_val
setT6toS4:
	subi $t6, $s4, '0'
	subi $t6, $t6, 1
	j return_val

sprobujZablokowac:
	la $t5, plansza
	
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	
	# Rzad 1
	lb $t0,0($t5)
	lb $t1,1($t5)
	lb $t2,2($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszZablokowac
	
	# Rzad 2
	lb $t0,3($t5)
	lb $t1,4($t5)
	lb $t2,5($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszZablokowac
	
	# Rzad 3
	lb $t0,6($t5)
	lb $t1,7($t5)
	lb $t2,8($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszZablokowac
	
	# Kolumna 1
	lb $t0,0($t5)
	lb $t1,3($t5)
	lb $t2,6($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszZablokowac
	
	# Kolumna 2
	lb $t0,1($t5)
	lb $t1,4($t5)
	lb $t2,7($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszZablokowac
	
	# Kolumna 3
	lb $t0,2($t5)
	lb $t1,5($t5)
	lb $t2,8($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszZablokowac
	
	# Przekatna 1
	lb $t0,0($t5)
	lb $t1,4($t5)
	lb $t2,8($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszZablokowac
	
	# Przekatna 2
	lb $t0,2($t5)
	lb $t1,4($t5)
	lb $t2,6($t5)
	jal podliczLinie
	jal sprawdzCzyMozeszZablokowac
	
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val
sprawdzCzyMozeszZablokowac:
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	move $s4, $zero
	bgezal $t4, sprawdzCzyDwaO
	bltzal $t4, sprawdzCzyDwaX
	jal sprawdzCzyJednoWolne
	beq $s4, 2, toTutaj
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	j return_val
sprobujZajacSrodek:
	li $s5, 4
	lb $s4, plansza($s5)
	blt $s4, 'A', setT6toS4
	j return_val
sprobujZajacRogi:
	li $s5, 0
	lb $s4, plansza($s5)
	blt $s4, 'A', setT6toS4
	li $s5, 2
	lb $s4, plansza($s5)
	blt $s4, 'A', setT6toS4
	li $s5, 6
	lb $s4, plansza($s5)
	blt $s4, 'A', setT6toS4
	li $s5, 8
	lb $s4, plansza($s5)
	blt $s4, 'A', setT6toS4
	j return_val
zajmijLosoweMiejsce:
	la $t5, plansza
petlaZajmijLosoweMiejsce:
	lb $s4, 0($t5)
	blt $s4, 'A', setT6toS4
	addi $t5, $t5, 1
	j petlaZajmijLosoweMiejsce