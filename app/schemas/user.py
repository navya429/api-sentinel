from datetime import datetime
from uuid import UUID
from pydantic import EmailStr, Field
from app.schemas.common import ORMModel

class UserCreate(ORMModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class UserResponse(ORMModel):
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime

class TokenResponse(ORMModel):
    access_token: str
    token_type: str = "bearer"
