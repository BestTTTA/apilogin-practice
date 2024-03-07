from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import hashlib
from model import Info_user
from database import users_collection
from fastapi.middleware.cors import CORSMiddleware
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/register/")
async def register_users(user_create: Info_user):
    existing_user = users_collection.find_one({"username": user_create.username})
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Username {user_create.username} already exists")

    hashed_password = hash_password(user_create.password)

    user_data = {"username": user_create.username, "password": hashed_password}
    result = users_collection.insert_one(user_data)

    return {"message": "Registered", "user_id": str(result.inserted_id)}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

@app.post("/login/")
async def login(user: Info_user):
    user_data = users_collection.find_one({"username": user.username})
    
    if Info_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if user_data and verify_password(user.password, user_data["password"]):
        user_id = str(user_data.get("_id"))
        username = user_data.get("username")
        return {"user_id": user_id, "username": username}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
