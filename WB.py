import copy

def check_z(result):
	return True if int(result) == 0 else False


def write_back(reg_dict, target, PC, M, window):
	W = copy.deepcopy(M)
	
	
	if M.ins == 'NOP':
		z = False
		v = False
		result = 'X'
		return PC, z, v, W
		
		
	result = M.result
	z, v = False, False
	if result == 'none':
		pass
	elif target == 'PC':
		PC = result-1
	else:
		max_r = 32767
		min_r = -32768
		if M.ins == 'li':
			max_r = 255
			min_r = -256
		if int(result) > max_r: 
			result = int(result) - (round(int(result)/(max_r+1))) * (max_r+1)
			z = check_z(result)
			v = True
		elif int(result) < min_r:
			result = (max_r+1) + (int(result) - (min_r))
			z = check_z(result)
			v = True
		else:
			z = check_z(result)
			v = False
		reg_dict[target] = result
  
	window['-FLAGTEXT-'].update('Flags\n' + 'Zero: ' + str(z) + '\nOverflow: ' + str(v))
	
	return PC, z, v, W
