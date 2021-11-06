import copy

def load_program_into_memory(file_name):
	all_lines, line, dummy_line = [], [], []
	all_labels, memory = {}, {}
	H, data_mode = False, False
	target = '#'
	with open(file_name) as test_file:
		for file_line in test_file:
			if file_line.startswith('#') or file_line.startswith(';') or file_line == '\n' or file_line == '':
				pass
			else:
				file_line = file_line.replace(',', '')
				file_line = file_line.split(';', 1)[0]
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

	if not len(line):
		print('File is empty.')
		exit(0)


	if not any(':' in word for word in line[i]) and not data_mode:
		all_lines.append(line[i])
		
	#print(memory)
	print(all_lines)
	#exit(0)
	return all_lines, all_labels, memory
