 .data
    mem .space  256
.text
    li $r0, 16
    li $r1, 255
    addi $r1, $r1, 2
    sw $r1, mem($r0)
    addi $r0, $r0, 2
    li $r1, 255
    addi $r1, $r1, 17
    sw $r1, mem($r0)
    addi $r0, $r0, 2
    li $r1, 17
    sw $r1, mem($r0)
    addi $r0, $r0, 2
    li $r1, 240
    sw $r1, mem($r0)
    addi $r0, $r0, 2
    li $r1, 255
    sw $r1, mem($r0)

    li $r0, 64
    li $r1, 255
    addi $r1, $r1, 2
    sll $r1, $r1, 4  ; 1010hex
    li $r2, 15  ; 000Fhex
    li $r3, 240 ; 00F0hex
    li $r4, 0   ; t0 = 0000hex
    li $r5, 16  ; a0 = 0010hex
    li $r6, 5   ; a1 = 0005hex
while:
    li $r7, 0   ; $zero
    ble $r6, $r7, endloop    ; branch if (a1 <= 0)
    dec $r6         ; a1 = a1 - 1
    lw $r4, mem($r5)    ; t0 = mem[a0]
if:
    li $r7, 255
    inc $r7         ; r7 = 256 = 0100hex
    ble $r4, $r7, else		; branch to else if (t0 <= 0100hex)
    li $r7, 8
    div $r0, $r0, $r7
    or $r1, $r1, $r0
    li $r7, 255
    sll $r7, $r7, 8
    sw $r7, mem($r5)
    j endif
else:
    li $r7, 4
    mul $r2, $r2, $r7
    xor $r3, $r3, $r2
    li $r7, 255
    sw $r7, mem($r5)
endif:
    addi $r5, $r5, 2 ; a0 = a0 + 2
    j while
endloop:
