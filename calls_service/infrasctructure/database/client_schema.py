from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from enum import Enum

class ClientState(str, Enum):
    PENDING = "pending"
    CALLED = "called"

class ClientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    review: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=500)
    adress: Optional[str]
    web: Optional[str]
    mail: Optional[EmailStr]
    latitude: Optional[str]
    length: Optional[str]
    ubication: Optional[str]
    state: ClientState = Field(default=ClientState.PENDING)

class ClientResponse(ClientBase):
    id: str = Field(alias="_id")
    total_calls: int = 0
    
    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

class ClientList(BaseModel):
    clients: List[ClientResponse]
    total: int
    page: int
    size: int = 10
    
    model_config = {
        "from_attributes": True
    }