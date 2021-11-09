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
			size = round(int(int(line[i][2]))/2)
			memory[line[i][0]] = list(0  for n in range(size))

		elif not data_mode:
			all_lines.append(line[i])

	if not len(line):
		print('File is empty.')
		exit(0)


	if not any(':' in word for word in line[i]) and not data_mode:
		all_lines.append(line[i])
		
	print('\n', all_lines)
	return all_lines, all_labels, memory
