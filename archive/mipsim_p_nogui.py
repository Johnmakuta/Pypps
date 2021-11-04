import copy

class fields:
	def __init__(self):
		self.ins = 'N'
		self.op = 'N'
		self.func = 'N'
		self.rd = 'N'
		self.rs = 'N'
		self.rt = 'N'
		self.imm = 'N'
		self.result = 'N'
	def print_fields(self):
		print('     ', self.ins, self.op, self.func, self.rd, self.rs, self.rt, self.imm)




def all_print_fields(F, D, E, M):
	print('\n      ')
	F.print_fields()
	D.print_fields()
	E.print_fields()
	M.print_fields()
	print()




def print_RF(RF):
	for reg, value in RF.items():
		print("{} {}".format(reg, value))
	print()




def load_program_into_memory(file_name):
	all_lines = []
	all_labels = {}
	with open(file_name) as test_file:
		for line in test_file:
			if ':' in line:
				all_labels[line.replace(':\n', '')] = (len(all_lines))
			elif line.startswith('#') or (line == '\n'):
				pass
			else:
				line = line.replace(',', '')
				line = line.split()
				if (len(line) > 3) and (len(all_lines) > 0):
					if (len(line) > 3) and (len(all_lines) > 0):
						all_lines.append('NOP1')
						all_lines.append('NOP2')
						all_lines.append(line)
					else:
						all_lines.append(line)
				elif (len(line) > 2) and (len(all_lines) > 0):
					if line[1] in all_lines[len(all_lines)-1] or line[2] in all_lines[len(all_lines)-1]:
						all_lines.append('NOP3')
						all_lines.append('NOP4')
						all_lines.append(line)
					else:
						all_lines.append(line)
				else:
					all_lines.append(line)
					all_lines.append('NOP5')
					all_lines.append('NOP6')
					all_lines.append('NOP7')
					
				if (line[0] == 'beq') or (line[0] == 'ble'):
					all_lines.append('NOP8')
					all_lines.append('NOP9')
					all_lines.append('NOP10')
				
					
	print(all_lines)
	return all_lines, all_labels

def fetch(PC, all_lines, F):
	PC += 1
	print(len(all_lines), PC)
	F.ins = all_lines[PC][0]
	if F.ins == 'N':
		F.rd = F.rt = F.rs = 'X'
		return PC, F
	if (F.ins == 'addi') or (F.ins == 'subi') or (F.ins == 'li') or (F.ins == 'sll'):
		F.rd = all_lines[PC][1]
		F.rt = F.rs = 'X'
	elif (F.ins == 'lw') or (F.ins == 'sw') or (F.ins == 'beq') or (F.ins == 'ble'):
		F.rd = all_lines[PC][1]
		F.rs = all_lines[PC][2]
		F.rt = 'X'
	elif (F.ins == 'or') or (F.ins == 'xor') or (F.ins == 'slt') or (F.ins == 'add') or (F.ins == 'div') or (F.ins == 'mul'):
		F.rd = all_lines[PC][1]
		F.rs = all_lines[PC][2]
		F.rt = all_lines[PC][3]
	elif F.ins == 'j':
		F.rs = F.rt = F.rd = 'X'	
	else:
		print(F.ins)
		print('      UNKNOWN') 
	
	return PC, F




def decode(PC, all_lines, all_labels, F):

	D = copy.deepcopy(F)
	D.ins = all_lines[PC][0]
	if D.ins == 'N':
		D.op = D.func = D.imm = 'X'
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
	
	# lw, sw, beq, ble
	elif D.ins == 'lw':
		D.op = '1000'
		D.func = '000'
		D.imm = 'X'
	elif D.ins == 'sw':
		D.op = '1000'
		D.func = '000'
		D.imm = 'X'
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
		D.imm = 'X'
	elif D.ins == 'xor':
		D.op = '0000'
		D.func = '010'
		D.imm = 'X'
	elif D.ins == 'slt':
		D.op = '0000'
		D.func = '011'
		D.imm = 'X'
	elif D.ins == 'add':
		D.op = '0000'
		D.func = '000'
		D.imm = 'X'
	elif D.ins == 'div':
		D.op = '0000'
		D.func = '100'
		D.imm = 'X'
	elif D.ins == 'mul':
		D.op = '0000'
		D.func = '101'
		D.imm = 'X'
	
	# j
	elif D.ins == 'j':
		D.op = '0001'
		D.func = '000'
		D.imm = all_labels[all_lines[PC][1]]
		
	else:
		D.op = 'U'
		D.func = 'U'
		print('      UNKNOWN') 
	
	return D




def execute(reg_dict, D):

	E = copy.deepcopy(D)
	if E.ins == 'N':
		E.result = 'X'
		return E
	# li, j, addi, subi, sll
	if E.ins == 'li' or E.ins == 'j':
		E.result = E.imm
	elif E.ins == 'addi':
		E.result = int(reg_dict[E.rd]) + int(E.imm)
	elif E.ins == 'subi':
		E.result = int(reg_dict[E.rd]) - int(E.imm)
	elif E.ins == 'sll':
		E.result = int(reg_dict[E.rd]) << int(E.imm)
	
	# lw, sw, beq	
	elif E.ins == 'lw':
		E.result = int(reg_dict[E.rs])
	elif E.ins == 'sw':
		E.result = int(reg_dict[E.rd])
	elif E.ins == 'beq':
		E.result = E.imm if int(reg_dict[E.rd]) == int(reg_dict[E.rs]) else 'none'
	elif E.ins == 'ble':
		E.result = E.imm if int(reg_dict[E.rd]) <= int(reg_dict[E.rs]) else 'none'
		
	# or, xor, slt, add, div, mul
	elif E.ins == 'or':
		E.result = int(reg_dict[E.rs]) or int(reg_dict[E.rt])
	elif E.ins == 'xor':
		E.result = int(reg_dict[E.rs]) ^ int(reg_dict[E.rt])
	elif E.ins == 'slt':
		E.result = 1 if int(reg_dict[E.rs]) < int(reg_dict[E.rt]) else 0
	elif E.ins == 'add':
		E.result = int(reg_dict[E.rs]) + int(reg_dict[E.rt])
	elif E.ins == 'mul':
		E.result = int(reg_dict[E.rs]) * int(reg_dict[E.rt])
	elif E.ins == 'div':
		E.result = int(reg_dict[E.rs]) / int(reg_dict[E.rt])
	
	else:
		result = 'U'
		print('      UNKNOWN') 
		
	return E




def mem(E):

	M = copy.deepcopy(E)
	if M.ins == 'N':
		target = 'X'
		return target, M 
	if (M.ins == 'li') or (M.ins == 'addi') or (M.ins == 'lw') or (M.ins == 'subi') or (M.ins == 'sll'):
		target = M.rd
	elif M.ins == 'sw':
		target = M.rs
	elif (M.ins == 'add') or (M.ins == 'or') or (M.ins == 'xor') or (M.ins == 'slt') or (M.ins == 'div') or (M.ins == 'mul'):
		target = M.rd
	elif (M.ins == 'j') or (M.ins == 'beq') or (M.ins == 'ble'):
		target = 'PC'
	else:
		target = 'U'
	
	return target, M




def write_back(reg_dict, target, PC, M):

	# note to pj: test flags
	if M.ins == 'N':
		z = False
		v = False
		result = 'X'
		return PC, z, v
	result = M.result
	z = v = False
	if result == 'none':
		pass
	elif target == 'PC':
		PC = result-1
	else:
		if int(result) == 0:
			z = True
			v = False
		elif int(result) > 32767:
			z = False
			v = True 
			result = result - (round(result/32767)+1) * 32767
		elif int(result) < -32768:
			z = False
			v = True
			result = result + (round(result/32768)+1) * 32768
		else:
			z = False
			v = False
		reg_dict[target] = result
	#reg_dict[target] = result
		
	return PC, z, v







# setup
reg_dict = dict([("$r%s" % x, 0) for x in range(4)]) 
print_RF(reg_dict)
PC = -1
F = fields()
D = fields()
E = fields()
M = fields()
user_input = ''
i = 1
z = v = R = False
all_lines, all_labels = load_program_into_memory('test.s')


# RUN
while PC < (len(all_lines)-2):
	if not R:
		user_input = input('\n      Enter R to run program to completion. Enter any other key to step. >')
		if user_input.lower() == 'r':
			R = True
	
	lines_left = (len(all_lines)-1) - PC
	
	#1
	PC, F = fetch(PC, all_lines, F)
	all_print_fields(F,D,E,M)

	
	#2
	D = decode(PC, all_lines, all_labels, F)
	all_print_fields(F,D,E,M)
	PC, F = fetch(PC, all_lines, F)	
	all_print_fields(F,D,E,M)
	
	#3
	
	E = execute(reg_dict, D)
	all_print_fields(F,D,E,M)
	D = decode(PC, all_lines, all_labels, F)
	all_print_fields(F,D,E,M)
	PC, F = fetch(PC, all_lines, F)
	all_print_fields(F,D,E,M)
	
	#4
	target, M = mem(E)
	all_print_fields(F,D,E,M)
	E = execute(reg_dict, D)
	all_print_fields(F,D,E,M)
	D = decode(PC, all_lines, all_labels, F)
	all_print_fields(F,D,E,M)
	PC, F = fetch(PC, all_lines, F)
	
	#5
	PC, z, v = write_back(reg_dict, target, PC, M)
	all_print_fields(F,D,E,M)
	target, M = mem(E)
	all_print_fields(F,D,E,M)
	E = execute(reg_dict, D)
	all_print_fields(F,D,E,M)
	D = decode(PC, all_lines, all_labels, F)
	
	#6
	PC, z, v = write_back(reg_dict, target, PC, M)
	all_print_fields(F,D,E,M)
	target, M = mem(E)
	all_print_fields(F,D,E,M)
	E = execute(reg_dict, D)
	all_print_fields(F,D,E,M)
		
	#7
	PC, z, v = write_back(reg_dict, target, PC, M)
	all_print_fields(F,D,E,M)
	target, M = mem(E)
	all_print_fields(F,D,E,M)
	
	#8
	PC, z, v = write_back(reg_dict, target, PC, M)
	all_print_fields(F,D,E,M)
	
	
	if not R:
		#print('\n      PC is', PC)
		print('\n      STEP', i) 
		#F.print_fields()
		all_print_fields(F, D, E, M)
		i += 1
		print_RF(reg_dict)
		print('Zero:', z, '\nOverflow:', v)

print()

if(R):
	print('\n      FINAL\n')
	print_RF(reg_dict)
	print('Zero:', z, '\nOverflow:', v, '\n')
