	li $r0, 0			;r0 = 0
	inc $r0				;r0 = 1
	dec $r0				;r0 = 0

	bie $r0, even		;goes to even
	dec $r0

even:
	inc $r0				;r0 = 1
