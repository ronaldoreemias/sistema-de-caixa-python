import PySimpleGUI as sg
import sqlite3
import hashlib
import re

def abrir_menu1():
    sg.theme('LightGreen')

    layout = [
        [sg.Text('Controle de Entrega de Pacotes', font=('Helvetica', 24), justification='center', pad=(0, 10), expand_x=True, text_color='green')],
        [sg.Column([
            [sg.Button('Cadastrar Fornecedor', key='Cadastrar fornecedor', font=('Helvetica', 16), size=(25, 2), button_color=('white', 'green'), pad=(10, 10)),
             sg.Button('Procurar venda feita', key='Procurar venda feita', font=('Helvetica', 16), size=(25, 2), button_color=('white', 'green'), pad=(10, 10))]
        ], justification='center')],
        [sg.Column([
            [sg.Button('Confirmar Entrega', key='Confirmar entrega', font=('Helvetica', 16), size=(25, 2), button_color=('white', 'green'), pad=(10, 10)),
             sg.Button('Cadastrar Avaria Pacote', key='Cadastrar avaria pacote', font=('Helvetica', 16), size=(25, 2), button_color=('white', 'green'), pad=(10, 10))],
        ], justification='center')],
        [sg.Button('Voltar para o Menu', key='Voltar para o menu', font=('Helvetica', 16), size=(60, 2), button_color=('white', 'green'), pad=(10, 10))]
    ]

    window = sg.Window('Tela de Menu do Sistema', layout, size=(800, 450))

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Voltar para o menu'):
            break
        elif event == 'Cadastrar fornecedor':
            cadastrar_fornecedor()
        elif event == 'Procurar venda feita':
            consulta_pacote()
        elif event == 'Confirmar entrega':
            adicionar_pacote()
        elif event == 'Cadastrar avaria pacote':
            cadastrar_entrega()

    window.close()

def inicializar_banco():
    conn = sqlite3.connect('fornecedores.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fornecedores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cnpj_cpf TEXT NOT NULL,
                    contato TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fornecedor_id INTEGER,
                    nome_produto TEXT NOT NULL,
                    quantidade_paletes INTEGER NOT NULL,
                    quantidade_caixas INTEGER NOT NULL,
                    data_pedido TEXT NOT NULL,
                    FOREIGN KEY(fornecedor_id) REFERENCES fornecedores(id)
                )''')
    conn.commit()
    conn.close()

def cadastrar_fornecedor():
    fornecedores = []

    layout = [
        [sg.Text('Cadastro de Fornecedor', font=('Helvetica', 20), justification='center', text_color='green')],
        [sg.Text('Nome:', size=(15, 1)), sg.InputText(key='nome_fornecedor')],
        [sg.Text('CNPJ / CPF:', size=(15, 1)), sg.InputText(key='cnpj_cpf_fornecedor')],
        [sg.Text('Contato:', size=(15, 1)), sg.InputText(key='contato_fornecedor')],
        [sg.Text('Lista de Produtos')],
        [sg.Text('Nome do Produto:', size=(15, 1)), sg.InputText(key='nome_produto')],
        [sg.Text('Quantidade por Paletes:', size=(15, 1)), sg.InputText(key='quantidade_paletes')],
        [sg.Text('Quantidade de Caixas:', size=(15, 1)), sg.InputText(key='quantidade_caixas')],
        [sg.Text('Data do Pedido:', size=(15, 1)), sg.InputText(key='data_pedido')],
        [sg.Button('Adicionar Produto', font=('Helvetica', 14), size=(15, 1))],
        [sg.Listbox(values=[], size=(60, 10), key='listbox_produtos')],
        [sg.Button('Salvar Fornecedor', font=('Helvetica', 14), size=(15, 1)), sg.Button('Cancelar', font=('Helvetica', 14), size=(15, 1))]
    ]

    window = sg.Window('Cadastrar Fornecedor', layout)

    produtos = []

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancelar'):
            break
        elif event == 'Adicionar Produto':
            produto = {
                'nome_produto': values['nome_produto'],
                'quantidade_paletes': values['quantidade_paletes'],
                'quantidade_caixas': values['quantidade_caixas'],
                'data_pedido': values['data_pedido']
            }
            
            if not all(produto.values()):
                sg.popup('Por favor, preencha todas as informações do produto!')
            else:
                produtos.append(produto)
                listbox_values = [f"Produto: {p['nome_produto']}, Paletes: {p['quantidade_paletes']}, Caixas: {p['quantidade_caixas']}, Data: {p['data_pedido']}" for p in produtos]
                window['listbox_produtos'].update(listbox_values)
        elif event == 'Salvar Fornecedor':
            fornecedor = {
                'nome': values['nome_fornecedor'],
                'cnpj_cpf': values['cnpj_cpf_fornecedor'],
                'contato': values['contato_fornecedor'],
                'produtos': produtos.copy()
            }

            if not all(fornecedor.values()) or not fornecedor['produtos']:
                sg.popup('Por favor, preencha todas as informações do fornecedor e adicione pelo menos um produto!')
            else:
                conn = sqlite3.connect('fornecedores.db')
                c = conn.cursor()
                c.execute('INSERT INTO fornecedores (nome, cnpj_cpf, contato) VALUES (?, ?, ?)', 
                          (fornecedor['nome'], fornecedor['cnpj_cpf'], fornecedor['contato']))
                fornecedor_id = c.lastrowid
                for produto in fornecedor['produtos']:
                    c.execute('''INSERT INTO produtos (fornecedor_id, nome_produto, quantidade_paletes, quantidade_caixas, data_pedido) 
                                 VALUES (?, ?, ?, ?, ?)''', 
                              (fornecedor_id, produto['nome_produto'], produto['quantidade_paletes'], produto['quantidade_caixas'], produto['data_pedido']))
                conn.commit()
                conn.close()
                sg.popup('Fornecedor cadastrado com sucesso!')
                produtos.clear()
                window['listbox_produtos'].update([])
                window['nome_fornecedor']('')
                window['cnpj_cpf_fornecedor']('')
                window['contato_fornecedor']('')
                window['nome_produto']('')
                window['quantidade_paletes']('')
                window['quantidade_caixas']('')
                window['data_pedido']('')

    window.close()


def consulta_pacote():
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


def adicionar_pacote():
    layout = [
        [sg.Text('Confirmação de Entrega', font=('Helvetica', 20), justification='center', text_color='green')],
        [sg.Text('ID do Fornecedor:', size=(15, 1)), sg.InputText(key='id_fornecedor')],
        [sg.Text('Nome do Produto:', size=(15, 1)), sg.InputText(key='nome_produto')],
        [sg.Text('Quantidade por Paletes:', size=(15, 1)), sg.InputText(key='quantidade_paletes')],
        [sg.Text('Quantidade de Caixas:', size=(15, 1)), sg.InputText(key='quantidade_caixas')],
        [sg.Text('Data do Pedido:', size=(15, 1)), sg.InputText(key='data_pedido')],
        [sg.Button('Adicionar', font=('Helvetica', 14), size=(15, 1)), sg.Button('Cancelar', font=('Helvetica', 14), size=(15, 1))]
    ]

    window = sg.Window('Adicionar Pacote', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancelar'):
            break
        elif event == 'Adicionar':
            conn = sqlite3.connect('fornecedores.db')
            c = conn.cursor()
            c.execute('''INSERT INTO produtos (fornecedor_id, nome_produto, quantidade_paletes, quantidade_caixas, data_pedido) 
                         VALUES (?, ?, ?, ?, ?)''', 
                      (values['id_fornecedor'], values['nome_produto'], values['quantidade_paletes'], values['quantidade_caixas'], values['data_pedido']))
            conn.commit()
            conn.close()
            sg.popup('Pacote adicionado com sucesso!')

    window.close()

def cadastrar_entrega():
    layout = [
        [sg.Text('Cadastro de Avaria de Pacote', font=('Helvetica', 20), justification='center', text_color='green')],
        [sg.Text('ID do Pacote:', size=(15, 1)), sg.InputText(key='id_pacote')],
        [sg.Text('Descrição da Avaria:', size=(15, 1)), sg.InputText(key='descricao_avaria')],
        [sg.Button('Registrar', font=('Helvetica', 14), size=(15, 1)), sg.Button('Cancelar', font=('Helvetica', 14), size=(15, 1))]
    ]

    window = sg.Window('Registrar Avaria', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancelar'):
            break
        elif event == 'Registrar':
            # Aqui você pode adicionar a lógica para registrar avarias no banco de dados.
            sg.popup('Avaria registrada com sucesso!')

    window.close()


# Chamada da função para abrir o menu
if __name__ == '__main__':
    abrir_menu1()
