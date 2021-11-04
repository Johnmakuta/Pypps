import PySimpleGUI as sg

s = (20, 10)
REG_section = [[sg.Text('Registers', key='-REGTEXT-', background_color='white', size=s, text_color='black')]]
FLAG_section = [[sg.Text('Flags', key='-FLAGTEXT-', background_color='white', size=s, text_color='black')]]

layout = [[[sg.Text('Clock control')], sg.Button('Step'), 
		sg.Button('Run'), sg.VerticalSeparator(), sg.Column(REG_section, element_justification = 'c'), sg.Column(FLAG_section, element_justification = 'c')]]

window = sg.Window('MIPSIM', layout, size=(400, 400), location=(600,330))
event, values = window.read()

window.close()
