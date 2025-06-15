from sqlalchemy.orm import Session
from domain.models.clients import Client
from client_schema import ClientCreate, ClientUpdate


class ClientRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, client_id: int):
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(Client).offset(skip).limit(limit).all()

    def create(self, client_data: ClientCreate):
        new_client = Client(**client_data.dict())
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)
        return new_client

    def update(self, client_id: int, client_data: ClientUpdate):
        client = self.get_by_id(client_id)
        if not client:
            return None

        for field, value in client_data.dict(exclude_unset=True).items():
            setattr(client, field, value)

        self.db.commit()
        self.db.refresh(client)
        return client

    def delete(self, client_id: int):
        client = self.get_by_id(client_id)
        if not client:
            return None
        self.db.delete(client)
        self.db.commit()
        return client
