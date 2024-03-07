from pydantic import BaseModel

class Info_user(BaseModel):
    username: str
    password: str