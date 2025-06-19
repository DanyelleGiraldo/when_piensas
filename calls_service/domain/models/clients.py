from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class ClientBase(BaseModel):
    name: str = Field(..., max_length=100)
    phone: str = Field(..., max_length=20)
    review: Optional[str] = None
    category: Optional[str] = None
    adress: Optional[str] = None
    web: Optional[str] = None
    mail: Optional[EmailStr] = None
    latitude: Optional[str] = None
    length: Optional[str] = None
    ubication: Optional[str] = None
    state: Optional[str] = "pending"


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=300)
    phone: Optional[str] = Field(None, max_length=20)
    review: Optional[str] = None
    category: Optional[str] = None
    adress: Optional[str] = None
    web: Optional[str] = None
    mail: Optional[EmailStr] = None
    latitude: Optional[str] = None
    length: Optional[str] = None
    ubication: Optional[str] = None
    state: Optional[str] = None


class ClientResponse(ClientBase):
    id: str

    class Config:
        orm_mode = True


class ClientSearch(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    mail: Optional[str] = None
    category: Optional[str] = None
    state: Optional[str] = None


class ClientList(BaseModel):
    clients: list[ClientResponse]
    total: int
    page: int
    size: int
