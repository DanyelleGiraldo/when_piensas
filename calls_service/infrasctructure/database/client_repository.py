from bson import ObjectId
from pymongo.collection import Collection

class ClientRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_pending_clients(self, skip: int = 0, limit: int = 10):
        """Obtiene los clientes pendientes de llamar"""
        return list(self.collection.find(
            {"state": "pending"}
        ).skip(skip).limit(limit))

    def mark_as_called(self, client_id: str):
        """Actualiza el estado del cliente a called"""
        result = self.collection.update_one(
            {
                "_id": ObjectId(client_id),
                "state": "pending"
            },
            {
                "$set": {"state": "called"},
                "$inc": {"total_calls": 1}
            }
        )
        if result.matched_count == 0:
            return None
        return self.get_by_id(client_id)

    def get_by_id(self, client_id: str):
        return self.collection.find_one({"_id": ObjectId(client_id)})

    def count_pending(self) -> int:
        """Cuenta el total de clientes en estado pendiente"""
        return self.collection.count_documents({"state": "pending"})