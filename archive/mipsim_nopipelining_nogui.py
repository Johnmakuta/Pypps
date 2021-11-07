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




def load_program_into_memory(file_name, memory):
	all_lines = []
	all_labels = {}
	data_sec = True	# Check for Data Section of Program
	with open(file_name) as test_file:
		for line in test_file:
			if ".data" in line:
				data_sec = True
				continue
			if ".text" in line:
				data_sec = False
				continue
			else:
				# .text section
				if ':' in line:
					all_labels[line.replace(':\n', '')] = (len(all_lines))
					#print(all_labels)
				elif line.startswith('#'):
					pass
				elif line == '\n':
					pass
				elif data_sec:
					array = line.replace(':', '')
					array = array.replace('\n', '').split()
					print('ahahahahah', array)
					array[0] = 'zaro'
					print('ahahahahah', array)
					print(array[0])
					print(array[1])
					print(array[2])
					#size = int(array[2])
					#print(size)
					#size = int(int(array[2])/4)

					#memory[array[0]] = list(0 for n in range(size))
				else:
					line = line.replace(',', '')
					all_lines.append(line.split())
	return all_lines, all_labels




def fetch(PC, all_lines, F):
	PC += 1
	F.ins = all_lines[PC][0]
	if (F.ins == 'addi') or (F.ins == 'subi') or (F.ins == 'li') or (F.ins == 'sll'):
		F.rs = all_lines[PC][1]
		F.rt = F.rd = 'X'
	elif (F.ins == 'lw') or (F.ins == 'sw') or (F.ins == 'beq') or (F.ins == 'ble'):
		F.rs = all_lines[PC][1]
		F.rt = all_lines[PC][2]
		F.rd = 'X'
	elif (F.ins == 'or') or (F.ins == 'xor') or (F.ins == 'slt') or (F.ins == 'add') or (F.ins == 'div') or (F.ins == 'mul'):
		F.rs = all_lines[PC][2]
		F.rt = all_lines[PC][3]
		F.rd = all_lines[PC][1]
	elif F.ins == 'j':
		F.rs = F.rt = F.rd = 'X'	
	else:
		print('      UNKNOWN') 
	
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN
	# CHECK FOR HAZARDS BEFORE YOU RETURN

	return PC, F, F




def decode(PC, all_lines, all_labels, D):
	D.ins = all_lines[PC][0]
	# note to all: these if statements can be 
	# cleaned up a lot, so feel free to do so
	
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
	
	return D, D




def execute(reg_dict, E):
	# li, j, addi, subi, sll
	if E.ins == 'li' or E.ins == 'j':
		result = E.imm
	elif E.ins == 'addi':
		result = int(reg_dict[E.rs]) + int(E.imm)
	elif E.ins == 'subi':
		result = int(reg_dict[E.rs]) - int(E.imm)
	elif E.ins == 'sll':
		result = int(reg_dict[E.rs]) << int(E.imm)
	
	# lw, sw, beq	
	elif E.ins == 'lw':
		result = int(reg_dict[E.rt])
	elif E.ins == 'sw':
		result = int(reg_dict[E.rs])
	elif E.ins == 'beq':
		result = E.imm if int(reg_dict[E.rs]) == int(reg_dict[E.rt]) else 'none'
	elif E.ins == 'ble':
		result = E.imm if int(reg_dict[E.rs]) <= int(reg_dict[E.rt]) else 'none'
		
	# or, xor, slt, add, div, mul
	elif E.ins == 'or':
		result = int(reg_dict[E.rs]) or int(reg_dict[E.rt])
	elif E.ins == 'xor':
		result = int(reg_dict[E.rs]) ^ int(reg_dict[E.rt])
	elif E.ins == 'slt':
		result = 1 if int(reg_dict[E.rs]) < int(reg_dict[E.rt]) else 0
	elif E.ins == 'add':
		result = int(reg_dict[E.rs]) + int(reg_dict[E.rt])
	elif E.ins == 'mul':
		result = int(reg_dict[E.rs]) * int(reg_dict[E.rt])
	elif E.ins == 'div':
		result = int(reg_dict[E.rs]) / int(reg_dict[E.rt])
	
	else:
		result = 'U'
		print('      UNKNOWN') 
		
	return result, E, E




def mem(M):
	if (M.ins == 'li') or (M.ins == 'addi') or (M.ins == 'lw') or (M.ins == 'subi') or (M.ins == 'sll'):
		target = M.rs
	elif M.ins == 'sw':
		target = M.rt
	elif (M.ins == 'add') or (M.ins == 'or') or (M.ins == 'xor') or (M.ins == 'slt') or (M.ins == 'div') or (M.ins == 'mul'):
		target = M.rd
	elif (M.ins == 'j') or (M.ins == 'beq') or (M.ins == 'ble'):
		target = 'PC'
	else:
		target = 'U'
	
	return target




def write_back(reg_dict, target, result, PC):
	# note to pj: test flags
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
			result = result - 32767
		elif int(result) < -32768:
			z = False
			v = True
			result = result + 32768
		else:
			z = False
			v = False
		reg_dict[target] = result
		
	return PC, z, v







# setup
reg_dict = dict([("$r%s" % x, 0) for x in range(4)]) 
memory = {}
print_RF(reg_dict)
PC = -1
F = fields()
D = fields()
E = fields()
M = fields()
user_input = ''
i = 1
z = v = R = False
all_lines, all_labels = load_program_into_memory('array_test.s', memory)


# RUN
while PC < (len(all_lines)-1):
	if not R:
		user_input = input('\n      Enter R to run program to completion. Enter any other key to step. >')
		if user_input.lower() == 'r':
			R = True
	#all_print_fields(F,D,E,M)
	print_RF(reg_dict)
	PC, F, D = fetch(PC, all_lines, F)
	
	D, E = decode(PC, all_lines, all_labels, D)
	
	result, E, M = execute(reg_dict, E)
	
	target = mem(M)
	
	PC, z, v = write_back(reg_dict, target, result, PC)
	
	if not R:
		#print('\n      PC is', PC)
		print('\n      STEP', i) 
		F.print_fields()
		i += 1
		print_RF(reg_dict)
		print('Zero:', z, '\nOverflow:', v)

print()

if(R):
	print('\n      FINAL\n')
	print_RF(reg_dict)
	print('Zero:', z, '\nOverflow:', v, '\n')
