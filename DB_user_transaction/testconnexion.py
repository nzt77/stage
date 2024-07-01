import PySimpleGUIWeb as sg
import yaml
from flask import Flask, render_template_string, jsonify, request
import threading
import webbrowser
import time
import requests

app = Flask(__name__)

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

window = sg.Window('Page de Connexion', layout, web_port=5000, web_start_browser=False)

def run_flask():
    app.run(debug=True, use_reloader=False, port=5000)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Connexion</title>
        <script src="https://cdn.jsdelivr.net/npm/@webcomponents/webcomponentsjs@2/webcomponents-bundle.js"></script>
        <script src="https://unpkg.com/@pysimplegui/pysimpleguiweb"></script>
    </head>
    <body>
        <div id="app"></div>
        <script>
            PySimpleGUIWeb.port = 5000;
            PySimpleGUIWeb.loadWindow('Page de Connexion', '#app');
        </script>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    event = data.get('event')
    values = data.get('values')
    
    if event == 'Login':
        username = values['username']
        password = values['password']
        
        valid_user = False
        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                valid_user = True
                return jsonify({'message': 'Connexion réussie', 'username': username})
        
        return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'})
    
    elif event == 'Register':
        username = values['username']
        password = values['password']
        
        user_exists = False
        for user in users_data['users']:
            if user['username'] == username:
                user_exists = True
                break
        
        if user_exists:
            return jsonify({'message': 'Nom d\'utilisateur déjà utilisé'})
        else:
            new_user = {"username": username, "password": password, "role": "client"}
            users_data['users'].append(new_user)
            save_users(users_data)
            return jsonify({'message': 'Utilisateur créé avec succès ! Vous pouvez maintenant vous connecter.'})
    
    return jsonify({'message': 'Invalid event'})

threading.Thread(target=run_flask).start()

time.sleep(2)
webbrowser.open("http://localhost:5000")

while True:
    event, values = window.read()
    
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    
    if event in ('Login', 'Register'):
        response = requests.post('http://localhost:5000/submit', json={'event': event, 'values': values})
        response_data = response.json()
        sg.popup(response_data['message'])

window.close()
