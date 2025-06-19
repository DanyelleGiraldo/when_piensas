from bson import ObjectId
from infrasctructure.database.client_repository import ClientRepository
from config.db import get_clients
from infrasctructure.database.client_schema import ClientResponse, ClientList

class ClientService:
    def __init__(self):
        collection = get_clients()
        if collection is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        self.repo = ClientRepository(collection)
    
    def _prepare_client_data(self, client_data: dict) -> dict:
        """
        Prepara los datos del cliente para la serialización
        """
        if client_data and '_id' in client_data:
            client_data['_id'] = str(client_data['_id'])
        return client_data
    
    def get_pending_clients(self, page: int = 1, limit: int = 10) -> ClientList:
        skip = (page - 1) * limit
        clients = self.repo.get_pending_clients(skip=skip, limit=limit)
        total = self.repo.count_pending()
        
        prepared_clients = [self._prepare_client_data(client) for client in clients]
        
        return ClientList(
            clients=[ClientResponse(**client) for client in prepared_clients],
            total=total,
            page=page,
            size=limit
        )
    
    def mark_as_called_by_phone(self, phone_number: str) -> ClientResponse:
        updated_client = self.repo.mark_as_called_by_phone(phone_number)
        if not updated_client:
            raise ValueError("Cliente no encontrado o no está en estado pendiente")

        # Convertir ObjectId a string
        prepared_client = self._prepare_client_data(updated_client)
        return ClientResponse(**prepared_client)
