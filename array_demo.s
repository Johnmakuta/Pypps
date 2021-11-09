.data
    array   .space 256

.text
    li $r0, 0
    li $r1, 69
    li $r2, 2
    li $r3, 3
    li $r4, 4
    li $r5, 5
    li $r6, 6
    li $r7, 7

    sw $r1, array($r0)
    addi $r0, 2
    sw $r2, array($r0)
    addi $r0, 2
    sw $r3, array($r0)
    addi $r0, 2
    sw $r4, array($r0)
    addi $r0, 2
    sw $r5, array($r0)
    addi $r0, 2
    sw $r6, array($r0)
    addi $r0, 2
    sw $r7, array($r0)
    addi $r0, 2

    li $r0, 0

    lw $r7, array($r0)
    addi $r0, 2
    lw $r6, array($r0)
    addi $r0, 2
    lw $r5, array($r0)
    addi $r0, 2
    lw $r4, array($r0)
    addi $r0, 2
    lw $r3, array($r0)
    addi $r0, 2
    lw $r2, array($r0)
    addi $r0, 2
    lw $r1, array($r0)
    addi $r0, 2
