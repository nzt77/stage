from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from cryptography.fernet import Fernet
import hashlib
from datetime import datetime

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
        raise HTTPException(status_code=400, detail="Transaction ID existe deja")
    transactions_db[transaction.id] = encrypted_transaction
    return {"message": "Transaction créée avec succès !", "transaction": encrypted_transaction}

@app.get("/transactions/", response_model=List[EncryptedTransaction])
async def read_transactions():
    return list(transactions_db.values())
