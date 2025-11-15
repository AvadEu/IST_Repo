.data
stack_space: .space 100   # rezerwacja miejsca na stos (opcjonalnie)


first_word: .word 120
second_word: .word 60

.text
.globl main

main:

    # Push wartości 10 na stos
    lw $t0, first_word            # załaduj 10 do $t0
    addi $sp, $sp, -4     # alokuj miejsce na stosie
    sw $t0, 0($sp)       # zapisz $t0 na stos

    # Push wartości 20 na stos
    lw $t0, second_word
    addi $sp, $sp, -4
    sw $t0, 0($sp)

    # Pop wartości ze stosu do $t1
    lw $t1, 0($sp)        # pobierz ostatni element (20)
    addi $sp, $sp, 4      # zwolnij miejsce
    li $v0, 1
    la $a0, ($t1)
    syscall

    # Pop kolejnej wartości do $t2
    lw $t2, 0($sp)        # pobierz kolejny element (10)
    addi $sp, $sp, 4
    
    li $v0, 1
    la $a0, ($t2)
    syscall

    # Teraz $t1=20, $t2=10

    # Zakończ program
    li $v0, 10
    syscall
