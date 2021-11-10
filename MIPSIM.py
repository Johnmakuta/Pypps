#!/usr/bin/python
import sys
from os import path
import copy
import PySimpleGUI as sg
import FETCH
import DECODE
import EXECUTE
import MEM
import WB
import FIELDS
import LOAD

if len(sys.argv) < 2:
	print('Error. Usage: python3 MIPSIM.py filename\nExiting.')
	exit(0)
file_name_input = str(sys.argv[1])
if not path.exists(file_name_input):
	print('Error. File not found.\nExiting.')
	exit(0)

def main():
	# GUI
	s = (20, 16)
	st = (18,10)
	sw = (40, 2)
	REG_section = [[sg.Text('Registers', key='-REGTEXT-', background_color='white', size=s, text_color='black')]]
	FLAG_section = [[sg.Text('Flags\nZero: Unknown\nOverflow: Unknown', key='-FLAGTEXT-', background_color='white', size=st, text_color='black')]]
	F_section = [[sg.Text('Fetch', key='-FTEXT-', background_color='white', size=sw, text_color='black')]]
	D_section = [[sg.Text('Decode', key='-DTEXT-', background_color='white', size=sw, text_color='black')]]
	E_section = [[sg.Text('Execute', key='-ETEXT-', background_color='white', size=sw, text_color='black')]]
	M_section = [[sg.Text('Memory', key='-MTEXT-', background_color='white', size=sw, text_color='black')]]
	W_section = [[sg.Text('Write back', key='-WTEXT-', background_color='white', size=sw, text_color='black')]]
	MEMORY_section = [[sg.Text('Memory', key='-MEMORYTEXT-', background_color='white', size=s, text_color='black')]]
	
	layout = [[[sg.Text('Clock control')], [sg.Button('Mini step'), sg.Button('Step'), 
			sg.Button('Run'), sg.Button('Restart'), sg.VerticalSeparator(), sg.Column(REG_section, element_justification = 'c'), sg.Column(MEMORY_section, element_justification = 'c'), sg.Column(FLAG_section, element_justification = 'c')],
			[sg.Column(F_section, element_justification = 'c')], [sg.Column(D_section, element_justification = 'c')], [sg.Column(E_section, element_justification = 'c')],
			[sg.Column(M_section, element_justification = 'c')], [sg.Column(W_section, element_justification = 'c')], sg.Text('Clock cycle: 0, PC: 0', key='-STEP-'), sg.Text('', key='-FINISHED-')]]
	
	window = sg.Window('MIPSIM', layout, size=(950, 650), location=(100,330))
	
	def ask_window(R, RS, SO, window, reg_dict):
		while True:
			GUI_event, values = window.read()
			if R:
				return R, SO, GUI_event
			if GUI_event == "Restart":
				RS = True
				return R, RS, SO, GUI_event
			if GUI_event == "Run":
				R = True
				break
			elif GUI_event == "Mini step":
				break
			elif GUI_event == "Step":
				SO = True
				break
			elif GUI_event == sg.WIN_CLOSED:
				exit(0)
		
		update_window(window, reg_dict)
		
		return R, RS, SO, GUI_event
		
	def update_window(window, reg_dict):
		window['-REGTEXT-'].update('Registers\n' + FIELDS.print_RF_string(reg_dict))
		window['-FTEXT-'].update('Fetch\n' + F.print_fields_string(reg_dict))
		window['-DTEXT-'].update('Decode\n' + D.print_fields_string(reg_dict))
		window['-ETEXT-'].update('Execute\n' + E.print_fields_string(reg_dict))
		window['-MTEXT-'].update('Memory\n' + M.print_fields_string(reg_dict))
		window['-WTEXT-'].update('Write back\n' + W.print_fields_string(reg_dict))
		window['-MEMORYTEXT-'].update('Memory\n' + FIELDS.print_RF_string(memory))
		
	
	def reset_text(window):
		window['-REGTEXT-'].update('Registers\n')
		window['-STEP-'].update('Clock cycle: 0, PC: 0')
		window['-FINISHED-'].update('')
		window['-FLAGTEXT-'].update('Flags\nZero: Unknown\nOverflow: Unknown')
		window['-FTEXT-'].update('Fetch\n')
		window['-DTEXT-'].update('Decode\n')
		window['-ETEXT-'].update('Execute\n')
		window['-MTEXT-'].update('Memory\n')
		window['-WTEXT-'].update('Write back')
		window['-MEMORYTEXT-'].update('Memory')
		
	while True:
		# setup
		REG_NUM, PC, i = 8, -1, 1
		reg_dict = dict([("$r%s" % x, 0) for x in range(REG_NUM)]) 
		F, D, E, M, W=FIELDS.fields(), FIELDS.fields(), FIELDS.fields(), FIELDS.fields(), FIELDS.fields()
		user_input = ''
		z, v, R, SO, RS = (False,)*5
		#LOAD
		all_lines, all_labels, memory = LOAD.load_program_into_memory(file_name_input)	
		if len(all_lines) == 0:
			exit(0)
		
		# RUN
		while PC < (len(all_lines)-1):
			
			lines_left = (len(all_lines)-1) - PC

			if not SO and not R:
				R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
				if RS:
					reset_text(window)
					RS = False
					break
			
			window['-STEP-'].update('Clock cycle: ' + str(i-1) + ', PC: ' + str(hex((PC+1)*2)) + ' ' + str(PC))
			
			#1
			#FETCH
			PC, F = FETCH.fetch(PC, all_lines, F)
	
			if not SO and not R:
				R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
				if RS:
					reset_text(window)
					RS = False
					break
			
			
			#2
			#Decode
			D = DECODE.decode(PC, all_lines, all_labels, F)
			if lines_left > 1:
				PC, F = FETCH.fetch(PC, all_lines, F)	
	
			if not SO and not R:
				R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
				if RS:
					reset_text(window)
					RS = False
					break
			
	
	
			#3
			#Execution
			E, D, F, all_labels = EXECUTE.execute(reg_dict, E, D, F, PC, all_labels, all_lines, memory, 'none', 'none')
			if lines_left > 1:
				D = DECODE.decode(PC, all_lines, all_labels, F)
			if lines_left > 2:
				PC, F = FETCH.fetch(PC, all_lines, F)
	
			if not SO and not R:
				R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
				if RS:
					reset_text(window)
					RS = False
					break
			
	
	
			#4
			target, M, forward_result, F, D, all_lines = MEM.mem(E, F, D, all_lines, PC)
			if lines_left > 1:
				E, D, F, all_labels = EXECUTE.execute(reg_dict, E, D, F, PC, all_labels, all_lines, memory, forward_result, M)
			if lines_left > 2:
				D = DECODE.decode(PC, all_lines, all_labels, F)
			if lines_left > 3:
				PC, F = FETCH.fetch(PC, all_lines, F)
	
			if not SO and not R:
				R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
				if RS:
					reset_text(window)
					RS = False
					break
			
	
	
			#5
			PC, z, v, W = WB.write_back(reg_dict, memory, target, PC, M, window)
			if lines_left > 1:
				target, M, forward_result, F, D, all_lines = MEM.mem(E, F, D, all_lines, PC)
			if lines_left > 2:
				E, D, F, all_labels = EXECUTE.execute(reg_dict, E, D, F, PC, all_labels, all_lines, memory, forward_result, M)
			if lines_left > 3:
				D = DECODE.decode(PC, all_lines, all_labels, F)
	
			if not SO and not R:
				R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
				if RS:
					reset_text(window)
					RS = False
					break
			
	
	
			#6
			if lines_left > 1:
				PC, z, v, W = WB.write_back(reg_dict, memory, target, PC, M, window)
			if lines_left > 2:	
				target, M, forward_result, F, D, all_lines = MEM.mem(E, F, D, all_lines, PC)
			if lines_left > 3:	
				E, D, F, all_labels = EXECUTE.execute(reg_dict, E, D, F, PC, all_labels, all_lines, memory, forward_result, M)
	
			if not SO and not R and not (PC >= len(all_lines)-1):
				R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
				if RS:
					reset_text(window)
					RS = False
					break
				
	
	
			#7
			if lines_left > 2:
				PC, z, v, W = WB.write_back(reg_dict, memory, target, PC, M, window)
			if lines_left > 3:
				target, M, forward_result, F, D, all_lines = MEM.mem(E, F, D, all_lines, PC)
	
			if not SO and not R and not (PC >= len(all_lines)-1):
				R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
				if RS:
					reset_text(window)
					RS = False
					break
			
	
	
			#8
			if lines_left > 3:
				PC, z, v, W = WB.write_back(reg_dict, memory, target, PC, M, window)
	
			if not SO and not R and not (PC >= len(all_lines)-1):
				R, RS, SO, GUI_event = ask_window(R, RS, SO, window, reg_dict)
				if RS:
					reset_text(window)
					RS = False
					break
			
			i += 1
				
			SO = False
			
		if R or SO or (PC >= len(all_lines)-1):
			update_window(window, reg_dict)
			window['-FLAGTEXT-'].update('Flags\n' + 'Zero: ' + str(z) + '\nOverflow: ' + str(v))
			window['-FINISHED-'].update('File finished running.')
			window.find_element('Mini step').Update(disabled=True)
			window.find_element('Step').Update(disabled=True)
			window.find_element('Run').Update(disabled=True)
			while True:
				GUI_event, values = window.read()
				if GUI_event == sg.WIN_CLOSED:
					exit(0)
				elif GUI_event == "Restart":
					reset_text(window)
					window.find_element('Mini step').Update(disabled=False)
					window.find_element('Step').Update(disabled=False)
					window.find_element('Run').Update(disabled=False)
					break
				
	exit(0)
	
if __name__ == "__main__":
    main()
	
