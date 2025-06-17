from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from infrastructure.database.base_client import ClientBase, ClientStatus


class ClientCreate(ClientBase):
    """Para creación de cliente."""
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=7, max_length=20)
    review: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=500)
    adress: Optional[str]
    web: Optional[str]
    mail: Optional[EmailStr]
    latitude: Optional[str]
    length: Optional[str]
    ubication: Optional[str]
    state: Optional[ClientStatus] = None

    @validator('phone')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('El número de teléfono debe contener solo dígitos')
        return v


class ClientResponse(ClientBase):
    id: int
    total_calls: int = 0
    successful_calls: int = 0

    class Config:
        from_attributes = True

class ClientDelete(BaseModel):
    id: int = Field(..., description="ID del cliente a eliminar")

class ClientSearch(BaseModel):
    name: Optional[str] = Field(None, description="Nombre del cliente")
    phone: Optional[str] = Field(None, description="Número de teléfono")
    mail: Optional[EmailStr] = Field(None, description="Correo electrónico")
    category: Optional[str] = Field(None, description="Categoría del cliente")
    state: Optional[ClientStatus] = Field(None, description="Estado del cliente")


class ClientList(BaseModel):
    clients: List[ClientResponse]
    total: int
    page: int
    size: int
