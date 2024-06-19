from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from cryptography.fernet import Fernet
import hashlib
from datetime import datetime
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("config.json", "r") as file:
    config = json.load(file)
PRIVATE_KEY = config["PRIVATE_KEY"].encode()

PUBLIC_KEY = config.get("PUBLIC_KEY", "").encode()

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

cipher = Fernet(PRIVATE_KEY)

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

def encrypt_data(transaction: Transaction, previous_hash: str = "") -> str:
    transaction_data = f"{transaction.id}|{transaction.montant}|{transaction.date}|{transaction.auteur}"
    combined_data = f"{transaction_data}|{previous_hash}"
    encrypted_data = cipher.encrypt(combined_data.encode())
    return encrypted_data.decode()

def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

transactions_db = {}

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

@app.get("/public-key", response_model=str)
async def get_public_key():
    _, public_key = generate_rsa_keypair()
    return public_key

@app.post("/public-key")
async def set_public_key(public_key: str):
    global PUBLIC_KEY
    PUBLIC_KEY = public_key.encode()
    return {"message": "Clé publique enregistrée avec succès"}

@app.post("/decrypt")
async def decrypt_data(encrypted_data: str):
    if not PUBLIC_KEY:
        raise HTTPException(status_code=500, detail="Clé publique non disponible")
    
    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY,
        backend=default_backend()
    )
    decrypted_data = public_key.decrypt(
        encrypted_data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return {"decrypted_data": decrypted_data.decode()}

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur notre API FastAPI avec chiffrement RSA !"}
