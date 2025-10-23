import PySimpleGUI as sg

layout = [
    [sg.Text('Tela de Menu do Sistema', size=(40, 1), justification='center', font=('Helvetica', 20), text_color='white', background_color='#2B2B2B')],
    [sg.Column([
        [sg.Button('Cadastrar cliente', size=(20, 2), key='Cadastrar cliente'), sg.Button('Consulta de cliente', size=(20, 2), key='Consulta de cliente')],
        [sg.Button('Adicionar dependente', size=(20, 2), key='Adicionar dependente'), sg.Button('Marcar aula', size=(20, 2), key='Marcar aula')],
        [sg.Button('Sair', size=(20, 2), key='Sair')]
    ], justification='center')]
]

window = sg.Window('Menu Principal', layout, size=(500, 300), element_justification='center')

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Sair'):
        break

window.close()
