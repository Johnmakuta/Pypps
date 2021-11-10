class fields:
	def __init__(self):
		self.ins = 'U'
		self.op = '0000'
		self.func = '000'
		self.rd = '000'
		self.rs = '000'
		self.rt = '000'
		self.imm = '000000000'
		self.result = 'U'
		
		
		
	def print_fields_string(self, reg_dict):
		if self.ins == 'U':
			return ''
		if self.ins == 'NOP':
			#return '[no operation]'
			return '0000 000 000 000 000000 000'
			
		imm_bin = self.imm
		temp = 'none'
		if (self.imm != 'U') and (self.imm != 'xxxxxxxxx'):
			try:
				temp = float(self.imm)
			except ValueError:
				temp = int(self.imm)
			if temp != 'none':
				if self.ins == 'li':
					fill = 9
				else:
					fill = 6
				imm_bin = bin(int(temp))[2:].zfill(fill)
			else:
				imm_bin = bin((1<<fill) + int(temp))[2:].zfill(fill)
				
				
		else:
			self.imm = '000000000'

		try:
			rd_reg_num = list(reg_dict.keys()).index(self.rd)
			rd_reg_num = str(bin(rd_reg_num)[2:].zfill(3))
		except ValueError:
			rd_reg_num = '000'
		
		try:
			rs_reg_num = list(reg_dict.keys()).index(self.rs)
			rs_reg_num = str(bin(rs_reg_num)[2:].zfill(3))
		except ValueError:
			rs_reg_num = '000'
			
		try:
			rt_reg_num = list(reg_dict.keys()).index(self.rt)
			rt_reg_num = str(bin(rt_reg_num)[2:].zfill(3))
		except ValueError:
			rt_reg_num = '000'

		if '(' in self.rs:
			rs_reg_num = self.rs
			dummy_dummy = rs_reg_num.replace('(',' ').replace(')','').split()
			rs_reg_num = dummy_dummy[1]
			rs_reg_num = list(reg_dict.keys()).index(rs_reg_num)
			rs_reg_num = str(bin(rs_reg_num)[2:].zfill(3))
		
		if self.ins == 'li':
			imm_bin = str(imm_bin)
			return str(self.op) + ' ' + rd_reg_num + ' ' + rs_reg_num + ' ' + str(imm_bin[0]) + str(imm_bin[1]) + str(imm_bin[2]) + ' ' + str(imm_bin[3]) + str(imm_bin[4]) + str(imm_bin[5]) + str(imm_bin[6]) + str(imm_bin[7]) + str(imm_bin[8]) + ' ' + str(self.func)
		
		return str(self.op) + ' ' + rd_reg_num + ' ' + rs_reg_num + ' ' + rt_reg_num + ' ' + str(imm_bin) + ' ' + str(self.func)



def print_RF_string(reg_dict):
	string = ''
	for reg, value in reg_dict.items():
		string += "{} {}".format(reg, value) + '\n'
	return string
