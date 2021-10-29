# testing functions vvv
def test_load_immediate(reg_dict, index, immediate):
	reg_dict[index]=immediate
	print('li', index, immediate)
	
def test_add_immediate(reg_dict, index, immediate):
	reg_dict[index] = int(reg_dict[index]) + int(immediate)
	print('addi', index, immediate)

def test_file(reg_dict, file_name): # use this to run the entire file
	with open(file_name) as test_file:
		for line in test_file:
			line = line.replace(',', '')
			content = line.split()	
			
			instruction = content[0]
			if instruction == 'li':
				test_load_immediate(reg_dict, content[1], content[2])
			elif instruction == 'addi':
				test_add_immediate(reg_dict, content[1], content[2])
			else:
				print('im still working on that part') 
	
	return
# testing functions ^^^



def print_RF(RF):
	for reg, value in RF.items():
		print("{} {}".format(reg, value))
	print()

def fetch(PC):
	return PC+1

def load_program_into_memory(file_name):
	all_lines = []
	all_labels = {}
	with open(file_name) as test_file:
		for line in test_file:
			if ':' in line:
				all_labels[line.replace(':\n', '')] = (len(all_lines))
				print(all_labels)
			else:
				line = line.replace(',', '')
				all_lines.append(line.split())
	return all_lines, all_labels

def decode(PC, all_ins, all_labels):
	ins = all_ins[PC][0]
	
	if ins == 'li':
		op = 1100
		func = 000
		rs = all_ins[PC][1]
		imm = all_ins[PC][2]
		rt = rd = 'X'
	elif ins == 'addi':
		op = 1000
		func = 000
		rs = all_ins[PC][1]
		imm = all_ins[PC][2]
		rt = rd = 'X'
	elif ins == 'lw':
		op = 1000
		func = 000
		rs = all_ins[PC][1]
		rt = all_ins[PC][2]
		imm = rd = 'X'
	elif ins == 'sw':
		op = 1000
		func = 000
		rs = all_ins[PC][1]
		rt = all_ins[PC][2]
		imm = rd = 'X'
	elif ins == 'j':
		op = 'please put in something here'
		func = 'please put in something here'
		rs = rt = rd = 'X'
		imm = all_labels[all_ins[PC][1]]
		
	else:
		op = 'your'
		func = 'mom'
		print('im still working on that part') 
	
	return ins, op, rs, rt, rd, imm, func

def execute(reg_dict, ins, rs, rt, rd, imm):
	if ins == 'li' or ins == 'j':
		result = imm
	elif ins == 'addi':
		result = int(reg_dict[rs]) + int(imm)
	elif ins == 'lw':
		result = int(reg_dict[rt])
	elif ins == 'sw':
		result = int(reg_dict[rs])
	#elif ins == 'j':
		#result = int(imm)
	else:
		result = 'your mom'
		print('im still working on that part') 
		
	return result

def mem(ins, rs, rt, rd):
	if (ins == 'li') or (ins == 'addi') or (ins == 'lw'):
		target = rs
	elif ins == 'sw':
		target = rt
	elif ins == 'j':
		target = 'PC'
	else:
		target = 'your_mother'
	
	return target

def write_back(reg_dict, target, result, PC):
	if target == 'PC':
		PC = result-1
	else:
		reg_dict[target] = result
	return PC



# setup
registers = dict([("$r%s" % x, 0) for x in range(4)]) 
print_RF(registers)
PC = -1
# UI setup
user_input = ''
i = 1
R = False
# read file
all_ins, label_dict = load_program_into_memory('i_type_test.s')


# run
while PC < (len(all_ins)-2):
	if not R:
		user_input = input('\n      Enter R to run program to completion. Enter any other key to step. >')
		if user_input.lower() == 'r':
			R = True
	PC = fetch(PC)
	print('\n      PC is', PC)
	ins, op, rs, rt, rd, imm, func = decode(PC, all_ins, label_dict)
	result = execute(registers, ins, rs, rt, rd, imm)
	target = mem(ins, rs, rt, rd)
	PC = write_back(registers, target, result, PC)
	
	if not R:
		print('\n      STEP', i, '\n\n     ', ins, rs, rt, rd, imm, '\n')
		i += 1
		print_RF(registers)

# for debug
#test_file(registers, 'i_type_test.s')

if(R):
	print('\n      FINAL\n')
	print_RF(registers)
