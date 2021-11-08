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
	def print_fields_string(self, reg_dict):
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

		try:
			rd_reg_num = list(reg_dict.keys()).index(self.rd)
			rd_reg_num = str(bin(rd_reg_num)[2:].zfill(3))
		except ValueError:
			rd_reg_num = 'xxx'
		
		try:
			rs_reg_num = list(reg_dict.keys()).index(self.rs)
			rs_reg_num = str(bin(rs_reg_num)[2:].zfill(3))
		except ValueError:
			rs_reg_num = 'xxx'
			
		try:
			rt_reg_num = list(reg_dict.keys()).index(self.rt)
			rt_reg_num = str(bin(rt_reg_num)[2:].zfill(3))
		except ValueError:
			rt_reg_num = 'xxx'
		
		return 'instruction: ' + '\n' + str(self.op) + ' ' + str(self.func) + ' ' + rd_reg_num + ' ' + rs_reg_num + ' ' + rt_reg_num + ' ' + str(imm_bin)

def print_RF_string(reg_dict):
	string = ''
	for reg, value in reg_dict.items():
		string += "{} {}".format(reg, value) + '\n'
	return string
