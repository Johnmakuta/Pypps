import copy

def mem(E):

	M = copy.deepcopy(E)
	if M.ins == 'NOP':
		target = 'X'
		return target, M, M.result 
	if (M.ins == 'li') or (M.ins == 'addi') or (M.ins == 'lw') or (M.ins == 'subi') or (M.ins == 'sll') or (M.ins == 'inc') or (M.ins == 'dec'):
		target = M.rd
	elif M.ins == 'sw':
		target = M.rs
	elif (M.ins == 'add') or (M.ins == 'or') or (M.ins == 'xor') or (M.ins == 'slt') or (M.ins == 'div') or (M.ins == 'mul'):
		target = M.rd
	elif (M.ins == 'j') or (M.ins == 'beq') or (M.ins == 'ble') or (M.ins == 'bie'):
		target = 'PC'
	else:
		target = 'U'
	
	return target, M, M.result

