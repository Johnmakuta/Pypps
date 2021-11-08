import copy

def add_1_to(dict):
    for entry in dict.items():
       dict[entry[0]] = entry[1] + 1
    return dict

def add_2_to(dict):
    for entry in dict.items():
       dict[entry[0]] = entry[1] + 2
    return dict

def flusher(PC, imm, all_lines, all_labels):
	if PC != imm:
			# debug
			#print('PC != imm', PC, imm)
			all_lines[PC][0] = 'NOP'
			if (PC+1) != imm:
				# debug
				#print('PC+1 != imm', PC+1, imm)
				all_lines[PC+1][0] = 'NOP'
			else:
				if imm > PC:
					all_lines.insert((PC), ['NOP'])
					all_labels = add_1_to(all_labels)
					imm += 1
				
	else:
		if imm > PC:
			all_lines.insert((PC), ['NOP'])
			all_lines.insert((PC), ['NOP'])	
			all_labels = add_2_to(all_labels)
			imm += 2

	
	return all_labels, imm
	
	

def execute(reg_dict, E, D, F, PC, all_labels, all_lines, memory):
	E = copy.deepcopy(D)
	
	if E.ins == 'NOP':
		E.result = 'x'
		return E, D, F, all_labels
	
	# li, j, addi, subi, sll
	if E.ins == 'li':
		E.result = E.imm
	elif E.ins == 'j':
		E.result = E.imm
		all_labels, E.result = flusher(PC, E.imm, all_lines, all_labels)	
		
		
	# inc, dec, bie
	elif E.ins == 'inc': #replaces ble
		E.result = int(reg_dict[E.rd]) + 1
	elif E.ins == 'dec': #replaces beq
		print(E.print_fields_string())
		print(all_lines)
		E.result = int(reg_dict[E.rd]) - 1
	elif E.ins == 'bie': #replaces sll
		E.result = E.imm if (int(reg_dict[E.rd]) % 2 == 0) else 'none'
		if E.result != 'none':
			all_labels, E.result = flusher(PC, E.imm, all_lines, all_labels)	
		

	elif E.ins == 'addi':
		E.result = int(reg_dict[E.rd]) + int(E.imm)
	elif E.ins == 'subi':
		E.result = int(reg_dict[E.rd]) - int(E.imm)
	elif E.ins == 'sll':
		E.result = int(reg_dict[E.rd]) << int(E.imm)
	
	# lw, sw, beq	
	elif E.ins == 'lw':
		if '(' in E.rs:
			#print('We found our Array in lw')
			#print((E.rs).split('('))
			#print((E.rs).split('(')[1][:3])
			mem_space = (E.rs).split('(')
			mem_space[1] = mem_space[1][:3]
			mem_space[1] = int(int(reg_dict[mem_space[1]]) / 2)
			E.result = memory[mem_space[0]][mem_space[1]]
		elif '$' in E.rs:
			#print(E.rs)
			#print(reg_dict[E.rs])
			E.result = int(reg_dict[E.rs])
		
	elif E.ins == 'sw':
		if '(' in E.rd:
			#print('We found our Array in sw')
			mem_space = (E.rd).split('(')
			mem_space[1] = mem_space[1][:3]
			mem_space[1] = int(int(reg_dict[mem_space[1]]) / 2)
			E.result = memory[mem_space[0]][mem_space[1]]
			#print('Memory: ')
			#print(memory[mem_space[0]][mem_space[1]])
		elif '$' in E.rd:
			#print(E.rd)
			#print(reg_dict[E.rd])
			E.result = int(reg_dict[E.rd])
		
	elif E.ins == 'beq':
		E.result = E.imm if int(reg_dict[E.rd]) == int(reg_dict[E.rs]) else 'none'
		if E.result != 'none':
			all_labels, E.result = flusher(PC, E.imm, all_lines, all_labels)	

	elif E.ins == 'ble':
		E.result = E.imm if int(reg_dict[E.rd]) <= int(reg_dict[E.rs]) else 'none'
		if E.result != 'none':
			all_labels, E.result = flusher(PC, E.imm, all_lines, all_labels)		

		
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
