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
			return '[no operation]'
			
		imm_bin = self.imm
		if (self.imm != 'U') and (self.imm != 'xxxxxxxxx'):
			try:
				temp = float(self.imm)
				#imm_bin = format(temp, '09b')
			except ValueError:
				temp = int(self.imm)
				#imm_bin = format(temp, '09b')
			if int(temp) > 0:
				imm_bin = bin(int(temp))[2:].zfill(16)
			else:
				imm_bin = bin((1<<16) + int(temp))[2:].zfill(16)

				
		return 'instruction: ' + str(self.ins) + '\n' + str(self.op) + ' ' + str(self.func) + ' ' + str(self.rd) + ' ' + str(self.rs) + ' ' + str(self.rt) + ' ' + str(imm_bin)

def print_RF_string(RF):
	string = ''
	for reg, value in RF.items():
		string += "{} {}".format(reg, value) + '\n'
	return string
