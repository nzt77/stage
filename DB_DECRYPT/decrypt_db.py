from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import json
import csv
import hashlib
import os

def load_private_key_from_file(file_path):
    with open(file_path, 'r') as file:
        private_key_pem = file.read()
    return private_key_pem

def load_private_key(pem_data):
    private_key = serialization.load_pem_private_key(
        pem_data.encode(),
        password=None,
    )
    return private_key

def decrypt_with_private_key(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        base64.b64decode(encrypted_message),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

def calculate_hash(transaction_data, previous_hash=""):
    combined_data = f"{previous_hash}|{transaction_data}"
    return hashlib.sha256(combined_data.encode()).hexdigest()


script_dir = os.path.dirname(os.path.abspath(__file__))
private_key_path = os.path.join(script_dir, 'private_key.txt')

private_key_pem = load_private_key_from_file(private_key_path)
private_key = load_private_key(private_key_pem)

db_path = os.path.join(script_dir, 'db.txt')

try:
    with open(db_path, 'r') as file:
        encrypted_data_list = json.load(file)
except json.JSONDecodeError as e:
    print(f"Erreur lors du chargement du fichier JSON : {e}")
    exit(1)

decrypted_data_list = []
previous_hash = ""
for entry in encrypted_data_list:
    transaction_id = entry['id']
    encrypted_message = entry['encrypted_data']
    decrypted_message = decrypt_with_private_key(private_key, encrypted_message)
    
    decrypted_parts = decrypted_message.split('|')
    if len(decrypted_parts) != 4:
        raise ValueError(f"Erreur dans le format de la data décryptée {transaction_id}")
    
    transaction_data = f"{transaction_id}|{decrypted_parts[1]}|{decrypted_parts[2]}|{decrypted_parts[3]}"
    calculated_hash = calculate_hash(transaction_data, previous_hash)
    
    error_message = ""
    if calculated_hash != entry['hash']:
        error_message = f"<--- Incoherence !"
    
    decrypted_data_list.append({
        "ID": transaction_id,
        "Montant": decrypted_parts[1],
        "Date": decrypted_parts[2],
        "Auteur": decrypted_parts[3],
        "Erreur": error_message
    })
    
    if not error_message:
        previous_hash = entry['hash']
    else:
        previous_hash = entry['hash']


ddb_path = os.path.join(script_dir, 'decrypted_db.csv')

with open(ddb_path, 'w', newline='') as csvfile:
    fieldnames = ['ID', 'Montant', 'Date', 'Auteur', 'Erreur']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in decrypted_data_list:
        writer.writerow(data)

print("Le fichier decrypted_db.csv a été créé avec succès.")
