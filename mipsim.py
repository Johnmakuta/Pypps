class fields:
	def __init__(self):
		self.ins = 'X'
		self.op = 'X'
		self.func = 'X'
		self.rd = 'X'
		self.rs = 'X'
		self.rt = 'X'
		self.imm = 'X'
	def print_fields(self):
		print('\n     ', self.ins, self.op, self.func, self.rd, self.rs, self.rt, self.imm, '\n')

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
				#print(all_labels)
			else:
				line = line.replace(',', '')
				all_lines.append(line.split())
	return all_lines, all_labels

def fetch(PC, all_lines, F):
	F.ins = all_lines[PC][0]
	if F.ins == 'li':
		F.rs = all_lines[PC][1]
		F.rt = F.rd = 'X'
	elif F.ins == 'addi':
		F.rs = all_lines[PC][1]
		F.rt = F.rd = 'X'
	elif F.ins == 'lw':
		F.rs = all_lines[PC][1]
		F.rt = all_lines[PC][2]
		F.rd = 'X'
	elif F.ins == 'sw':
		F.rs = all_lines[PC][1]
		F.rt = all_lines[PC][2]
		F.rd = 'X'
	elif F.ins == 'j':
		F.rs = F.rt = F.rd = 'X'	
	else:
		print('im still working on that part') 
	
	# CHECK FOR A HAZARD BEFORE YOU RETURN
	# CHECK FOR A HAZARD BEFORE YOU RETURN
	# CHECK FOR A HAZARD BEFORE YOU RETURN
	# CHECK FOR A HAZARD BEFORE YOU RETURN
	# CHECK FOR A HAZARD BEFORE YOU RETURN
	# CHECK FOR A HAZARD BEFORE YOU RETURN
	# CHECK FOR A HAZARD BEFORE YOU RETURN

	return PC, F, F

def decode(PC, all_lines, all_labels, D):
	D.ins = all_lines[PC][0]
	if D.ins == 'li':
		D.op = '1100'
		D.func = '000'
		D.imm = all_lines[PC][2]
	elif D.ins == 'addi':
		D.op = '1000'
		D.func = '000'
		D.imm = all_lines[PC][2]
	elif D.ins == 'lw':
		D.op = '1000'
		D.func = '000'
		D.imm = 'X'
	elif D.ins == 'sw':
		D.op = '1000'
		D.func = '000'
		D.imm = 'X'
	elif D.ins == 'j':
		D.op = '0001'
		D.func = '000'
		D.imm = all_labels[all_lines[PC][1]]
	else:
		D.op = 'your'
		D.func = 'mom'
		print('im still working on that part') 
	
	return D, D

def execute(reg_dict, E):
	if E.ins == 'li' or E.ins == 'j':
		result = E.imm
	elif E.ins == 'addi':
		result = int(reg_dict[E.rs]) + int(E.imm)
	elif E.ins == 'lw':
		result = int(reg_dict[E.rt])
	elif E.ins == 'sw':
		result = int(reg_dict[E.rs])
	else:
		result = 'your mom'
		print('im still working on that part') 
		
	return result, E, E

def mem(M):
	if (M.ins == 'li') or (M.ins == 'addi') or (M.ins == 'lw'):
		target = M.rs
	elif M.ins == 'sw':
		target = M.rt
	elif M.ins == 'j':
		target = 'PC'
	else:
		target = 'your_mother'
	
	return target

def write_back(reg_dict, target, result, PC):
	if target == 'PC':
		PC = result-1
	else:
		reg_dict[target] = result
		PC += 1
	return PC



# setup
reg_dict = dict([("$r%s" % x, 0) for x in range(4)]) 
print_RF(reg_dict)
PC = 0
F = fields()
D = fields()
E = fields()
M = fields()
user_input = ''
i = 1
R = False
all_lines, all_labels = load_program_into_memory('i_type_test.s')


# RUN
while PC < (len(all_lines)-1):
	if not R:
		user_input = input('\n      Enter R to run program to completion. Enter any other key to step. >')
		if user_input.lower() == 'r':
			R = True
		
	PC, F, D = fetch(PC, all_lines, F)
	
	print('\n      PC is', PC)
	
	D, E = decode(PC, all_lines, all_labels, D)
	
	result, E, M = execute(reg_dict, E)
	
	target = mem(M)
	
	PC = write_back(reg_dict, target, result, PC)
	
	if not R:
		print('\n      STEP', i)
		F.print_fields()
		i += 1
		print_RF(reg_dict)

if(R):
	print('\n      FINAL\n')
	print_RF(reg_dict)
