import copy

def decode(PC, all_lines, all_labels, F):

	D = copy.deepcopy(F)
	D.ins = all_lines[PC][0]
	if D.ins == 'NOP':
		D.op, D.func, D.imm = 'xxx', 'xxxx', 'xxxxxxxxx'
		return D
	
	# li, addi, subi, sll
	if D.ins == 'li':
		D.op = '1100'
		D.func = '000'
		D.imm = all_lines[PC][2]
	elif D.ins == 'addi':
		D.op = '1000'
		D.func = '000'
		D.imm = all_lines[PC][3]
	elif D.ins == 'subi':
		D.op = '1001'
		D.func = '000'
		D.imm = all_lines[PC][3]
	elif D.ins == 'sll':
		D.op = '1111'
		D.func = '000'
		D.imm = all_lines[PC][3]
	
	# inc, dec, bie
	elif D.ins == 'inc': 
		D.op = '0011'
		D.func = '000'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'dec': 
		D.op = '0100'
		D.func = '000'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'bie': 
		D.op = '0110'
		D.func = '000'
		D.imm = all_labels[all_lines[PC][2]]
	
	
	# lw, sw, beq, ble
	elif D.ins == 'lw':
		D.op = '1000'
		D.func = '000'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'sw':
		D.op = '1000'
		D.func = '000'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'beq':
		D.op = '0010'
		D.func = '000'
		D.imm = all_labels[all_lines[PC][3]]
	elif D.ins == 'ble':
		D.op = '0101'
		D.func = '000'
		D.imm = all_labels[all_lines[PC][3]]
	
	# or, xor, slt, add, div, mul
	elif D.ins == 'or':
		D.op = '0000'
		D.func = '001'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'xor':
		D.op = '0000'
		D.func = '010'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'slt':
		D.op = '0000'
		D.func = '011'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'add':
		D.op = '0000'
		D.func = '000'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'div':
		D.op = '0000'
		D.func = '100'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'mul':
		D.op = '0000'
		D.func = '101'
		D.imm = 'xxxxxxxxx'
	
	# j
	elif D.ins == 'j':
		D.op = '0001'
		D.func = '000'
		D.imm = all_labels[all_lines[PC][1]]
		
	else:
		D.op = 'U'
		D.func = 'U'
		
	
	if D.imm != 'xxxxxxxxx':
		max_r = 0
		min_r = 0
		if D.ins == 'li':
			max_r = 255
			min_r = -256
		elif D.ins == 'addi' or D.ins == 'subi' or D.ins == 'sll':
			max_r = 31
			min_r = -32
		if max_r != 0:
			if int(D.imm) > max_r: 
				D.imm = int(D.imm) - (round(int(D.imm)/(max_r+1))) * (max_r+1)
			elif int(D.imm) < min_r:
				D.imm = (max_r+1) + (int(D.imm) - (min_r))
		
	
	return D
