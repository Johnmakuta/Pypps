li $r0, 30					;r0 = 30
lw $r1, $r0					;r1 = 30					
j over_there    			;go to over_there

addi $r0, 100				


over_there:
addi $r0, $r0, 10				;r0 = 40
sw $r0, $r1						;r1 = 40
add $r0, $r0, $r0 				;r0 = 80
lw $r1, $r0						;r1 = 80
beq $r0, $r1, right_here 		;go to right_there

j dont_go_there		

right_here:
subi $r0, $r0, 1				;r0 = 70				
or $r0, $r1, $r0
xor $r0, $r1, $r0			
slt $r2, $r0, $r1			

li $r2, 2					
div $r1, $r1, $r2			
sll $r1, $r1, 2					
ble $r1, $r2, woo			

woo:
dont_go_there:
