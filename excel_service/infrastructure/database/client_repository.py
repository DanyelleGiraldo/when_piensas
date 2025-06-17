from bson import ObjectId
from client_schema import ClientCreate, ClientUpdate
from pymongo.collection import Collection


class ClientRepository:

    def __init__(self, collection: Collection):
        self.collection = collection

    def get_by_id(self, client_id: str):
        return self.collection.find_one({"_id": ObjectId(client_id)})

    def get_all(self, skip: int = 0, limit: int = 10):
        return list(self.collection.find().skip(skip).limit(limit))

    def create(self, client_data: ClientCreate):
        data = client_data.dict()
        result = self.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return data

    def update(self, client_id: str, client_data: ClientUpdate):
        update_data = {"$set": client_data.dict(exclude_unset=True)}
        result = self.collection.update_one(
            {"_id": ObjectId(client_id)},
            update_data
        )
        if result.matched_count == 0:
            return None
        return self.get_by_id(client_id)

    def delete(self, client_id: str):
        client = self.get_by_id(client_id)
        if not client:
            return None
        self.collection.delete_one({"_id": ObjectId(client_id)})
        return client
