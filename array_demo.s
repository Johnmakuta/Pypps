.data
    array   .space 12

.text
    li $r0, 600					
    lw $r1, $r0					
    li $r1, 50
    sw $r1, $r0
    li $r0, 0
    sw $r1, array($r0)
    lw $r0, array($r0)
    li $r0, 2
    li $r7, 69
    sw $r7, array($r0)
    lw $r2, array($r0)
    li $r0, 0
    lw $r3, array($r0)