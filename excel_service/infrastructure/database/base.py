from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from enum import Enum

class ClientStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"
    PENDING = "PENDING"


class ClientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=7, max_length=20)
    review: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=500)
    adress: Optional[str]
    web: Optional[str]
    mail: Optional[EmailStr]
    latitude: Optional[str]
    length: Optional[str]
    ubication: Optional[str]
    state: ClientStatus = Field(default=ClientStatus.PENDING)

    @validator('phone')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('El número de teléfono debe contener solo dígitos')
        return v