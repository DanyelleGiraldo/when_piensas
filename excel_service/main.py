from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from typing import List
from infrastructure.database.client_schema import (
    ClientCreate, 
    ClientUpdate, 
    ClientResponse, 
    ClientSearch,
    ClientList
)
from config.db import get_clients, init_database
from domain.services.excel_extraction import process_excel, save_clients
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

app = FastAPI(title="API de Clientes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_database()

@app.post("/clients/", response_model=ClientResponse)
def create_client(client: ClientCreate):
    collection = get_clients()
    result = collection.insert_one(client.dict())
    client_data = collection.find_one({"_id": result.inserted_id})
    return ClientResponse(**client_data, id=str(client_data["_id"]))

@app.get("/clients/{client_id}", response_model=ClientResponse)
def get_client(client_id: str):
    collection = get_clients()
    client = collection.find_one({"_id": ObjectId(client_id)})
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return ClientResponse(**client, id=str(client["_id"]))

@app.put("/clients/{client_id}", response_model=ClientResponse)
def update_client(client_id: str, client: ClientUpdate):
    collection = get_clients()
    result = collection.update_one(
        {"_id": ObjectId(client_id)},
        {"$set": client.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    updated_client = collection.find_one({"_id": ObjectId(client_id)})
    return ClientResponse(**updated_client, id=str(updated_client["_id"]))

@app.delete("/clients/{client_id}")
def delete_client(client_id: str):
    collection = get_clients()
    result = collection.delete_one({"_id": ObjectId(client_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado exitosamente"}

@app.get("/clients/", response_model=ClientList)
def list_clients(skip: int = 0, limit: int = 10):
    collection = get_clients()
    clients_cursor = collection.find().skip(skip).limit(limit)
    clients = [ClientResponse(**doc, id=str(doc["_id"])) for doc in clients_cursor]
    total = collection.count_documents({})
    return ClientList(
        clients=clients,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@app.post("/clients/search", response_model=List[ClientResponse])
def search_clients(filters: ClientSearch):
    collection = get_clients()
    query = {}

    if filters.name:
        query["name"] = {"$regex": filters.name, "$options": "i"}
    if filters.phone:
        query["phone"] = filters.phone
    if filters.mail:
        query["mail"] = filters.mail
    if filters.category:
        query["category"] = {"$regex": filters.category, "$options": "i"}
    if filters.state:
        query["state"] = filters.state

    clients_cursor = collection.find(query)
    return [ClientResponse(**doc, id=str(doc["_id"])) for doc in clients_cursor]

@app.post("/clients/upload-excel")
async def upload_excel(
    file: UploadFile = File(...),
    col_name: str = Query(...),
    col_number: str = Query(...),
    col_review: str = Query(...),
    col_category: str = Query(...),
    col_adress: str = Query(...),
    col_web: str = Query(...),
    col_mail: str = Query(...),
    col_latitude: str = Query(...),
    col_length: str = Query(...),
    col_ubication: str = Query(...)
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)")

    try:
        clients = process_excel(
            file,
            col_name,
            col_number,
            col_review,
            col_category,
            col_adress,
            col_web,
            col_mail,
            col_latitude,
            col_length,
            col_ubication
        )
        await save_clients(clients)
        return {"message": f"Se procesaron {len(clients)} clientes exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "healthy"}
