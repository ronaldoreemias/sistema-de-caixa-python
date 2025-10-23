import PySimpleGUI as sg
from caixa import abrir_caixa
from cadastro import abrir_cadastro
import sqlite3
from datetime import datetime
from men import abrir_menu1
from telaconfig import telaconfig

def configuracaoTi():
    telaconfig()

def open_men():
    abrir_menu1()

def open_cadastro():
    abrir_cadastro()

def open_caixa():
    abrir_caixa()

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
        [sg.Button('Fechar', font=('Helvetica', 12))]
    ]
    
    # Criar a janela
    window = sg.Window('Relatórios Salvos', layout)
    
    # Loop de eventos para capturar ações do usuário
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Fechar':
            break
    
    # Fechar a janela
    window.close()

def gerar_relatorio():
    # Conectar ao banco de dados
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    # Obter produtos do banco de dados
    cursor.execute("SELECT id, nome, preco, quantidade FROM produtos")
    produtos = cursor.fetchall()

    # Montar o relatório
    relatorio = "Relatório de Produtos\n"
    relatorio += f"Data e Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    relatorio += f"{'ID':<5} {'Nome':<20} {'Preço':<10} {'Quantidade':<10}\n"
    relatorio += "-"*50 + "\n"

    valor_total_vendido = 0.0
    valor_total_estoque = 0.0
    for produto in produtos:
        id, nome, preco, quantidade = produto
        valor_total_estoque += preco * quantidade
        relatorio += f"{id:<5} {nome:<20} {preco:<10.2f} {quantidade:<10}\n"
    
    # Calcular as diferenças
    cursor.execute("SELECT produto_id, SUM(quantidade) as total_vendido FROM vendas GROUP BY produto_id")
    vendas = cursor.fetchall()
    for venda in vendas:
        produto_id, total_vendido = venda
        for produto in produtos:
            if produto[0] == produto_id:
                valor_total_vendido += produto[2] * total_vendido
                break

    relatorio += "\nResumo Financeiro:\n"
    relatorio += f"Valor Total Vendido: R$ {valor_total_vendido:.2f}\n"
    relatorio += f"Valor Total em Estoque: R$ {valor_total_estoque:.2f}\n"

    # Salvar relatório em um arquivo de texto
    pasta = sg.popup_get_folder('Selecione a pasta para salvar o relatório')
    if pasta:
        with open(f"{pasta}/relatorio_produtos.txt", 'w') as file:
            file.write(relatorio)
        sg.popup('Relatório gerado com sucesso!')

    conn.close()

def buscar_venda_por_cpf():
    # Conectar ao banco de dados
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    # Solicitar CPF
    cpf = sg.popup_get_text('Digite o CPF para busca:', 'Buscar Venda por CPF')
    if not cpf:
        sg.popup('CPF não informado!')
        return

    # Buscar vendas pelo CPF
    cursor.execute("SELECT * FROM vendas WHERE cpf==?", (cpf,))
    vendas = cursor.fetchall()

    # Mostrar resultados
    if vendas:
        relatorio = f"Vendas para o CPF: {cpf}\n"
        relatorio += "-"*50 + "\n"
        for venda in vendas:
            relatorio += f"ID: {venda[0]} | Produto ID: {venda[1]} | Quantidade: {venda[2]} | Data: {venda[3]}\n"
        sg.popup_scrolled(relatorio, title='Relatório de Vendas por CPF')
    else:
        sg.popup('Nenhuma venda encontrada para este CPF.')

    conn.close()

def menu():

    sg.theme('LightGreen')

    menu_def = [['Opções', ['Suporte', 'Configurações', 'Gerar Relatório']],
                ['atalho caixa', ['abrir Caixa ', 'Relatório da Lanchonete', 'Buscar Venda por CPF' ]],
                ['Configurações'],
                ['Sair']]

    layout = [
        [sg.Menu(menu_def)],
        [sg.Text(' ')],
        [sg.Text(' ')],
        [sg.Text('menu do funcionario - Caixa', font=('Helvetica', 20), justification='center', pad=(0, 10), expand_x=True, text_color='green')],
        [sg.Column([
            [sg.Button('Estoque', font=('Helvetica', 14), size=(20, 2), button_color=('white', 'green'), pad=(10, 10)),
             sg.Button('Caixa', font=('Helvetica', 14), size=(20, 2), button_color=('white', 'green'), pad=(10, 10))]
        ], justification='center')],
        [sg.Column([
            [sg.Button('Relatório das vendas', font=('Helvetica', 14), size=(20, 2), button_color=('white', 'green'), pad=(10, 10)),
             sg.Button('Suporte', font=('Helvetica', 14), size=(20, 2), button_color=('white', 'green'), pad=(10, 10))]
        ], justification='center')],
        [sg.Column([
            [sg.Button('Buscar Venda por CPF', font=('Helvetica', 14), size=(20, 2), button_color=('white', 'green'), pad=(10, 10)), 
             sg.Button('controle de estoque', font=('Helvetica', 14), size=(20, 2), button_color=('white', 'green'), pad=(10, 10))]
        ], justification='center')],
        [sg.Column([
            [sg.Button('Relatório do estoque', font=('Helvetica', 14), size=(20, 2), button_color=('white', 'green'), pad=(10, 10))]
        ], justification='center')]
    ]
    window = sg.Window('Menu Principal', layout, size=(900, 500))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        elif event == 'controle de estoque':
            abrir_menu1()
        elif event == 'Estoque':
            open_cadastro()
        elif event == 'Caixa':
            open_caixa()

        elif event == 'Relatório do estoque':
            gerar_relatorio()

        elif event == 'Relatório das vendas':
            mostrar_relatorios()
        
        elif event == 'Buscar Venda por CPF':
            buscar_venda_por_cpf()

        elif event == 'Configurações':
            # Janela para área de acesso restrito
            layout_config = [
                [sg.Text('Área do sistema restrita para o T.I.', font=('Helvetica', 14))],
                [sg.Text('Senha:', size=(15, 1)), sg.InputText(password_char='*', key='senha')],
                [sg.Button('Confirmar'), sg.Button('Cancelar')]
            ]
            window_config = sg.Window('Configurações - Acesso Restrito', layout_config)
            while True:
                event_config, values_config = window_config.read()
                if event_config == sg.WIN_CLOSED or event_config == 'Cancelar':
                    break
                elif event_config == 'Confirmar':
                    senha = values_config['senha']
                    # Verificação de senha (substitua 'minhasenha' pela senha correta)
                    if senha == 'minhasenha':
                        configuracaoTi()
                        # Coloque aqui o código para abrir as configurações
                    else:
                        sg.popup('Acesso negado!', 'Senha incorreta.')
            window_config.close()
        elif event == 'Suporte':
            # Janela para suporte
            layout_suporte = [
                [sg.Text('Bem-vindo ao Suporte', font=('Helvetica', 14))],
                [sg.Text('Para suporte, ligue para o número abaixo:')],
                [sg.Text('(82) 9 8887-3225', font=('Helvetica', 14), text_color='blue')],
                [sg.Button('Fechar')]
            ]
            window_suporte = sg.Window('Suporte', layout_suporte, size=(400, 200))
            while True:
                event_suporte, _ = window_suporte.read()
                if event_suporte == sg.WIN_CLOSED or event_suporte == 'Fechar':
                    break
            window_suporte.close()

    window.close()

if __name__ == "__main__":
    menu()
