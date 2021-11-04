import copy
import PySimpleGUI as sg

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

def print_RF_string(RF):
	string = ''
	for reg, value in RF.items():
		string += "{} {}".format(reg, value) + '\n'
	return string


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
						all_lines.append(['NOP'])
						all_lines.append(['NOP'])
						all_lines.append(line)
					else:
						all_lines.append(line)
				elif (len(line) > 2) and (len(all_lines) > 0):
					if line[1] in all_lines[len(all_lines)-1] or line[2] in all_lines[len(all_lines)-1]:
						all_lines.append(['NOP'])
						all_lines.append(['NOP'])
						all_lines.append(line)
					else:
						all_lines.append(line)
				else:
					all_lines.append(line)
					all_lines.append(['NOP'])
					all_lines.append(['NOP'])
					all_lines.append(['NOP'])
					
				if (line[0] == 'beq') or (line[0] == 'ble'):
					all_lines.append(['NOP'])
					all_lines.append(['NOP'])
					all_lines.append(['NOP'])
				
					
	#print(all_lines)
	return all_lines, all_labels

def fetch(PC, all_lines, F):
	PC += 1
	F.ins = all_lines[PC][0]
	if F.ins == 'NOP':
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
	if D.ins == 'NOP':
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
	if E.ins == 'NOP':
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
	if M.ins == 'NOP':
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
	if M.ins == 'NOP':
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



def print_all_lines(line_to_print):
	string = ''
	print('\n      ')
	for word in line_to_print:
		string = string + word + ' '
	print(string)



# setup
reg_dict = dict([("$r%s" % x, 0) for x in range(4)]) 
#print_RF(reg_dict)
PC = -1
F = fields()
D = fields()
E = fields()
M = fields()
user_input = ''
i = 1
z = v = R = False
all_lines, all_labels = load_program_into_memory('test.s')


# GUI
#sg.theme('DarkTanBlue')
REG_section = [[sg.Text('Registers', key='-REGTEXT-', background_color='white', size=(100,100), text_color='black')]]
FLAG_section = [[sg.Text('Flags', key='-FLAGTEXT-', background_color='white', size=(100,50), text_color='black')]]

layout = [[[sg.Text('Clock control')], 
		[sg.Button('Step'), 
		sg.Button('Run'), 
		sg.VerticalSeparator(), 
		sg.Column(REG_section, element_justification='c'),
		sg.VerticalSeparator(), 
		sg.Column(FLAG_section, element_justification='c')]]]
		
window = sg.Window('MIPSIM', layout,size=(400, 400), location=(600,330))





# RUN
while PC < (len(all_lines)-2):
	while True:
		if R:
			break
		GUI_event, values = window.read()
		if GUI_event == "Run":
			R = True
			break
		elif GUI_event == "Step":
			break
		elif GUI_event == sg.WIN_CLOSED:
			exit(0)
	
	lines_left = (len(all_lines)-1) - PC
	
	#1
	PC, F = fetch(PC, all_lines, F)

	
	#2
	D = decode(PC, all_lines, all_labels, F)
	PC, F = fetch(PC, all_lines, F)	
	
	#3
	
	E = execute(reg_dict, D)
	D = decode(PC, all_lines, all_labels, F)
	PC, F = fetch(PC, all_lines, F)
	
	#4
	target, M = mem(E)
	E = execute(reg_dict, D)
	D = decode(PC, all_lines, all_labels, F)
	PC, F = fetch(PC, all_lines, F)
	
	#5
	PC, z, v = write_back(reg_dict, target, PC, M)
	target, M = mem(E)
	E = execute(reg_dict, D)
	D = decode(PC, all_lines, all_labels, F)
	
	#6
	PC, z, v = write_back(reg_dict, target, PC, M)
	target, M = mem(E)
	E = execute(reg_dict, D)
		
	#7
	PC, z, v = write_back(reg_dict, target, PC, M)
	target, M = mem(E)
	
	#8
	PC, z, v = write_back(reg_dict, target, PC, M)
	
	
	if not R:
		#print('\n      PC is', PC)
		#print('\n      STEP', i, '\n') 
		#all_print_fields(F, D, E, M)
		#print_all_lines(all_lines[PC])
		#print_all_lines(all_lines[PC+1])
		#print_all_lines(all_lines[PC+2])
		#print_all_lines(all_lines[PC+3])
		window['-REGTEXT-'].update('Registers\n' + print_RF_string(reg_dict))
		window['-FLAGTEXT-'].update('Flags\n' + 'Zero:' + str(z) + '\nOverflow:' + str(v))
		#print('Zero:', z, '\nOverflow:', v)
	
	i += 1

#print()

if R:
	#print('\n      FINAL\n')
	#print_RF(reg_dict)
	window['-REGTEXT-'].update('Registers\n' + print_RF_string(reg_dict))
	window['-FLAGTEXT-'].update('Flags\n' + 'Zero:' + str(z) + '\nOverflow:' + str(v))
	#print('Zero:', z, '\nOverflow:', v, '\n')
	while True:
		GUI_event, values = window.read()
		if GUI_event == sg.WIN_CLOSED:
			break
	
exit(0)
