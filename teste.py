import PySimpleGUI as sg
import sqlite3

# Função para buscar relatórios e exibir resultados
def buscar_relatorio():
    sg.theme('LightGreen')  # Define um tema para a janela

    layout = [
        [sg.Text('Busca de Relatório de Compra', font=('Helvetica', 24), justification='center', text_color='green', size=(30, 1), pad=((5, 5), (10, 20)))],
        [sg.Text('Nome do Produto:', size=(25, 1), font=('Helvetica', 14)), sg.InputText(key='nome_produto', size=(30, 1))],
        [sg.Text('CPF:', size=(25, 1), font=('Helvetica', 14)), sg.InputText(key='cpf', size=(30, 1))],
        [sg.Button('Buscar', font=('Helvetica', 14), size=(15, 1)), sg.Button('Cancelar', font=('Helvetica', 14), size=(15, 1))]
    ]

    window = sg.Window('Buscar Relatório', layout, element_justification='center')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancelar'):
            break
        elif event == 'Buscar':
            nome_produto = values['nome_produto']
            cpf = values['cpf']
            conn = sqlite3.connect('relatorios.db')
            c = conn.cursor()
            c.execute('''SELECT data_hora, relatorio
                         FROM relatorios
                         WHERE relatorio LIKE ? AND relatorio LIKE ?''', (f'%{nome_produto}%', f'%{cpf}%'))
            relatorios = c.fetchall()
            conn.close()
            
            if relatorios:
                for rel in relatorios:
                    data_hora, relatorio = rel
                    sg.popup_scrolled('Relatório de Compra', relatorio, font=('Helvetica', 12), size=(60, 20))
            else:
                sg.popup('Nenhum relatório encontrado para esses critérios.')

    window.close()

# Função de consulta de pacotes
def consulta_pacote():
    layout = [
        [sg.Text('Consulta de Pacote', font=('Helvetica', 20), justification='center', text_color='green')],
        [sg.Text('Nome do Fornecedor ou Produto:', size=(25, 1)), sg.InputText(key='nome')],
        [sg.Button('Procurar', font=('Helvetica', 14), size=(15, 1)), sg.Button('Cancelar', font=('Helvetica', 14), size=(15, 1))]
    ]

    window = sg.Window('Consultar Pacote', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancelar'):
            break
        elif event == 'Procurar':
            nome = values['nome']
            conn = sqlite3.connect('relatorios.db')
            c = conn.cursor()
            c.execute('''SELECT data_hora, relatorio
                         FROM relatorios
                         WHERE relatorio LIKE ?''', (f'%{nome}%',))
            relatorios = c.fetchall()
            conn.close()
            
            if relatorios:
                result = "\n".join([f'Data e Hora: {p[0]}\nRelatório:\n{p[1]}\n' for p in relatorios])
                sg.popup_scrolled('Relatórios Encontrados', result, font=('Helvetica', 12), size=(60, 20))
            else:
                sg.popup('Nenhum relatório encontrado para este nome.')

    window.close()

# Função principal para exibir o menu
def menu_principal():
    layout = [
        [sg.Button('Buscar Relatório', font=('Helvetica', 14), size=(25, 2))],
        [sg.Button('Consultar Pacote', font=('Helvetica', 14), size=(25, 2))]
    ]

    window = sg.Window('Menu Principal', layout, element_justification='center')

    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Buscar Relatório':
            window.close()
            buscar_relatorio()
            window = sg.Window('Menu Principal', layout, element_justification='center')
        elif event == 'Consultar Pacote':
            window.close()
            consulta_pacote()
            window = sg.Window('Menu Principal', layout, element_justification='center')

    window.close()

menu_principal()
