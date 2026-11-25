from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegsiter(BaseModel):
    full_name:str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value:str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Full name must contain atleast 2 characters")
        return value


    @field_validator("email")
    @classmethod
    def normalize_email(cls, value:str) -> str:
        return value.strip().lower()


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) #Allows Pydantic to create response schemas directly from SQLAlchemy model objects (using object attributes instead of dictionaries).

    id: UUID
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime