import copy

def flusher(PC, imm, all_lines, all_labels):
	if PC != imm:
		all_lines[PC][0] = 'NOP'
		if (PC+1) != imm:
			all_lines[PC+1][0] = 'NOP'

	
	return all_labels, imm
	

def HDU(E, M, forward_result_M, reg_dict):
	try:
		rdb = int(reg_dict[E.rd])
	except KeyError:
		rdb = 'none'
	
	try:
		rsb = int(reg_dict[E.rs])
	except KeyError:
		rsb = 'none'
		
	try:
		rtb = int(reg_dict[E.rt])
	except KeyError:
		rtb = 'none'
	
	if M != 'none' and forward_result_M != 'x':
		if (E.rd == M.rd) and E.rd != 'x':
			rdb = int(forward_result_M)
		if (E.rs == M.rd) and E.rs != 'x':
			rsb = int(forward_result_M)
		if (E.rt == M.rd) and E.rt != 'x':
			rtb = int(forward_result_M)
		
	return rdb, rsb, rtb

def execute(reg_dict, E, D, F, PC, all_labels, all_lines, memory, forward_result_M, M):
	E = copy.deepcopy(D)
	
	

	rdb, rsb, rtb = HDU(E, M, forward_result_M, reg_dict)
	
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
		E.result = rdb + 1
	elif E.ins == 'dec': #replaces beq
		E.result = rdb - 1
	elif E.ins == 'bie': #replaces sll
		E.result = E.imm if (rdb % 2 == 0) else 'none'
		
		if E.result != 'none':
			all_labels, E.result = flusher(PC, E.imm, all_lines, all_labels)	
		

	elif E.ins == 'addi':
		E.result = rdb + int(E.imm)
	elif E.ins == 'subi':
		E.result = rdb - int(E.imm)
	elif E.ins == 'sll':
		E.result = rdb << int(E.imm)
	
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
			E.result = rsb
		
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
			E.result = rdb
		
	elif E.ins == 'beq':
		E.result = E.imm if rdb == rsb else 'none'
		if E.result != 'none':
			all_labels, E.result = flusher(PC, E.imm, all_lines, all_labels)	

	elif E.ins == 'ble':
		E.result = E.imm if rdb <= rsb else 'none'
		if E.result != 'none':
			all_labels, E.result = flusher(PC, E.imm, all_lines, all_labels)		

		
	# or, xor, slt, add, div, mul
	elif E.ins == 'or':
		E.result = rsb or rtb
		
	elif E.ins == 'xor':
		E.result = rsb ^ rtb
		
	elif E.ins == 'slt':
		E.result = 1 if rsb < rtb else 0
		
	elif E.ins == 'add':
		E.result = rsb + rtb
			
	elif E.ins == 'mul':
		E.result = rsb * rtb
			
	elif E.ins == 'div':
		E.result = rsb / rtb
	
	else:
		result = 'U'
		
	return E, D, F, all_labels
