import copy

def add_1_to(dict):
    for entry in dict.items():
       dict[entry[0]] = entry[1] + 1
    return dict

def add_2_to(dict):
    for entry in dict.items():
       dict[entry[0]] = entry[1] + 2
    return dict

def insert(PC, imm, all_lines, all_labels):
	if PC != imm:
			print('PC != imm', PC, imm)
			all_lines[PC][0] = 'NOP'
			if (PC+1) != imm:
				print('PC+1 != imm', PC+1, imm)
				all_lines[PC+1][0] = 'NOP'
			else:
				all_lines.insert((PC), ['NOP'])
				all_labels = add_1_to(all_labels)
				imm += 1
				
	else:
		all_lines.insert((PC), ['NOP'])
		all_lines.insert((PC), ['NOP'])	
		all_labels = add_2_to(all_labels)
		imm += 2
	
	return all_labels, imm

def execute(reg_dict, E, D, F, PC, all_labels, all_lines):
	E = copy.deepcopy(D)
	#print(E.ins)
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
