import copy

def flusher(PC, imm, all_lines, F, D):	
	if PC != imm:
		D.ins = 'NOP'
		if (PC+1) != imm:
			F.ins = 'NOP'
	return all_lines, F, D

def mem(E, F, D, all_lines, PC):

	M = copy.deepcopy(E)
	if M.ins == 'NOP':
		target = 'X'
		return target, M, M.result, F, D, all_lines
	if (M.ins == 'li') or (M.ins == 'addi') or (M.ins == 'lw') or (M.ins == 'subi') or (M.ins == 'sll') or (M.ins == 'inc') or (M.ins == 'dec'):
		target = M.rd
	elif M.ins == 'sw':
		target = M.rs
	elif (M.ins == 'add') or (M.ins == 'or') or (M.ins == 'xor') or (M.ins == 'slt') or (M.ins == 'div') or (M.ins == 'mul'):
		target = M.rd
	elif (M.ins == 'j') or (M.ins == 'beq') or (M.ins == 'ble') or (M.ins == 'bie'):
		target = 'PC'
		if M.result != 'none':
			all_lines, F, D = flusher(PC, M.result, all_lines, F, D)
	else:
		target = 'U'
	
	return target, M, M.result, F, D, all_lines

