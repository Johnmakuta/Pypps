	li $r0, 0
	inc $r0
	dec $r0

	bie $r0, even
	j odd

even:
	inc $r0

odd:
	dec $r0
