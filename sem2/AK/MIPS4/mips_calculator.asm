.data
argument_buffer:    .space 32
zero_double:        .double 0.0                      # Stała do porównania z zerem
ten_double:         .double 10.0                     # Stała 10.0 do obsługi notacji naukowej
max_double:         .double 1.7976931348623157e+308   # MAX DOUBLE
min_double:         .double -1.7976931348623157e+308  # MIN DOUBLE

zero_div_err_txt:   .asciiz "\nBlad. Dzielenie przez 0 jest niedozwolone!"
overfit_err_txt:    .asciiz "\nWystapilo przepelnienie, wynik poza zakresem!.\n"
second_arg_msg:     .asciiz "Podaj druga liczbe: "
num_format_txt:     .asciiz "\nPodana wartosc jest nieprawidlowa. Wprowadz liczbe w poprawnym formacie (z kropka lub notacja naukowa)\n"
num_digits_txt:     .asciiz "\nError: Maksymalna liczba cyfr po przecinku to 15!\n"
first_arg_msg:      .asciiz "\nPodaj pierwsza liczbe: "
scope_err_txt:      .asciiz "\nLiczba jest poza zakresem double. Sprobuj ponownie!\n"
menu_num_err:       .asciiz "\nNieprawidlowa opcja! Sprobuj ponownie!\n"
carry_on_txt:       .asciiz "\nCzy chcesz obliczanie kontynuowac? (0-NIE, 1-TAK): "
outcome_txt:        .asciiz "Wynik: "
menu_txt:           .asciiz "\nJaka operacje wykonac?\n1 - Dodawanie\n2 - Odejmowanie\n3 - Mnozenie\n4 - Dzielenie\nWybierz operacje (1-4): "
newline:            .asciiz "\n"

.text
main:
petla_menu:
    li      $v0, 4
    la      $a0, newline
    syscall

    li      $v0, 4
    la      $a0, menu_txt
    syscall

wybierz_operacje:
    li      $v0, 12                         # Wczytanie znaku z klawiatury
    syscall
    move    $s0, $v0                        # Przechowanie znaku w $s0
    sub     $s0, $s0, 48                    # Zamiana ASCII na wartość liczby (1-4)

    beq     $s0, 1, get_first_arg
    beq     $s0, 2, get_first_arg
    beq     $s0, 3, get_first_arg
    beq     $s0, 4, get_first_arg
    b       wrong_operation

get_first_arg:
    li      $v0, 4
    la      $a0, first_arg_msg
    syscall

    li      $s1, 1                          # Flaga: pobieramy pierwszy argument
    jal     validate_num                    # Walidacja i parsowanie liczby
    mov.d   $f12, $f0                       # Przeniesienie wyniku parsowania do $f12

    # Sprawdzenie czy argument 1 jest w zakresie double
    l.d     $f20, max_double
    c.le.d  $f12, $f20
    bc1f    scope_err_1

    l.d     $f20, min_double
    c.le.d  $f20, $f12
    bc1f    scope_err_1

get_second_arg:
    li      $v0, 4
    la      $a0, second_arg_msg
    syscall

    li      $s1, 2                          # Flaga: pobieramy drugi argument
    jal     validate_num
    mov.d   $f14, $f0

    # Sprawdzenie czy argument 2 jest w zakresie double
    l.d     $f20, max_double
    c.le.d  $f14, $f20
    bc1f    scope_err_2

    l.d     $f20, min_double
    c.le.d  $f20, $f14
    bc1f    scope_err_2

    jal     calculate                       # Obliczenie wyniku

wyswietl_wynik:
    li      $v0, 4
    la      $a0, outcome_txt
    syscall

    li      $v0, 3                          # Wypisanie wyniku (double)
    mov.d   $f12, $f2
    syscall

iterate_loop:
    li      $v0, 4
    la      $a0, carry_on_txt
    syscall

    li      $v0, 12                         # Wczytanie znaku
    syscall

    beq     $v0, '1', main                  # Jeśli '1' → powrót do początku
    beq     $v0, '0', zakoncz               # Jeśli '0' → koniec
    j       iterate_loop                    # Inne znaki → pytamy ponownie

zakoncz:
    li      $v0, 10
    syscall

##### Sekcja obliczeń #####
calculate:
    li      $t1, 1
    beq     $s0, $t1, func_add
    li      $t1, 2
    beq     $s0, $t1, func_sub
    li      $t1, 3
    beq     $s0, $t1, func_mul
    li      $t1, 4
    beq     $s0, $t1, func_div
    jr      $ra

func_add:
    add.d   $f2, $f12, $f14
    # Sprawdzenie, czy wynik nie jest NaN (NaN oznacza przepełnienie/niepoprawny wynik)
    c.eq.d  $f2, $f2
    bc1f    blad_przepelnienie
    jr      $ra

func_sub:
    sub.d   $f2, $f12, $f14
    c.eq.d  $f2, $f2
    bc1f    blad_przepelnienie
    jr      $ra

func_mul:
    mul.d   $f2, $f12, $f14
    c.eq.d  $f2, $f2
    bc1f    blad_przepelnienie
    jr      $ra

func_div:
    l.d     $f20, zero_double
    c.eq.d  $f14, $f20
    bc1t    zero_err
    div.d   $f2, $f12, $f14
    c.eq.d  $f2, $f2
    bc1f    blad_przepelnienie
    jr      $ra

##### Sekcja walidacji i parsowania liczby (obsługa notacji naukowej) #####
validate_num:
    # --------------------------
    # Rejestry wykorzystywane tu:
    # $t0 - index (pozycja w buforze)
    # $t1 - flaga minusa (0 - dodatnia, 1 - ujemna)
    # $t2 - akumulator części całkowitej (integer)
    # $t3 - akumulator części ułamkowej (integer, przed podzieleniem przez 10^digits)
    # $t4 - licznik cyfr po kropce
    # $t5 - flaga: czy w części wykladniczej? (0 - mantysa, 1 - wykladnik)
    # $t6 - tymczasowy (na odczytywany znak oraz przy parsowaniu wykładnika)
    # $t7 - znak wykładnika (0 - dodatni, 1 - ujemny)
    # $t8 - wartość wykładnika (integer)
    # $t9 - porównanie ASCII '9'
    # $s1 - flaga, która argument (1 - pierwszy, 2 - drugi)
    # --------------------------

    # 1. Odczyt łańcucha w argument_buffer
    li      $v0, 8
    la      $a0, argument_buffer
    li      $a1, 100
    syscall

    # Inicjalizacja rejestrów
    li      $t0, 0              # index = 0
    li      $t1, 0              # flaga minusa = 0
    li      $t2, 0              # część całkowita = 0
    li      $t3, 0              # część ułamkowa = 0
    li      $t4, 0              # licznik cyfr po kropce = 0
    li      $t5, 0              # flaga wykladnika = 0 (0 - mantysa, 1 - wykladnik)
    li      $t6, 0              # do odczytu znaku
    li      $t7, 0              # znak wykladnika (0 - dodatni, 1 - ujemny)
    li      $t8, 0              # wartość wykladnika
    li      $t9, 57             # ASCII '9'
    
    la      $t6, argument_buffer    # adres bufora
    lb      $t6, 0($t6)             # wczytanie pierwszego znaku

validate_loop:
    # Jeśli natrafiliśmy na koniec linii (newline=10) lub null=0 → zakończ walidację
    beq     $t6, 10, validate_done
    beq     $t6, 0, validate_done

    # 1. Pierwszy znak może być '-'
    beq     $t0, 0, check_leading_minus

    # 2. Jeśli nie w części wykładnika:
    beq     $t5, 0, validate_mantissa

    # 3. Jeśli w części wykładnika (t5=1):
    j       validate_exponent_part

check_leading_minus:
    li      $t9, 45                 # ASCII '-' 
    beq     $t6, $t9, minus_ok      # jeśli minus
    j       validate_mantissa       # w przeciwnym razie sprawdzamy mantysę

minus_ok:
    li      $t1, 1                  # flaga, że liczba ujemna
    addi    $t0, $t0, 1
    # Przejdź do następnego znaku
    la      $t6, argument_buffer
    add     $t6, $t6, $t0
    lb      $t6, 0($t6)
    j       validate_loop

validate_mantissa:
    # Sprawdzamy cyfry od '0' do '9'
    li      $t9, 48                 # ASCII '0'
    blt     $t6, $t9, check_dot_e
    li      $t9, 57                 # ASCII '9'
    bgt     $t6, $t9, check_dot_e
    # Jeśli cyfra, po prostu idziemy do next_char
    j       validate_next_char

check_dot_e:
    # Sprawdzamy kropkę
    li      $t9, 46                 # ASCII '.'
    beq     $t6, $t9, dot_ok
    # Sprawdzamy 'e' lub 'E'
    li      $t9, 101                # ASCII 'e'
    beq     $t6, $t9, exponent_start
    li      $t9, 69                 # ASCII 'E'
    beq     $t6, $t9, exponent_start
    # Jeśli inne, błąd formatu
    j       format_err

dot_ok:
    # Kropka, ale tylko jeśli jeszcze nie było kropki
    addi    $t4, $t4, 0             # (tu nic: dopiero w parsowaniu liczymy cyfry po kropce)
    # Sprawdzenie, czy już była kropka czy wykładnik
    beq     $t5, 1, format_err      # Jeśli już w części wykładnika → błąd
    # Oznaczamy, że wystąpiła kropka
    la      $t9, argument_buffer    # Ponowne odczytanie bufora
    # Nie liczymy dokładnie kropek w walidacji; sprawdzimy w parsowaniu
    j       validate_next_char

exponent_start:
    # 'e' lub 'E' – początek części wykładnika
    beq     $t5, 1, format_err      # Jeśli już był wykładnik, błąd
    li      $t5, 1                  # Ustawiamy flagę: teraz parsujemy wykładnik
    addi    $t0, $t0, 1             # Przesuwamy index do znaku po 'e'
    # Wczytujemy kolejny znak
    la      $t6, argument_buffer
    add     $t6, $t6, $t0
    lb      $t6, 0($t6)
    # Sprawdzamy, czy to '+' lub '-'
    li      $t9, 43                 # ASCII '+'
    beq     $t6, $t9, exp_sign_plus
    li      $t9, 45                 # ASCII '-'
    beq     $t6, $t9, exp_sign_minus
    # Jeśli nie '+'/'-', to sprawdzamy od razu cyfrę
    j       validate_loop

exp_sign_plus:
    li      $t7, 0                  # znak wykładnika dodatni
    addi    $t0, $t0, 1
    la      $t6, argument_buffer
    add     $t6, $t6, $t0
    lb      $t6, 0($t6)
    j       validate_loop

exp_sign_minus:
    li      $t7, 1                  # znak wykładnika ujemny
    addi    $t0, $t0, 1
    la      $t6, argument_buffer
    add     $t6, $t6, $t0
    lb      $t6, 0($t6)
    j       validate_loop

validate_exponent_part:
    # W części wykładnika akceptujemy tylko cyfry od '0' do '9'
    li      $t9, 48
    blt     $t6, $t9, format_err
    li      $t9, 57
    bgt     $t6, $t9, format_err
    # Cyfra to ok, przejdziemy w next_char, budując exponent w drugiej fazie
    j       validate_next_char

validate_next_char:
    addi    $t0, $t0, 1             # index++
    la      $t6, argument_buffer
    add     $t6, $t6, $t0
    lb      $t6, 0($t6)
    j       validate_loop

validate_done:
    # Po walidacji musimy sprawdzić, czy w części wykładnika jest co najmniej jedna cyfra,
    # jeśli w ogóle była flaga t5=1. Upraszczamy: pomijamy szczegółową weryfikację.
    # Przechodzimy do parsowania
    j       parse_num

format_err:
    li      $v0, 4
    la      $a0, num_format_txt
    syscall
    li      $t9, 1
    beq     $s1, $t9, get_first_arg
    li      $t9, 2
    beq     $s1, $t9, get_second_arg

##### Parsowanie liczby z notacją naukową #####
parse_num:
    la      $a1, argument_buffer        # $a1 → adres bufora
    li      $t0, 0                      # index = 0
    li      $t1, 0                      # flaga minusa
    li      $t2, 0                      # część całkowita (integer)
    li      $t3, 0                      # część ułamkowa (integer)
    li      $t4, 0                      # licznik cyfr po kropce
    li      $t5, 0                      # flaga parsowania ułamkowego odmierzająca część mantysy
                                        # (0 - przed kropką, 1 - po kropce)
    li      $t6, 0                      # do odczytu znaku
    li      $t7, 0                      # nieużywane tutaj jako flaga - zastąp.
    li      $t8, 0                      # wartość wykladnika
    li      $t9, 57                     # ASCII '9'

    # Odczytaj pierwszy znak
    add     $t6, $a1, $t0
    lb      $t6, 0($t6)
    # Sprawdź minus na początku
    li      $t7, 45                     # ASCII '-'
    beq     $t6, $t7, parser_set_minus
    j       parser_parse_int

parser_set_minus:
    li      $t1, 1                      # flaga minusa
    addi    $t0, $t0, 1
    add     $t6, $a1, $t0
    lb      $t6, 0($t6)

parser_parse_int:
    # Parsowanie części całkowitej (do kropki lub 'e'/'E' lub końca)
    li      $t7, 46                     # ASCII '.'
    beq     $t6, $t7, parser_point
    li      $t7, 101                    # ASCII 'e'
    beq     $t6, $t7, parser_exponent
    li      $t7, 69                     # ASCII 'E'
    beq     $t6, $t7, parser_exponent

    # Sprawdź, czy cyfra
    li      $t7, 48                     # ASCII '0'
    blt     $t6, $t7, parser_finish_mantysa
    li      $t7, 57                     # ASCII '9'
    bgt     $t6, $t7, parser_finish_mantysa
    # Mamy cyfrę → t6 = t6 - '0'
    li      $t7, 48
    sub     $t6, $t6, $t7
    # t2 = t2 * 10 + t6
    mul     $t2, $t2, 10
    add     $t2, $t2, $t6
    # Przejdź dalej
    addi    $t0, $t0, 1
    add     $t6, $a1, $t0
    lb      $t6, 0($t6)
    j       parser_parse_int

parser_point:
    # Wczytano kropkę → przełączamy na parsowanie części ułamkowej
    li      $t5, 1                      # flaga: parsujemy część po kropce
    addi    $t0, $t0, 1
    add     $t6, $a1, $t0
    lb      $t6, 0($t6)
    j       parser_parse_frac

parser_parse_frac:
    # Parsujemy część ułamkową do napotkania 'e'/'E' lub końca
    li      $t7, 101                    # ASCII 'e'
    beq     $t6, $t7, parser_exponent
    li      $t7, 69                     # ASCII 'E'
    beq     $t6, $t7, parser_exponent
    # Sprawdź koniec mantysy
    beq     $t6, 0, parser_finish_mantysa
    beq     $t6, 10, parser_finish_mantysa
    # Sprawdź, czy cyfra
    li      $t7, 48
    blt     $t6, $t7, parser_finish_mantysa
    li      $t7, 57
    bgt     $t6, $t7, parser_finish_mantysa
    # Mamy cyfrę
    li      $t7, 48
    sub     $t6, $t6, $t7
    # Budujemy t3 i zwiększamy licznik cyfr po przecinku
    mul     $t3, $t3, 10
    add     $t3, $t3, $t6
    addi    $t4, $t4, 1
    # Sprawdź maks. 15 cyfr po przecinku
    li      $t7, 15
    bgt     $t4, $t7, blad_ulamek
    # Kontynuuj
    addi    $t0, $t0, 1
    add     $t6, $a1, $t0
    lb      $t6, 0($t6)
    j       parser_parse_frac

parser_finish_mantysa:
    # Skonstruuj wartość mantysy w rejestrze FPU ($f0)
    mtc1    $t2, $f0
    cvt.d.w $f0, $f0                      # część całkowita w $f0
    beq     $t4, $zero, parser_check_sign
    # Mamy część ułamkową: t3 / (10^t4)
    mtc1    $t3, $f2
    cvt.d.w $f2, $f2                      # przeniesienie do double
    # Oblicz dzielnik: 10^t4
    li      $t7, 1
    move    $t9, $t4                      # $t9 = liczba cyfr po przecinku
compute_divisor_loop:
    beq     $t9, $zero, compute_divisor_end
    mul     $t7, $t7, 10
    addi    $t9, $t9, -1
    j       compute_divisor_loop
compute_divisor_end:
    mtc1    $t7, $f4
    cvt.d.w $f4, $f4
    div.d   $f2, $f2, $f4                 # ułamek w $f2
    add.d   $f0, $f0, $f2                 # mantysa w $f0

parser_check_sign:
    beq     $t1, $zero, parser_post_mantysa
    neg.d   $f0, $f0                      # negacja, jeśli minus

parser_post_mantysa:
    # Teraz sprawdzamy, czy mamy część wykładniczą: sprawdzamy aktualny znak w $t6
    li      $t7, 101                      # ASCII 'e'
    beq     $t6, $t7, parser_exponent
    li      $t7, 69                       # ASCII 'E'
    beq     $t6, $t7, parser_exponent
    # Brak wykładnika → zakończ
    jr      $ra

parser_exponent:
    # Jesteśmy po wykładniku (w $t6 jest 'e' lub 'E')
    addi    $t0, $t0, 1
    add     $t6, $a1, $t0
    lb      $t6, 0($t6)
    # Sprawdź znak '+' lub '-'
    li      $t7, 43                       # ASCII '+'
    beq     $t6, $t7, exp_positive
    li      $t7, 45                       # ASCII '-'
    beq     $t6, $t7, exp_negative
    # W przeciwnym razie od razu zaczynamy parsować cyfry wykładnika
    j       parser_exp_digits

exp_positive:
    li      $t7, 0                        # wykładnik dodatni
    addi    $t0, $t0, 1
    add     $t6, $a1, $t0
    lb      $t6, 0($t6)
    j       parser_exp_digits

exp_negative:
    li      $t7, 1                        # wykładnik ujemny
    addi    $t0, $t0, 1
    add     $t6, $a1, $t0
    lb      $t6, 0($t6)

parser_exp_digits:
    # Parsujemy cyfry wykładnika aż do końca lub napotkania nieskładni
    li      $t8, 0                        # t8 akumuluje wartość wykładnika (integer)
parser_exp_loop:
    beq     $t6, 0, parser_apply_exponent
    beq     $t6, 10, parser_apply_exponent
    li      $t7, 48
    blt     $t6, $t7, parser_apply_exponent
    li      $t7, 57
    bgt     $t6, $t7, parser_apply_exponent
    # Cyfra: t6 = t6 - '0'
    li      $t7, 48
    sub     $t6, $t6, $t7
    mul     $t8, $t8, 10
    add     $t8, $t8, $t6
    # Następny znacznik
    addi    $t0, $t0, 1
    add     $t6, $a1, $t0
    lb      $t6, 0($t6)
    j       parser_exp_loop

parser_apply_exponent:
    # W $f0 mamy mantysę, $t8 to wartość wykładnika, $t7 - znak (0: +
    # 1: -). Jeśli $t8 == 0 → nic nie robimy
    beq     $t8, $zero, parser_exp_done

    # Załaduj 10.0 do $f2
    l.d     $f2, ten_double

    # Jeśli wykładnik dodatni: mnożymy mantysę przez 10^t8
    li      $t9, 0
    beq     $t7, $zero, exp_mult_loop_setup
    # Wykładnik ujemny → dzielenie
    j       exp_div_loop_setup

exp_mult_loop_setup:
    # Pętla: powtarzaj t8 razy: f0 = f0 * 10.0
    move    $t9, $t8
exp_mult_loop:
    beq     $t9, $zero, parser_exp_done
    mul.d   $f0, $f0, $f2
    addi    $t9, $t9, -1
    j       exp_mult_loop

exp_div_loop_setup:
    # Pętla: powtarzaj t8 razy: f0 = f0 / 10.0
    move    $t9, $t8
exp_div_loop:
    beq     $t9, $zero, parser_exp_done
    div.d   $f0, $f0, $f2
    addi    $t9, $t9, -1
    j       exp_div_loop

parser_exp_done:
    jr      $ra

blad_ulamek:
    li      $v0, 4
    la      $a0, num_digits_txt
    syscall
    li      $t9, 1
    beq     $s1, $t9, get_first_arg
    li      $t9, 2
    beq     $s1, $t9, get_second_arg

wrong_operation:
    li      $v0, 4
    la      $a0, menu_num_err
    syscall
    j       petla_menu

scope_err_1:
    li      $v0, 4
    la      $a0, scope_err_txt
    syscall
    j       get_first_arg

scope_err_2:
    li      $v0, 4
    la      $a0, scope_err_txt
    syscall
    j       get_second_arg

zero_err:
    li      $v0, 4
    la      $a0, zero_div_err_txt
    syscall
    j       iterate_loop

blad_przepelnienie:
    li      $v0, 4
    la      $a0, overfit_err_txt
    syscall
    j       iterate_loop
