from database import users_collection
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == password:
        return user
    return False
