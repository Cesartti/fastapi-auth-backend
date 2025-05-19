from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: int

class Token(BaseModel):
    access_token: str
    token_type: str
    role: int
    user_id: int
