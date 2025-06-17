from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from enum import Enum
from bson import ObjectId
class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

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

    @validator('phone')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('El número de teléfono debe contener solo dígitos')
        return v
class ClientInDB(ClientBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
