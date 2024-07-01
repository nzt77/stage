import os
import yaml
import PySimpleGUIWeb as sg
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
from datetime import datetime

users_file = 'users.yaml'
log_file = 'log.txt'

public_key_pem = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0oW2ld1pySzH36hj+fkb
8hyAZJnCFGYo40YlSrxoXNSv2Y7vZiMbLIpLSDMW+2AXUgNd7m00OBGHmhfd0Tmo
aGjSkVB/xa3+D3FEJNONnr7O9D0Gw2AA7cEapvQQqxTatcTypQEmYEs11db0/OM1
Mtddrd6yNp4nIShf9VV2c21JowCh9jDKlM5oimw/x5Ab5e3TjXVrNhxdqoZPaHu7
OljwQ4zNIgblHQAS3UWweIigPQB2dic7W6Zu1O23Kr4k3iF6yL6m1FGvzQsLqljQ
x9LMf4vQXQwtWfM76TfwpBgkN7jsJbQ8TIwM+/BR+YIrr2c+7O/rLIQEmtl9TYhE
8QIDAQAB
-----END PUBLIC KEY-----'''

private_key_pem = '''-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDShbaV3WnJLMff
qGP5+RvyHIBkmcIUZijjRiVKvGhc1K/Zju9mIxssiktIMxb7YBdSA13ubTQ4EYea
F93ROahoaNKRUH/Frf4PcUQk042evs70PQbDYADtwRqm9BCrFNq1xPKlASZgSzXV
1vT84zUy112t3rI2nichKF/1VXZzbUmjAKH2MMqUzmiKbD/HkBvl7dONdWs2HF2q
hk9oe7s6WPBDjM0iBuUdABLdRbB4iKA9AHZ2Jztbpm7U7bcqviTeIXrIvqbUUa/N
CwuqWNDH0sx/i9BdDC1Z8zvpN/CkGCQ3uOwltDxMjAz78FH5giuvZz7s7+sshASa
2X1NiETxAgMBAAECggEAAluuEzKsnyzDVmPrLsWI3k1OB0Wm12MN9stcp2AoTE+A
YsL60OpewQ2rHZvSfse+RLrPhnHhtMKstRMRKhyBU7es3os7MZDEq96cbhjFv6Jd
uUpy6D6+8+rThhnT+ZHQiCdOT0vagEsHYNkfqGXqvO8nPpQ9uDMZ6oF3X0093oaB
jcJ5TBPcJngcdCn/xIoDgEamrxysmsTfcSATgGf5C1sXEYsyCyi+bwnpuLlQxnBO
/Fj+66vs9Xx0QU/65EUFB+6dUl3GyiDFWf0/89ipWmB/ecssjL632lVuNs7zwZJP
+/WThi8GKwpaXd3jaeeECPkWsHwKs8tb2glDwP4dAQKBgQD3oeLvRoT0Um+4uPu6
eV75a4V5Xw/dHhpQ+Q5jWo6OMSf1x/xW3lceMfGo2FFI2zNcOGQm4IfySzEUPHEo
VfoM24Dfv93ngRCpvp3bye15mfGYxJGYkRe1gilpP/GByG+Zneer30ds/mf5shkg
mUWIDWvHR/OAcFR8bm3icYWv0QKBgQDZos+QP766a7UX2hHLqkMdbNvdR8N/A4LC
uqI2lViH+UcCa/0hJ/ed+9k/SZshkki85t7k0NrNZt5FcIuNPpm5LGx8s8EiHigh
uWgUv0AiMbuXS2/3uqJp4DLOxtvf6CdajmSX/mVu/9gwpPGQO2aujUJ7LQxSzMOD
67nT5ByrIQKBgCOEnMAlJTzF9jBQmAqPDghIW8Sk1empP60Ni/rEKl5KvqiKHq93
BJfYIglNvZrtldhMXlEVM2qVTlzQropSiqL9eOae5n0mDfXK2WmE9QLUCcsXpqpz
ZSsrmDT4bvNmhFtMQsZsKBqCAvfVi7UZRtfU1PioYUyyz+tpC2nHTp2BAoGBANf/
sqmj2pQC2hT2JbtRHJNTu1L/KpQg0+KYgO5Tgy5QxZ0tuGjz1dpCXvdlAkZrfS2e
pZHLh51cfzXD4X0pqEAUSwfpD8Hg1EvES/xrZCeL3HboNBRWc2NJVKPM0eSD8Kr7
r/L6VYm4+sQssGNJ0Ttkj5rYtuZmu5Vum1wlhh6BAoGBAKNfSn0DO0l6ydky51lZ
jWE/H6/p7DpvxpW1CuJWsfH6jEgWCAtCLDCow4mdqgSEJMuTWqlikxaEPYzfq2ak
Si+7tcRkeiVM/FLPK8w2zeyVsUFr0H3CHor41+bew390na5FkmOfvfkSdMGonlix
schehsAqmCybxO4AdhOWweDq
-----END PRIVATE KEY-----'''

def load_private_key(pem_data):
    private_key = serialization.load_pem_private_key(
        pem_data.encode(),
        password=None,
    )
    return private_key

private_key = load_private_key(private_key_pem)

def load_public_key(pem_data):
    public_key = serialization.load_pem_public_key(
        pem_data.encode(),
    )
    return public_key

public_key = load_public_key(public_key_pem)

def encrypt(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode('utf-8')

def load_users():
    if not os.path.exists(users_file):
        return {'users': []}
    with open(users_file, 'r') as file:
        users = yaml.safe_load(file)
        if users is None:
            users = {'users': []}
        for user in users['users']:
            if 'is_arrived' not in user:
                user['is_arrived'] = False
        return users

def register_user(username, password, role='client'):
    users = load_users()
    encrypted_password = encrypt(public_key, password)
    users['users'].append({'username': username, 'password': encrypted_password, 'role': role, 'is_arrived': False})
    with open(users_file, 'w') as file:
        yaml.safe_dump(users, file)

def check_login(username, password):
    users = load_users()
    for user in users['users']:
        if user['username'] == username:
            decrypted = decrypt(private_key, user['password'])
            if decrypted == password:
                return user
    return None

def decrypt(private_key, encrypted_message):
    encrypted_bytes = base64.b64decode(encrypted_message + '=' * (-len(encrypted_message) % 4))
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

def log_event(username, role, event):
    with open(log_file, 'a') as file:
        file.write(f'{datetime.now()} - {event}: {username}, Role: {role}\n')

layout = [
    [sg.Text('Nom d\'utilisateur'), sg.Input(key='-USERNAME-')],
    [sg.Text('Mot de passe'), sg.Input(key='-PASSWORD-', password_char='*')],
    [sg.Button('Se connecter'), sg.Button('S\'inscrire')],
    [sg.Text('', key='-OUTPUT-')]
]

window = sg.Window('Page de Login', layout, web_port=2222, web_start_browser=True)

def open_user_window(user):
    role = user['role']
    welcome_layout = [
        [sg.Text(f'Bonjour {user["username"]}, vous avez le role {role}.')],
        [sg.Button('Arrivee'), sg.Button('Depart')],
        [sg.Button('Exit')]
    ]
    return sg.Window('Bienvenue', welcome_layout, web_port=2222)

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    elif event == 'Se connecter':
        username = values['-USERNAME-']
        password = values['-PASSWORD-']
        user = check_login(username, password)
        if user:
            new_window = open_user_window(user)
            while True:
                new_event, new_values = new_window.read()
                if new_event in (None, 'Exit'):
                    break
                if new_event == 'Arrivee' and not user['is_arrived']:
                    user['is_arrived'] = True
                    log_event(user['username'], user['role'], 'Arrivee')
                elif new_event == 'Depart' and user['is_arrived']:
                    user['is_arrived'] = False
                    log_event(user['username'], user['role'], 'Depart')
            new_window.close()
            save_users(load_users())  
        else:
            window['-OUTPUT-'].update('Nom d\'utilisateur ou mot de passe incorrect.')
    elif event == 'S\'inscrire':
        username = values['-USERNAME-']
        password = values['-PASSWORD-']
        if not username or not password:
            window['-OUTPUT-'].update('Veuillez remplir tous les champs.')
        else:
            register_user(username, password, role='client')
            window['-OUTPUT-'].update('Inscription réussie ! Vous pouvez maintenant vous connecter.')

window.close()

def save_users(users):
    with open(users_file, 'w') as file:
        yaml.safe_dump(users, file)