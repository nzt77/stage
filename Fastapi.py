from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modèles Pydantic pour les requêtes et les réponses
class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Base de données fictive
fake_users_db = {
    1: {"username": "john_doe", "email": "john.doe@example.com"},
    2: {"username": "jane_smith", "email": "jane.smith@example.com"}
}

fake_items_db = [
    {"name": "Stylo", "description": "Un stylo bleu", "price": 0.50},
    {"name": "Cahier", "description": "Un cahier petit format", "price": 2.00}
]

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur notre API FastAPI !"}

@app.get("/users/", response_model=List[User])
async def read_users():
    return fake_users_db.values()

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return fake_users_db[user_id]

@app.post("/users/", response_model=User)
async def create_user(user: User):
    if user.id in fake_users_db:
        raise HTTPException(status_code=400, detail="ID déjà utilisé")
    fake_users_db[user.id] = user.dict()
    return user

@app.get("/items/", response_model=List[Item])
async def read_items():
    return fake_items_db

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = next((item for item in fake_items_db if item["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return item

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    fake_items_db.append(item.dict())
    return item
