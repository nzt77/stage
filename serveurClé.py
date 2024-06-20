from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from cryptography.fernet import Fernet
import hashlib
from datetime import datetime
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import unittest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class User(BaseModel):
    id: int
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

users_db = {
    1: {"id": 1, "username": "noa", "password": "noa12"},
    2: {"id": 2, "username": "lucas", "password": "lucas12"}
}

class Transaction(BaseModel):
    id: int
    montant: float
    date: str
    auteur: str

class EncryptedTransaction(BaseModel):
    id: int
    encrypted_data: str

with open("config.json", "r") as file:
    config = json.load(file)
SECRET_KEY = config["SECRET_KEY"].encode()
cipher = Fernet(SECRET_KEY)

def encrypt_data(transaction: Transaction, previous_hash: str = "") -> str:
    transaction_data = f"{transaction.id}|{transaction.montant}|{transaction.date}|{transaction.auteur}"
    combined_data = f"{transaction_data}|{previous_hash}"
    encrypted_data = cipher.encrypt(combined_data.encode())
    return encrypted_data.decode()

def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

transactions_db = {}

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur notre API FastAPI !"}

@app.get("/users/", response_model=List[User])
async def read_users():
    return list(users_db.values())

@app.post("/login")
async def login(user: UserLogin):
    for user_record in users_db.values():
        if user_record["username"] == user.username and user_record["password"] == user.password:
            return {"message": "Connexion réussie"}
    raise HTTPException(status_code=400, detail="Nom d'utilisateur ou mot de passe incorrect")

@app.post("/register")
async def register(user: UserLogin):
    for user_record in users_db.values():
        if user_record["username"] == user.username:
            raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé")
    user_id = max(users_db.keys()) + 1
    users_db[user_id] = {"id": user_id, "username": user.username, "password": user.password}
    return {"message": "Utilisateur créé avec succès"}

@app.post("/transactions/")
async def create_transaction(transaction: Transaction):
    transaction.id = len(transactions_db) + 1  
    transaction.date = datetime.now().isoformat()  
    previous_transaction = transactions_db.get(transaction.id - 1)
    previous_hash = hash_data(previous_transaction.encrypted_data) if previous_transaction else ""
    encrypted_data = encrypt_data(transaction, previous_hash)
    encrypted_transaction = EncryptedTransaction(id=transaction.id, encrypted_data=encrypted_data)
    if transaction.id in transactions_db:
        raise HTTPException(status_code=400, detail="Transaction ID existe déjà")
    transactions_db[transaction.id] = encrypted_transaction
    return {"message": "Transaction créée avec succès !", "transaction": encrypted_transaction}

@app.get("/transactions/", response_model=List[EncryptedTransaction])
async def read_transactions():
    return list(transactions_db.values())

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    
    return private_pem, public_pem

def load_public_key(public_key_pem):
    return serialization.load_pem_public_key(
        public_key_pem.encode(),
        backend=default_backend()
    )

def load_private_key(private_key_pem):
    return serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )

def encrypt_with_public_key(public_key, data):
    return public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_with_private_key(private_key, encrypted_data):
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

class TestRSAKeyPair(unittest.TestCase):

    def setUp(self):
        self.private_pem, self.public_pem = generate_rsa_keypair()
        self.private_key = load_private_key(self.private_pem)
        self.public_key = load_public_key(self.public_pem)

    def test_key_generation(self):
        self.assertIsNotNone(self.private_pem)
        self.assertIsNotNone(self.public_pem)
        self.assertIsInstance(self.private_key, rsa.RSAPrivateKey)
        self.assertIsInstance(self.public_key, rsa.RSAPublicKey)

    def test_encryption_decryption(self):
        original_message = "Test message for encryption"
        encrypted_message = encrypt_with_public_key(self.public_key, original_message)
        decrypted_message = decrypt_with_private_key(self.private_key, encrypted_message)
        self.assertEqual(original_message, decrypted_message)
    
    def test_print_private_key(self):
        print("Clé privée :")
        print(self.private_pem)

if __name__ == "__main__":
    unittest.main()
