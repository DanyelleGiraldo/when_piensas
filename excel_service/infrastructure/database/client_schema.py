from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Union
from bson import ObjectId


# Utilidad para usar ObjectId con Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('ID inválido')
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Clase base para compartir atributos comunes
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
    state: Optional[str]


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
    state: Optional[str]

    @validator('phone')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('El número de teléfono debe contener solo dígitos')
        return v


class ClientResponse(ClientBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    total_calls: int = 0
    successful_calls: int = 0

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True


class ClientDelete(BaseModel):
    id: PyObjectId = Field(..., alias="_id")


class ClientSearch(BaseModel):
    name: Optional[str] = Field(None, description="Nombre del cliente")
    phone: Optional[str] = Field(None, description="Número de teléfono")
    mail: Optional[EmailStr] = Field(None, description="Correo electrónico")
    category: Optional[str] = Field(None, description="Categoría del cliente")
    state: Optional[str] = Field(None, description="Estado del cliente")


class ClientList(BaseModel):
    clients: List[ClientResponse]
    total: int
    page: int
    size: int

