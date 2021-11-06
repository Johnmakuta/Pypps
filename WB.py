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
		if int(result) > 32767: 
			result = int(result) - (round(int(result)/32768)) * 32768
			z = check_z(result)
			v = True
		elif int(result) < -32768:
			result = int(result) + (round(int(result)/-32769)) * 32769
			z = check_z(result)
			v = True
		else:
			z = check_z(result)
			v = False
		reg_dict[target] = result
  
	window['-FLAGTEXT-'].update('Flags\n' + 'Zero: ' + str(z) + '\nOverflow: ' + str(v))
	
	return PC, z, v, W
