def fetch(PC, all_lines, F):
	PC += 1
	F.ins = all_lines[PC][0]
	if F.ins == 'NOP':
		F.rd = F.rt = F.rs = 'xxxx'
		return PC, F
	if (F.ins == 'addi') or (F.ins == 'subi') or (F.ins == 'li') or (F.ins == 'sll') or (F.ins == 'inc') or (F.ins == 'dec') or (F.ins == 'bie'):
		F.rd = all_lines[PC][1]
		F.rt = F.rs = 'xxxx'
	elif (F.ins == 'lw') or (F.ins == 'sw') or (F.ins == 'beq') or (F.ins == 'ble'):
		F.rd = all_lines[PC][1]
		F.rs = all_lines[PC][2]
		F.rt = 'xxxx'
	elif (F.ins == 'or') or (F.ins == 'xor') or (F.ins == 'slt') or (F.ins == 'add') or (F.ins == 'div') or (F.ins == 'mul'):
		F.rd = all_lines[PC][1]
		F.rs = all_lines[PC][2]
		F.rt = all_lines[PC][3]
	elif F.ins == 'j':
		F.rs = F.rt = F.rd = 'xxxx'	
	
	return PC, F

