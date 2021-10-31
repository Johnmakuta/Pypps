li $r0, 600					# r0 = 600
lw $r1, $r0					# r1 = r0 = 600
j over_there    			# jump to the label over_there

addi $r0, 100				# r0 = r0 + 100 = 600 + 100 = 700 

over_there:
addi $r0, 50				# r0 = r0 + 50 = 600 + 50 = 650 
sw $r0, $r1					# r1 = r0 = 650
add $r0, $r0, $r0 			# r0 = r0 + r0 = 650 + 650 = 1300
lw $r1, $r0					# r1 = r0 = 1300
beq $r0, $r1, right_here 	# if r0 == r1, go to right_here (it will go)
j dont_go_there				# jump to the label dont_go_there
right_here:
subi $r0, 1000				# r0 = r0 - 1000 = 1300 - 1000 = 300
or $r0, $r1, $r0			# r0 = r1 or r0
xor $r0, $r1, $r0			# r0 = r1 xor r0
slt $r2, $r0, $r1			# r2 = 1 if r0 < r1 else 0 = 1

li $r2, 2					# r2 = 2
div $r1, $r1, $r2			# r1 = r1 / r2 = 1300 / 2 = 650
sll $r1, 2					# r1 = r1 << 2
ble $r1, $r2, woo			# if r1 <= r2, go to woo (it wont go)
mul $r1, $r1, $r0			# r1 = r1 * r0 = 0

woo:
dont_go_there:
