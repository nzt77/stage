from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import base64
import hashlib
from datetime import datetime
import json

public_key_pem = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0oW2ld1pySzH36hj+fkb
8hyAZJnCFGYo40YlSrxoXNSv2Y7vZiMbLIpLSDMW+2AXUgNd7m00OBGHmhfd0Tmo
aGjSkVB/xa3+D3FEJNONnr7O9D0Gw2AA7cEapvQQqxTatcTypQEmYEs11db0/OM1
Mtddrd6yNp4nIShf9VV2c21JowCh9jDKlM5oimw/x5Ab5e3TjXVrNhxdqoZPaHu7
OljwQ4zNIgblHQAS3UWweIigPQB2dic7W6Zu1O23Kr4k3iF6yL6m1FGvzQsLqljQ
x9LMf4vQXQwtWfM76TfwpBgkN7jsJbQ8TIwM+/BR+YIrr2c+7O/rLIQEmtl9TYhE
8QIDAQAB
-----END PUBLIC KEY-----'''

def load_public_key(pem_data):
    public_key = serialization.load_pem_public_key(
        pem_data.encode(),
    )
    return public_key

public_key = load_public_key(public_key_pem)

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
    hash: str

def encrypt_with_public_key(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode('utf-8')

def encrypt_data(public_key, transaction: Transaction) -> str:
    transaction_data = f"{transaction.id}|{transaction.montant}|{transaction.date}|{transaction.auteur}"
    encrypted_data = encrypt_with_public_key(public_key, transaction_data)
    return encrypted_data

def calculate_hash(transaction_data, previous_hash=""):
    combined_data = f"{previous_hash}|{transaction_data}"
    return hashlib.sha256(combined_data.encode()).hexdigest()

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
    encrypted_data = encrypt_data(public_key, transaction)
    transaction_data = f"{transaction.id}|{transaction.montant}|{transaction.date}|{transaction.auteur}"
    previous_transaction = transactions_db.get(transaction.id - 1)
    previous_hash = previous_transaction.hash if previous_transaction else ""
    transaction_hash = calculate_hash(transaction_data, previous_hash)
    encrypted_transaction = EncryptedTransaction(id=transaction.id, encrypted_data=encrypted_data, hash=transaction_hash)
    if transaction.id in transactions_db:
        raise HTTPException(status_code=400, detail="Transaction ID existe déjà")
    transactions_db[transaction.id] = encrypted_transaction
    return {"message": "Transaction créée avec succès !", "transaction": encrypted_transaction}

@app.get("/transactions/", response_model=List[EncryptedTransaction])
async def read_transactions():
    return list(transactions_db.values())
