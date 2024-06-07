from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez restreindre cela à des domaines spécifiques en production
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les en-têtes
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
