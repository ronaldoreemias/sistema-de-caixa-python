import PySimpleGUI as sg

def telaconfig():
    layout = [
        [sg.Text('Bem-vindo às Configurações do Sistema', font=('Helvetica', 18), justification='center')],
        [sg.Text('_' * 80)],
        
        [sg.Text('Preferências de Usuário', font=('Helvetica', 14))],
        [sg.Text('Nome de Usuário:', size=(20, 1)), sg.InputText(key='username')],
        [sg.Text('Tema:', size=(20, 1)), sg.Combo(['Claro', 'Escuro'], key='theme')],
        [sg.Text('Idioma:', size=(20, 1)), sg.Combo(['Português', 'Inglês', 'Espanhol'], key='language')],
        
        [sg.Text('_' * 80)],
        
        [sg.Text('Ajustes do Sistema', font=('Helvetica', 14))],
        [sg.Checkbox('Habilitar Notificações', key='notifications')],
        [sg.Checkbox('Modo Desenvolvedor', key='dev_mode')],
        [sg.Slider(range=(0, 100), orientation='h', size=(34, 20), default_value=50, key='volume')],
        [sg.Text('Volume:')],
        
        [sg.Text('_' * 80)],
        
        [sg.Text('Segurança', font=('Helvetica', 14))],
        [sg.Text('Alterar Senha:', size=(20, 1)), sg.InputText(password_char='*', key='password')],
        [sg.Text('Confirme a Senha:', size=(20, 1)), sg.InputText(password_char='*', key='confirm_password')],
        [sg.Checkbox('Habilitar Autenticação de Dois Fatores', key='2fa')],
        
        [sg.Text('_' * 80)],
        
        [sg.Text('Sobre o Sistema', font=('Helvetica', 14))],
        [sg.Text('Versão: 1.0.0')],
        [sg.Multiline('Licença de Uso: \n\nAqui você pode colocar os termos de uso ou outras informações pertinentes.', size=(60, 5), key='license')],
        
        [sg.Button('Salvar Configurações', font=('Helvetica', 12), button_color=('white', 'green')), sg.Button('Cancelar', font=('Helvetica', 12), button_color=('white', 'red'))]
    ]
    
    window = sg.Window('Configurações do Sistema', layout)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancelar'):
            break
        if event == 'Salvar Configurações':
            # Adicione aqui a lógica para salvar as configurações
            print(values)
    
    window.close()

if __name__ == "__main__":
    telaconfig()