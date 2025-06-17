# services/client_service.py
from bson import ObjectId

from infrastructure.database.client_repository import ClientRepository
from infrastructure.database.client_schema import ClientCreate, ClientUpdate, ClientSearch
from domain.models.clients import Client


class ClientService:
    def __init__(self, db: Session):
        self.repo = ClientRepository(db)

    def create(self, data: ClientCreate):
        return self.repo.create(data)

    def update(self, client_id: int, data: ClientUpdate):
        return self.repo.update(client_id, data)

    def delete(self, client_id: int):
        return self.repo.delete(client_id)

    def get_by_id(self, client_id: int):
        return self.repo.get_by_id(client_id)

    def list(self, skip: int = 0, limit: int = 10):
        return self.repo.get_all(skip, limit)

    def search(self, filters: ClientSearch):
        query = self.repo.db.query(Client)
        if filters.name:
            query = query.filter(Client.name.ilike(f"%{filters.name}%"))
        if filters.phone:
            query = query.filter(Client.phone == filters.phone)
        if filters.mail:
            query = query.filter(Client.mail == filters.mail)
        if filters.category:
            query = query.filter(Client.category.ilike(f"%{filters.category}%"))
        if filters.state:
            query = query.filter(Client.state == filters.state)
        return query.all()
