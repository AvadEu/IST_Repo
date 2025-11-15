.data
prompt_op:      .asciiz "Wybierz operacje (S - szyfrowanie, D - deszyfrowanie): "
prompt_key:     .asciiz "Podaj klucz permutacji (3-8 cyfr, bez powtorzen, cyfry 1-8): "
prompt_text:    .asciiz "Podaj tekst jawny (max 50 znakow, wielkie litery, bez spacji): "
prompt_ciph:    .asciiz "Podaj szyfrogram (max 50 znakow, wielkie litery): "
err_length:     .asciiz "Tekst za dlugi! Wprowadz ponownie.\n"
err_key_dlugi:  .asciiz "Wprowadzony klucz jest za dlugi, sprobuj ponownie\n"
err_key_krotki: .asciiz "Wprowadzony klucz jest za krotki, sproboj ponownie\n"
err_key_value:  .asciiz "Klucz zawiera wartosci z poza zakresu. Ponow probe:\n"
err_option:	.asciiz "Wybrano nie poprawna opcje! Sprobuj ponownie. \n"
out_result:     .asciiz "Wynik: "
range_err:	.asciiz "Program obsluguje tylko wielkie litery. Sprobuj ponownie!\n"
newline:        .asciiz "\n"

buffer:         .space 64      # Bufor na tekst jawny/szyfrogram
normalized_buffer: .space 128  # NOWY BUFOR: Bufor na znormalizowany tekst, większy rozmiar na słowne odpowiedniki
keybuf:         .space 16      # Bufor na klucz
perm:           .space 8       # tablica permutacji
invperm:        .space 8       # Permutacja odwrotna
result:         .space 64      # Bufor na wynik
textlen:        .word 0        # Długość tekstu
keylen:         .word 0        # Długość klucza
encrypt:        .word 0

cyfra0: .asciiz "ZERO"
cyfra1: .asciiz "JEDEN"
cyfra2: .asciiz "DWA"
cyfra3: .asciiz "TRZY"
cyfra4: .asciiz "CZTERY"
cyfra5: .asciiz "PIEC"
cyfra6: .asciiz "SZESC"
cyfra7: .asciiz "SIEDEM"
cyfra8: .asciiz "OSIEM"
cyfra9: .asciiz "DZIEWIEC"

cyfry_tab:
    .word cyfra0, cyfra1, cyfra2, cyfra3, cyfra4, cyfra5, cyfra6, cyfra7, cyfra8, cyfra9

.text
main:
    li $v0, 4                  # Wyświetlenie menu
    la $a0, prompt_op         
    syscall

    li $v0, 8                  # Wczytanie operacji S lub D
    la $a0, buffer             # bufor na odpowiedź
    la $a1, 2                  # Wczytanie 1 znaku + null
    syscall

    li $v0, 4		       # Wyświetlenie znaku nowego wiersza
    la $a0, newline
    syscall

    lb $t0, buffer             # Załadowanie wczytanego znaku do $t1
    
    li $t1, 'S'                # Wczytanie S do porównania
    beq $t0, $t1, szyfruj      # jeśli 'S', przejdź do szyfrowania
    li $t1, 's'                # Wczytanie s do porównania
    beq $t0, $t1, szyfruj      # jeśli 's', przejdź do szyfrowania
    
    li $t2, 'D'                # Wczytanie D do porównania
    beq $t0, $t2, odszyfruj    # jeśli 'D', przejdź do deszyfrowania
    li $t2, 'd'                # Wczytanie d do porównania
    beq $t0, $t2, odszyfruj    # jeśli 'd', przejdź do deszyfrowania

    li $v0, 4			       # Wyświetlenie znaku nowego wiersza
    la $a0, err_option
    syscall
    
    j main                     # Ponowne wywołanie przy niewłaściwym wyborze


wczytaj_klucz:
    li $v0, 4                  # Wyświetlenie wiadomości o podanie klucza
    la $a0, prompt_key
    syscall

    li $v0, 8                  # Wczytanie klucza
    la $a0, keybuf             # bufor na klucz
    li $a1, 16                 # max 15 znaków + null
    syscall

    la $a0, keybuf             # załadowanie klucza od keybuff
    jal sprawdz_klucz          # sprawdź poprawność klucza

    jr $ra                     # powrót do wywołującego


# --- SPRAWDZANIE KLUCZA ---
sprawdz_klucz:
    move $t0, $a0              # Załadowanie adresu klucza do $t0
    li $t1, 0                  # Liczenie długości klucza w $t1 = 0

klucz_len:
    lb $t2, 0($t0)             # Pobranie kolejnego znaku z $t0
    beqz $t2, klucz_endlen     # jeśli null, koniec liczenia długości
    
    la $t3, '\n'               # wczyt2nie '\n' do $t3
    beq $t2, $t3, klucz_endlen # jeśli '\n', koniec liczenia długości
    
    addiu $t0, $t0, 1          # zwiększenie indeksu znaku o 1
    addiu $t1, $t1, 1          # zwiększenie liczby znaków o 1
    
    j klucz_len                # Przeskok do kolejnej iteracji


klucz_endlen:
    sw $t1, keylen            # zapisanie długości klucza w keylen
    
    li $t3, 3
    blt $t1, $t3, klucz_krotko # jeśli długość < 3, wywołanie błędu
    
    li $t3, 8
    bgt $t1, $t3, klucz_dlugo  # jeśli długość > 8, wywołanie błędu

                               # Sprawdź czy cyfry 1-8, brak powtórzeń
    la $t0, keybuf             # $t0 = adres klucza
    li $t2, 0                  # $t2 = indeks
    la $t4, perm               # $t4 = tablica permutacji
    li $t5, 0                  # $t5 = maska użytych cyfr


klucz_loop:
    lb $t6, 0($t0)             # załaduj znak klucza do $t6
    
    beqz $t6, klucz_ok         # jezeli null to koniec sprawdzania
    
    la $t3 '\n'                # załadowanie '\n' do porównania
    beq $t6, $t3, klucz_ok     # jezeli '\n' to koniec sprawdzania
    
    subi $t6, $t6, 48          # zamiana znaku na liczbe poprzez odjecie 48 od ASCII
    blt $t6, 1, klucz_fail     # jezeli liczba mniejsza od 1 to błędny klucz
    
    lw $t7, keylen             # załadowanie długości klucza do $t7
    bgt $t6, $t7, klucz_fail   # jeśli liczba > długość klucza to błędny klucz
    
    # Sprawdzenie powtórzeń
    li $t8, 1                  # załadowanie 1 do $t8
    sllv $t8, $t8, $t6         # przesuń 1 o $t6 pozycji
    and $t9, $t5, $t8          # zastosowanie operacji not na $t5 oraz $t8
    bnez $t9, klucz_fail       # jeśli już ustawione, błąd klucza
    or $t5, $t5, $t8           # ustaw bit
    sb $t6, 0($t4)             # zapisz do perm zaktualizowaną maskę
    addiu $t0, $t0, 1          # kolejny znak
    addiu $t4, $t4, 1          # kolejna pozycja w perm
    j klucz_loop               # kolejna iteracja

klucz_ok:
    lw $t0, encrypt
    li $t1, 1
    beq $t0, $t1, wczytaj_tekst
    j wczytaj_szyfrogram


klucz_krotko:
    li $v0, 4                  # Wyświetlenie komunikatu klucz za krótki
    la $a0, err_key_krotki
    syscall
    j wczytaj_klucz            # Ponowne wczytanie klucza
    
klucz_dlugo:
    li $v0, 4                  # Wyświetlenie komunikatu klucz za krótki
    la $a0, err_key_dlugi
    syscall
    j wczytaj_klucz            # Ponowne wczytanie klucza
    
klucz_fail:
    li $v0, 4                  # Wyświetlenie informacji o błędnym kluczu
    la $a0, err_key_value
    syscall
    j wczytaj_klucz            # Ponowne wczytanie klucza
	
szyfruj:                       # Rozpoczęcie procesu szyfrowania
    li $t0 1
    sw $t0, encrypt
	j wczytaj_klucz
	
wczytaj_tekst:
    li $v0, 4                  # Wyświetlenie komunikatu o wczytaniu tekstu
    la $a0, prompt_text
    syscall

    li $v0, 8                  # Wczytanie tekstu do buffer'a
    la $a0, buffer
    li $a1, 64                 # max 63 znaki + null
    syscall

    la $a0, buffer             # załadowanie adresu buffer'a do $a0
    jal strlen                 # policzenie długości tekstu 
    
    lw $t1, textlen            # załadowanie długości tekstu do textlen
    li $t0, 50                 # załadowanie maksymalnej długości tekstu
    bgt $t1, $t0, za_dlugi     # jeśli za długi, powtórz wczytywanie
    
    la $a0, buffer             # Źródło dla normalizacji
    la $a1, normalized_buffer  # Cel dla normalizacji
    jal normalizuj	           # Normalizacja tekstu

    # Po normalizacji skopiuj znormalizowany tekst z powrotem do buffer
    la $a0, buffer
    la $a1, normalized_buffer
    jal strcpy

    la $a0, buffer 	           # Zapisanie długości tekstu po normalizacji
    jal strlen
    
    li $v0, 4		           # Wyświetlenie tekstu znormalizowanego
    la $a0, buffer
    syscall

    jal szyfruj_permut        # wywołaj szyfrowanie

    li $v0, 4                 # syscall: print_string
    la $a0, out_result        # wypisz "Wynik: "
    syscall

    li $v0, 4                 # syscall: print_string
    la $a0, result            # wypisz zaszyfrowany tekst
    syscall

    li $v0, 4                 # wypisuje nową linię
    la $a0, newline
    syscall

    j koniec                  # zakończ program

za_dlugi:
    li $v0, 4                  # wypisz komunikat o za długim tekście
    la $a0, err_length
    syscall
    j wczytaj_tekst            # powtórz wczytywanie tekstu

strlen:
    move $t0, $a0              # $t0 = adres tekstu
    li $t1, 0                  # licznik długości

strl_loop:
    lb $t2, 0($t0)             # pobierz znak
    
    beqz $t2, strl_end         # jeśli null, koniec
    
    li $t3, '\n'               # przypisanie znaku do porównania
    beq $t2, $t3, strl_end     # jeśli nowa linia, koniec
    
    addiu $t0, $t0, 1          # kolejny znak
    addiu $t1, $t1, 1          # inkrementuj licznik
    j strl_loop

strl_end:
    sw $t1, textlen            # zapisz długość tekstu w textlen
    jr $ra
	
	
# --- NORMALIZACJA ---
# $a0 = adres źródła (original buffer)
# $a1 = adres celu (normalized_buffer)
normalizuj:
    move $t0, $a0         # $t0 = wskaźnik źródła (do odczytu)
    move $t1, $a1         # $t1 = wskaźnik celu (do zapisu)

norm_loop:
    lb $t3, 0($t0)        # Pobierz bieżący znak ze źródła
    beqz $t3, norm_end    # Jeśli null, zakończ normalizację

    li $t4, '\n'
    beq $t3, $t4, norm_end  # Jeśli nowa linia, zakończ

    # Jeśli spacja, zignoruj i przejdź do następnego znaku
    li $t4, 32            # ASCII dla spacji
    beq $t3, $t4, norm_continue 

    # Sprawdź, czy znak jest cyfrą ('0'-'9')
    li $t4, '0'
    li $t5, '9'
    blt $t3, $t4, sprawdz_litere # Jeśli mniejszy niż '0', to nie cyfra
    bgt $t3, $t5, sprawdz_litere # Jeśli większy niż '9', to nie cyfra

    # --- JEST CYFRĄ: Zamień na słowo ---
    # $t3 zawiera cyfrę, $t4 wciąż zawiera '0'
    subu $t6, $t3, $t4    # Zamień znak ASCII na liczbę (0-9)
    la $t7, cyfry_tab
    sll $t8, $t6, 2       # Oblicz offset w tabeli (indeks * 4 bajty)
    addu $t7, $t7, $t8
    lw $t7, 0($t7)        # Załaduj adres słownego odpowiednika cyfry

norm_copy_word_loop:
    lb $t9, 0($t7)
    beqz $t9, norm_continue # Jeśli koniec słowa, przejdź do następnego znaku w buforze
    sb $t9, 0($t1)          # Zapisz literę słowa w docelowym miejscu
    addiu $t1, $t1, 1       # Przesuń wskaźnik zapisu
    addiu $t7, $t7, 1       # Przesuń wskaźnik odczytu słowa
    j norm_copy_word_loop

sprawdz_litere:
    # Sprawdź, czy znak jest wielką literą ('A'-'Z')
    blt $t3, 'A', check_lowercase # Sprawdź znaki spoza zakresu liter
    bgt $t3, 'Z', check_lowercase 

    # --- JEST WIELKĄ LITERĄ: Kopiuj ---
    sb $t3, 0($t1)          # Kopiuj znak
    addiu $t1, $t1, 1       # Przesuń wskaźnik zapisu
    j norm_continue         # Przejdź do następnego znaku źródłowego

check_lowercase:
    # Sprawdź, czy znak nie jest małą literą (błąd zakresu)
    bge $t3, 'a', capital_err
    j norm_continue         # Jeśli to inny znak (np. interpunkcja), zignoruj

capital_err:
    li $v0, 4
    la $a0, range_err
    syscall
    lw $t0, encrypt       
    li $t1, 1
    beq $t0, $t1, wczytaj_tekst
    j wczytaj_szyfrogram

norm_continue:
    addiu $t0, $t0, 1     # Przesuń wskaźnik odczytu do następnego znaku
    j norm_loop

norm_end:
    sb $zero, 0($t1)      # Zakończ wynikowy ciąg znakiem null
    jr $ra

# Funkcja strcpy: kopiuje string ze źródła do celu
# $a0 = cel
# $a1 = źródło
strcpy:
    move $t0, $a0 # dest
    move $t1, $a1 # src
strcpy_loop:
    lb $t2, 0($t1)
    sb $t2, 0($t0)
    beqz $t2, strcpy_done # Kopiuj do napotkania null-terminatora
    addiu $t0, $t0, 1
    addiu $t1, $t1, 1
    j strcpy_loop
strcpy_done:
    jr $ra

# --- SZYFROWANIE PERMUTACYJNE ---
szyfruj_permut:
    la $t0, buffer       # $t0 = źródło
    la $t1, result       # $t1 = bufor docelowy
    lw $s0, textlen      # $s0 = długość tekstu
    lw $s1, keylen       # $s1 = długość klucza
    la $s2, perm         # $s2 = permutacja

    li $t2, 0            # globalny indeks w tekście

szyfruj_loop:
    bge $t2, $s0, szyfruj_done

    subu $t3, $s0, $t2       # ile znaków zostało
    li $t4, 0                # indeks w permutacji
    li $s4, 0                # indeks w permutacji
    la $t5, perm             # reset wskaźnika na perm

szyfruj_blok:
    bge $s4, $s1, blok_koniec

    lb $t6, 0($t5)           # perm[i]
    subi $t6, $t6, 1         # indeks 0-based

    blt $t6, $t3, zapisz     # tylko jeśli w zakresie bloku

    # pomiń ten indeks permutacji
    addiu $t5, $t5, 1
    addiu $s4, $s4, 1
    j szyfruj_blok

zapisz:
    addu $t7, $t0, $t2       # początek bloku w źródle
    addu $t7, $t7, $t6       # przesunięcie wg permutacji
    lb $t8, 0($t7)           # pobierz znak

    addu $t9, $t1, $t2       # początek bloku w wyniku
    addu $t9, $t9, $t4       # miejsce docelowe (perm index)
    sb $t8, 0($t9)

    addiu $t5, $t5, 1
    addiu $t4, $t4, 1
    addiu $s4, $s4, 1
    j szyfruj_blok

blok_koniec:
    addu $t2, $t2, $s1
    j szyfruj_loop

szyfruj_done:
    addu $t3, $t1, $s0
    sb $zero, 0($t3)
    jr $ra

# --- KONIEC SZYFROWANIA PERMUTACYJNEGO ---
szyfruj_start:
	j wczytaj_tekst


odszyfruj:
    li $t0 0
    sw $t0, encrypt
	j wczytaj_klucz

# -- ODSZYFROWYWANIE ---
invert_perm:
    la $s2, perm            # wskaźnik na permutację (1-based)
    la $s3, invperm         # wskaźnik na odwrotną permutację (1-based)
    lw $s1, keylen          # długość permutacji

    li $t0, 0               # indeks i = 0

# Obliczanie odwrotnej permutacji
invert_loop:
    bge $t0, $s1, odszyfruj_permut

    addu $t2, $s2, $t0      # adres perm[i]
    lb $t3, 0($t2)          # odczytaj perm[i] (1-based)

    subi $t4, $t3, 1        # t4 = perm[i] - 1 (indeks 0-based w invperm)
    addu $t5, $s3, $t4      # adres invperm[perm[i]-1]

    addiu $t6, $t0, 1       # i+1 (wartość 1-based)
    sb $t6, 0($t5)          # zapisz do invperm

    addiu $t0, $t0, 1
    j invert_loop

odszyfruj_permut:
    la $t0, buffer          # adres zaszyfrowanego tekstu
    la $t1, result          # adres odszyfrowanego tekstu
    lw $t2, textlen         # długość tekstu
    lw $t3, keylen          # długość klucza
    la $t4, invperm         # adres odwrotnej permutacji

    li $t5, 0               # start aktualnego bloku (offset w tekście)

odszyfruj_loop:
    bge $t5, $t2, odszyfruj_done   # jeśli przetworzyliśmy cały tekst, koniec

    subu $t6, $t2, $t5      # ile znaków zostało w bieżącym bloku

    slt $t7, $t6, $t3
    beq $t7, $zero, pelny_blok

    move $t8, $t6           # niepełny blok
    j kontynuuj

pelny_blok:
    move $t8, $t3           # pełny blok

kontynuuj:
    li $t9, 0               # indeks permutacji (invperm)
    li $s0, 0               # licznik zapisanych znaków w bloku
    move $s1, $t4           # wskaźnik na początek invperm (dla bloku)

odszyfruj_blok:
    bge $t9, $t3, koniec_bloku

    lb $s2, 0($s1)          # invperm[t9] (1-based)
    subi $s2, $s2, 1        # na 0-based indeks źródłowy

    blt $s2, $t8, kopiuj_znak  # kopiuj znak tylko jeśli indeks źródłowy w bloku jest w zakresie
    j pomijaj_znak

kopiuj_znak:
    addu $s3, $t0, $t5      # początek bloku w szyfrogramie
    addu $s3, $s3, $s2      # adres znaku źródłowego
    lb $s4, 0($s3)          # pobierz znak

    addu $s5, $t1, $t5      # początek bloku w wyniku
    addu $s5, $s5, $s0      # adres docelowy (gęsto)
    sb $s4, 0($s5)          # zapisz znak

    addiu $s0, $s0, 1       # zwiększ licznik zapisanych znaków

pomijaj_znak:
    addiu $s1, $s1, 1       # przesuwamy wskaźnik permutacji
    addiu $t9, $t9, 1       # zwiększamy indeks permutacji
    j odszyfruj_blok

koniec_bloku:
    add $t5, $t5, $t3     # przesuwamy się do następnego bloku
    j odszyfruj_loop

odszyfruj_done:
    addu $s6, $t1, $t2
    sb $zero, 0($s6)        # null terminator
    jr $ra
# --- ODSZYFROWYWANIE KONIEC ---

wczytaj_szyfrogram:
    li $v0, 4                # Wyświetlenie komunikatu o wczytaniu tekstu
    la $a0, prompt_ciph
    syscall

    li $v0, 8                # Wczytanie tekstu do buffer'a
    la $a0, buffer
    li $a1, 64               # max 63 znaki + null
    syscall

    la $a0, buffer           # załadowanie adresu buffer'a do $a0
    jal strlen               # policzenie długości tekstu 
    
    lw $t1, textlen          # załadowanie długości tekstu do textlen
    li $t0, 50               # załadowanie maksymalnej długości tekstu
    bgt $t1, $t0, za_dlugi   # jeśli za długi, powtórz wczytywanie

    la $a0, buffer             # Źródło dla normalizacji
    la $a1, normalized_buffer  # Cel dla normalizacji
    jal normalizuj	           # Normalizacja tekstu

    # Po normalizacji skopiuj znormalizowany tekst z powrotem do buffer
    la $a0, buffer
    la $a1, normalized_buffer
    jal strcpy
    
    la $a0, buffer 	         # Zapisanie długości tekstu po normalizacji
    jal strlen
    
    li $v0, 4		         # Wyświetlenie tekstu znormalizowanego
    la $a0, buffer
    syscall

    jal invert_perm # wywołaj odszyfrowywanie

    li $v0, 4                # wypisz "Wynik : "
    la $a0, out_result        
    syscall

    li $v0, 4                 # wypisz zaszyfrowany tekst
    la $a0, result            
    syscall

    li $v0, 4                 # wypisuje nową linię
    la $a0, newline
    syscall

    j koniec                  # zakończ program


koniec:
	li $v0, 10		           # zakonczenie programu
	syscall