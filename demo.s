li $r0, 600					
lw $r1, $r0					
j over_there    			

addi $r0, 100				


over_there:
addi $r0, $r0, 50				
sw $r0, $r1					
add $r0, $r0, $r0 			
lw $r1, $r0					
beq $r0, $r1, right_here 	

j dont_go_there		

right_here:
subi $r0, $r0, 1000				
or $r0, $r1, $r0			
xor $r0, $r1, $r0			
slt $r2, $r0, $r1			

li $r2, 2					
div $r1, $r1, $r2			
sll $r1, $r1, 2					
ble $r1, $r2, woo			

woo:
dont_go_there:
