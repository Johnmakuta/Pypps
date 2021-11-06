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
		D.imm = all_lines[PC][2]
	elif D.ins == 'subi':
		D.op = '1001'
		D.func = '000'
		D.imm = all_lines[PC][2]
	elif D.ins == 'sll':
		D.op = '1111'
		D.func = '000'
		D.imm = all_lines[PC][2]
	
	# inc, dec, bie
	elif D.ins == 'inc': #replaces ble
		D.op = '0101'
		D.func = '000'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'dec': #replaces beq
		D.op = '0010'
		D.func = '000'
		D.imm = 'xxxxxxxxx'
	elif D.ins == 'bie': #replaces sll
		D.op = '1111'
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
	
	return D
