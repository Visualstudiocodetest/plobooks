from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    mot_de_passe: str = Field(..., min_length=6)
    role: Optional[str] = "user"

class UserRead(BaseModel):
    id_utilisateur: int
    nom: str
    prenom: str
    email: EmailStr
    role: str

class LoginRequest(BaseModel):
    username: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
