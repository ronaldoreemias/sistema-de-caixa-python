import PySimpleGUI as sg
from menu import menu  # Certifique-se de que o new_menu.py está no mesmo diretório ou ajuste o caminho de importação

def menu_inicial():
    menu()

# ---- FUNÇÕES DA INTERFACE ----

# Função de clique para login
def clique(email, senha):
    user_email = email
    user_senha = senha

    if not user_email or not user_senha:
        sg.popup_error("Erro", "Por favor, preencha todos os campos!")
        return False

    if user_email == 'admin' and user_senha == 'admin':
        sg.popup("Login", "Login bem-sucedido! Bem-vindo ao painel do funcionário.")
        menu_inicial()
        return True
    else:
        sg.popup_error("Erro", "E-mail ou senha incorretos.")
        return False

# ---- INICIALIZAÇÃO DA JANELA PRINCIPAL ----

def login_funcionario():

    sg.theme('LightGreen')

    # Layout da janela
    layout = [
        [sg.Text(' ')],
        [sg.Text(' ')],
        [sg.Text('Sistema de Caixa - Login', size=(60, 1),font=("Helvetica", 20), justification='center', text_color="black")],
        [sg.Text(' ')],
        [sg.Text(' ')],
        [sg.Text(' ')],
        [sg.Text('E-mail:', size=(5, 1), font=("Helvetica", 10)), sg.InputText(key='email', font=("Helvetica", 10))],
        [sg.Text(' ')],
        [sg.Text('Senha:', size=(5, 1), font=("Helvetica", 10)), sg.InputText(key='senha', password_char='*', font=("Helvetica", 10))],
        [sg.Text(' ')],
        [sg.Text(' ')],
        [sg.Button('Login', size=(10, 1), font=("Helvetica", 14)), sg.Button('Sair', size=(10, 1), font=("Helvetica", 14))]
    ]

    # Definindo a janela com tamanho maior e aparência profissional
    window = sg.Window('Login Funcionário', layout, size=(600, 400), element_justification='center', finalize=True)

    # Loop de eventos
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        elif event == 'Login':
            if clique(values['email'], values['senha']):
                window.close()

    window.close()

if __name__ == "__main__":
    login_funcionario()
