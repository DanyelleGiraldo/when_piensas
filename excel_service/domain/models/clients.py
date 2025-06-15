from sqlalchemy import Column, Integer, String, Boolean, VARCHAR
from config.db import Base

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name= Column(String(100), nullable=False)
    phone= Column(String(20), unique=True)
    review= Column(String(500))
    category= Column(String(500))
    adress= Column(VARCHAR)
    web= Column(VARCHAR)
    mail= Column(VARCHAR)
    latitude= Column(VARCHAR)
    length= Column(VARCHAR)
    ubication= Column(VARCHAR)
    state= str = Column(VARCHAR, default="pending")
