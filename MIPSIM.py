#!/usr/bin/python
import sys
from os import path
import copy
import PySimpleGUI as sg

if len(sys.argv) < 2:
	print('Error. Usage: python3 MIPSIM.py filename\nExiting.')
	exit(0)
file_name_input = str(sys.argv[1])
if not path.exists(file_name_input):
	print('Error. File not found.\nExiting.')
	exit(0)

class fields:
	def __init__(self):
		self.ins = 'U'
		self.op = 'U'
		self.func = 'U'
		self.rd = 'U'
		self.rs = 'U'
		self.rt = 'U'
		self.imm = 'U'
		self.result = 'U'
	def print_fields_string(self):
		if self.ins == 'U':
			return ''
		if self.ins == 'NOP':
			return '(NO OPERATION)'
		return 'instruction: ' + str(self.ins) + '\n' + str(self.op) + ' ' + str(self.func) + ' ' + str(self.rd) + ' ' + str(self.rs) + ' ' + str(self.rt) + ' ' + str(self.imm)

def print_RF_string(RF):
	string = ''
	for reg, value in RF.items():
		string += "{} {}".format(reg, value) + '\n'
	return string


def load_program_into_memory(file_name):
	all_lines, line, dummy_line = [], [], []
	all_labels, memory = {}, {}
	H, data_mode = False, False
	with open(file_name) as test_file:
		for file_line in test_file:
			if file_line.startswith('#') or file_line == '\n' or file_line == '':
				pass
			else:
				file_line = file_line.replace(',', '')
				file_line = file_line.split()
				line.append(file_line)
			



	for i in range(len(line)):
		if any('.data' in word for word in line[i]):
			data_mode = True
			continue
		elif any('.text' in word for word in line[i]):
			data_mode = False
			continue

		elif any(':' in word for word in line[i]) and not data_mode:
			all_labels[line[i][0].replace(':', '')] = (len(all_lines))
		elif data_mode:
			#print(line[i])
			#print(int(int(line[i][2]))/2)
			size = round(int(int(line[i][2]))/2)
			memory[line[i][0]] = list(0  for n in range(size))

		elif not data_mode:
			if not i+1 > len(line)-1:
				for j in range(1, len(line[i])):
					dummy_line = copy.deepcopy(line[i+1])
					if len(dummy_line) > 1:
						dummy_line.pop(1)
					if any(word in line[i][j] for word in line[i+1]) and not line[i][0] == 'j':
						H = True

				if H:
					all_lines.append(line[i])
					all_lines.append(['NOP'])
					all_lines.append(['NOP'])
					all_lines.append(['NOP'])
					H = False
				else:
					all_lines.append(line[i])




	if not any(':' in word for word in line[i]) and not data_mode:
		all_lines.append(line[i])
	#print(memory)
	print(all_lines)
	#exit(0)
	return all_lines, all_labels, memory

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
	
	return D


def add_1_to(dict):
    for entry in dict.items():
       dict[entry[0]] = entry[1] + 1
    return dict

def add_2_to(dict):
    for entry in dict.items():
       dict[entry[0]] = entry[1] + 2
    return dict

def insert(PC, imm, all_lines, all_labels):
	NN = False
	for j in range(1, len(all_lines[PC])):
		dummy_line = copy.deepcopy(all_lines[imm])
		if len(dummy_line) > 1:
			dummy_line.pop(1)
		if any(word in all_lines[PC][j] for word in dummy_line):
			NN = True
	if PC != imm:
		all_lines[PC][0] = 'NOP'
		if (PC+1) != imm:
			all_lines[PC+1][0] = 'NOP'
		else:
			if NN:
				all_lines.insert((PC), ['NOP'])
				all_labels = add_1_to(all_labels)
	else:
		if NN:
			all_lines.insert((PC), ['NOP'])
			all_lines.insert((PC), ['NOP'])
			all_labels = add_2_to(all_labels)    



	
	return all_labels, imm

def execute(reg_dict, E, D, F, PC, all_labels):
	E = copy.deepcopy(D)
	print(E.ins)
	if E.ins == 'NOP':
		#print('here', E.ins)
		E.result = 'X'
		return E, D, F, all_labels
	# li, j, addi, subi, sll
	if E.ins == 'li':
		E.result = E.imm
	elif E.ins == 'j':
		E.result = E.imm
		all_labels, E.result = insert(PC, E.imm, all_lines, all_labels)	
			
		
		

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
		if E.result != 'none':
			all_labels, E.result = insert(PC, E.imm, all_lines, all_labels)	

	elif E.ins == 'ble':
		E.result = E.imm if int(reg_dict[E.rd]) <= int(reg_dict[E.rs]) else 'none'
		if E.result != 'none':
			all_labels, E.result = insert(PC, E.imm, all_lines, all_labels)		

		
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
		
	return E, D, F, all_labels




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




def write_back(reg_dict, target, PC, M, window):
	# note to pj: test flags
	W = copy.deepcopy(M)
	if M.ins == 'NOP':
		z = False
		v = False
		result = 'X'
		return PC, z, v, W
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
  
	window['-FLAGTEXT-'].update('Flags\n' + 'Zero: ' + str(z) + '\nOverflow: ' + str(v))
	
	return PC, z, v, W

# GUI
#sg.theme('DarkTanBlue')
s = (20, 10)
st = (18,10)
sw = (24, 4)
REG_section = [[sg.Text('Registers', key='-REGTEXT-', background_color='white', size=s, text_color='black')]]
FLAG_section = [[sg.Text('Flags\nZero: Unknown\nOverflow: Unknown', key='-FLAGTEXT-', background_color='white', size=st, text_color='black')]]
F_section = [[sg.Text('Fetch', key='-FTEXT-', background_color='white', size=sw, text_color='black')]]
D_section = [[sg.Text('Decode', key='-DTEXT-', background_color='white', size=sw, text_color='black')]]
E_section = [[sg.Text('Execute', key='-ETEXT-', background_color='white', size=sw, text_color='black')]]
M_section = [[sg.Text('Memory', key='-MTEXT-', background_color='white', size=sw, text_color='black')]]
W_section = [[sg.Text('Write back', key='-WTEXT-', background_color='white', size=sw, text_color='black')]]

layout = [[[sg.Text('Clock control')], [sg.Button('Mini step'), sg.Button('Step'), 
		sg.Button('Run'), sg.Button('Restart'), sg.VerticalSeparator(), sg.Column(REG_section, element_justification = 'c'), sg.Column(FLAG_section, element_justification = 'c'),
		sg.Column(F_section, element_justification = 'c'), sg.Column(D_section, element_justification = 'c'), sg.Column(E_section, element_justification = 'c'),
		sg.Column(M_section, element_justification = 'c'), sg.Column(W_section, element_justification = 'c')], sg.Text('STEP: 0', key='-STEP-'), sg.Text('', key='-FINISHED-')]]

window = sg.Window('MIPSIM', layout, size=(1600, 300), location=(300,330))

def ask_window(R, RS, SO, window, reg_dict):
	while True:
		GUI_event, values = window.read()
		if R:
			return R, SO, GUI_event
		if GUI_event == "Restart":
			RS = True
			return R, RS, SO, GUI_event
		if GUI_event == "Run":
			R = True
			break
		elif GUI_event == "Mini step":
			break
		elif GUI_event == "Step":
			SO = True
			break
		elif GUI_event == sg.WIN_CLOSED:
			exit(0)
	
	update_window(window, reg_dict)
	
	return R, RS, SO, GUI_event
	
def update_window(window, reg_dict):
	window['-REGTEXT-'].update('Registers\n' + print_RF_string(reg_dict))
	window['-FTEXT-'].update('Fetch\n' + F.print_fields_string())
	window['-DTEXT-'].update('Decode\n' + D.print_fields_string())
	window['-ETEXT-'].update('Execute\n' + E.print_fields_string())
	window['-MTEXT-'].update('Memory\n' + M.print_fields_string())
	window['-WTEXT-'].update('Write back\n' + W.print_fields_string())

def reset_text(window):
	window['-REGTEXT-'].update('Registers\n')
	window['-STEP-'].update('STEP: 0')
	window['-FINISHED-'].update('')
	window['-FLAGTEXT-'].update('Flags\nZero: Unknown\nOverflow: Unknown')
	window['-FTEXT-'].update('Fetch\n')
	window['-DTEXT-'].update('Decode\n')
	window['-ETEXT-'].update('Execute\n')
	window['-MTEXT-'].update('Memory\n')
	window['-WTEXT-'].update('Write back')
	
while True:
	# setup
	REG_NUM, PC, i = 8, -1, 1
	reg_dict = dict([("$r%s" % x, 0) for x in range(REG_NUM)]) 
	F, D, E, M, W = (fields(),)*5
	user_input = ''
	z, v, R, SO, RS = (False,)*5
	all_lines, all_labels, memory = load_program_into_memory(file_name_input)
	if len(all_lines) == 0:
		exit(0)
	
	# RUN
	while PC < (len(all_lines)-1):
		
		lines_left = (len(all_lines)-1) - PC
		
		#print('here')
		if not SO and not R:
			R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
			if RS:
				reset_text(window)
				RS = False
				break
		
		window['-STEP-'].update('STEP: ' + str(i))
		
		#1
		PC, F = fetch(PC, all_lines, F)

		if not SO and not R:
			R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
			if RS:
				reset_text(window)
				RS = False
				break
		


		#2
		D = decode(PC, all_lines, all_labels, F)
		if lines_left > 1:
			PC, F = fetch(PC, all_lines, F)	

		if not SO and not R:
			R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
			if RS:
				reset_text(window)
				RS = False
				break
		


		#3
		E, D, F, all_labels = execute(reg_dict, E, D, F, PC, all_labels)
		if lines_left > 1:
			D = decode(PC, all_lines, all_labels, F)
		if lines_left > 2:
			PC, F = fetch(PC, all_lines, F)

		if not SO and not R:
			R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
			if RS:
				reset_text(window)
				RS = False
				break
		


		#4
		target, M = mem(E)
		if lines_left > 1:
			E, D, F, all_labels = execute(reg_dict, E, D, F, PC, all_labels)
		if lines_left > 2:
			D = decode(PC, all_lines, all_labels, F)
		if lines_left > 3:
			PC, F = fetch(PC, all_lines, F)

		if not SO and not R:
			R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
			if RS:
				reset_text(window)
				RS = False
				break
		


		#5
		PC, z, v, W = write_back(reg_dict, target, PC, M, window)
		if lines_left > 1:
			target, M = mem(E)
		if lines_left > 2:
			E, D, F, all_labels = execute(reg_dict, E, D, F, PC, all_labels)
		if lines_left > 3:
			D = decode(PC, all_lines, all_labels, F)

		if not SO and not R:
			R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
			if RS:
				reset_text(window)
				RS = False
				break
		


		#6
		if lines_left > 1:
			PC, z, v, W = write_back(reg_dict, target, PC, M, window)
		if lines_left > 2:	
			target, M = mem(E)
		if lines_left > 3:	
			E, D, F, all_labels = execute(reg_dict, E, D, F, PC, all_labels)

		if not SO and not R:
			R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
			if RS:
				reset_text(window)
				RS = False
				break
			


		#7
		if lines_left > 2:
			PC, z, v, W = write_back(reg_dict, target, PC, M, window)
		if lines_left > 3:
			target, M = mem(E)

		if not SO and not R:
			R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
			if RS:
				reset_text(window)
				RS = False
				break
		


		#8
		if lines_left > 3:
			PC, z, v, W = write_back(reg_dict, target, PC, M, window)

		if not SO and not R:
			R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
			if RS:
				reset_text(window)
				RS = False
				break
		
		i += 1
			
		SO = False
		
	if R or SO or (PC >= len(all_lines)-1):
		update_window(window, reg_dict)
		window['-FLAGTEXT-'].update('Flags\n' + 'Zero: ' + str(z) + '\nOverflow: ' + str(v))
		window['-FINISHED-'].update('File finished running.')
		window.find_element('Mini step').Update(disabled=True)
		window.find_element('Step').Update(disabled=True)
		window.find_element('Run').Update(disabled=True)
		while True:
			GUI_event, values = window.read()
			if GUI_event == sg.WIN_CLOSED:
				print(all_lines)
				exit(0)
			elif GUI_event == "Restart":
				reset_text(window)
				window.find_element('Mini step').Update(disabled=False)
				window.find_element('Step').Update(disabled=False)
				window.find_element('Run').Update(disabled=False)
				break
			
exit(0)
