import PySimpleGUIWeb as sg
import yaml

with open('users.yaml', 'r') as file:
    users_data = yaml.safe_load(file)

def save_users(users_data):
    with open('users.yaml', 'w') as file:
        yaml.safe_dump(users_data, file)

layout = [
    [sg.Text('Connexion', size=(15, 1), font=('Helvetica', 18), justification='center')],
    [sg.Text('Nom d\'utilisateur', size=(15, 1)), sg.InputText(key='username')],
    [sg.Text('Mot de passe', size=(15, 1)), sg.InputText(password_char='*', key='password')],
    [sg.Button('Login'), sg.Button('Register'), sg.Button('Cancel')]
]

window = sg.Window('Page de Connexion', layout)

while True:
    event, values = window.read()
    
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    
    if event == 'Login':
        username = values['username']
        password = values['password']
        
        valid_user = False
        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                valid_user = True
                sg.popup('Connexion réussie', f'Bienvenue, {username}!')
                break
        
        if not valid_user:
            sg.popup('Erreur de connexion', 'Nom d\'utilisateur ou mot de passe incorrect')
        else:
            permission_layout = [
                [sg.Text(f'Bienvenue, {username}', size=(15, 1), font=('Helvetica', 18), justification='center')],
                [sg.Text('Vous avez les permissions suivantes :')],
                [sg.Text('- Voir vos réservations')],
                [sg.Button('Logout')]
            ]
            
            permission_window = sg.Window('Permissions', permission_layout)
            while True:
                perm_event, perm_values = permission_window.read()
                if perm_event in (sg.WIN_CLOSED, 'Logout'):
                    permission_window.close()
                    break

    elif event == 'Register':
        username = values['username']
        password = values['password']
        
        user_exists = False
        for user in users_data['users']:
            if user['username'] == username:
                user_exists = True
                break
        
        if user_exists:
            sg.popup('Erreur de registre', 'Nom d\'utilisateur déjà utilisé')
        else:
            new_user = {"username": username, "password": password, "role": "client"}
            users_data['users'].append(new_user)
            save_users(users_data)
            sg.popup('Registre réussi', 'Utilisateur créé avec succès ! Vous pouvez maintenant vous connecter.')

window.close()
