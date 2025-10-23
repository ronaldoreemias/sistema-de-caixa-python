import sqlite3
import PySimpleGUI as sg
import os

def mostrar_relatorios():
    # Conectar ao banco de dados
    conn = sqlite3.connect('relatorios.db')
    c = conn.cursor()
    
    # Executar a consulta para obter todos os relatórios
    c.execute('SELECT * FROM relatorios')
    relatorios = c.fetchall()
    
    # Fechar a conexão com o banco de dados
    conn.close()
    
    # Definir o layout da janela do PySimpleGUI com uma barra de rolagem
    layout = [
        [sg.Text('ID', size=(10, 1), font=('Helvetica', 12, 'bold')),
         sg.Text('Data e Hora', size=(25, 1), font=('Helvetica', 12, 'bold')),
         sg.Text('Relatório', size=(50, 1), font=('Helvetica', 12, 'bold'))],
        [sg.Column(
            [
                [sg.Text(str(r[0]), size=(10, 1), pad=(5, 5)),
                 sg.Text(r[1], size=(25, 1), pad=(5, 5)),
                 sg.Multiline(r[2], size=(70, 10), pad=(5, 5), disabled=True, background_color='white', text_color='black')]
                for r in relatorios
            ],
            size=(900, 500), scrollable=True, vertical_scroll_only=True
        )],
        [sg.Button('Imprimir', font=('Helvetica', 12)), sg.Button('Fechar', font=('Helvetica', 12))]
    ]
    
    # Criar a janela
    window = sg.Window('Relatórios Salvos', layout)
    
    # Loop de eventos para capturar ações do usuário
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Fechar':
            break
        elif event == 'Imprimir':
            imprimir_relatorios(relatorios)
    
    # Fechar a janela
    window.close()

def imprimir_relatorios(relatorios):
    with open('relatorios.txt', 'w') as f:
        for r in relatorios:
            f.write(f'ID: {r[0]}\n')
            f.write(f'Data e Hora: {r[1]}\n')
            f.write(f'Relatório:\n{r[2]}\n')
            f.write('-' * 80 + '\n')
    
    if os.name == 'nt':
        os.startfile('relatorios.txt', 'print')
    else:
        # Comando para impressão no Linux/Mac
        os.system('lp relatorios.txt')

# Chamar a função para mostrar relatórios
mostrar_relatorios()
