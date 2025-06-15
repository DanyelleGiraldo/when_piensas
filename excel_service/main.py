from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from infrastructure.database.client_schema import (
    ClientCreate, 
    ClientUpdate, 
    ClientResponse, 
    ClientSearch,
    ClientList
)
from infrastructure.database.client_repository import ClientRepository
from config.db import get_db, init_database
from domain.services.excel_extraction import process_excel, save_clients
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de Clientes")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_database()

@app.post("/clients/", response_model=ClientResponse)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    repo = ClientRepository(db)
    return repo.create(client)

@app.get("/clients/{client_id}", response_model=ClientResponse)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    repo = ClientRepository(db)
    client = repo.get_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@app.put("/clients/{client_id}", response_model=ClientResponse)
async def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    repo = ClientRepository(db)
    updated_client = repo.update(client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return updated_client

@app.delete("/clients/{client_id}")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    repo = ClientRepository(db)
    deleted_client = repo.delete(client_id)
    if not deleted_client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado exitosamente"}

@app.get("/clients/", response_model=ClientList)
async def list_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    repo = ClientRepository(db)
    clients = repo.get_all(skip, limit)
    total = db.query(Client).count()
    return ClientList(
        clients=clients,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@app.post("/clients/search", response_model=List[ClientResponse])
async def search_clients(
    filters: ClientSearch,
    db: Session = Depends(get_db)
):
    repo = ClientRepository(db)
    return repo.search(filters)

@app.post("/clients/upload-excel")
async def upload_excel(
    file: UploadFile = File(...),
    col_name: str = Query(..., description="Nombre de la columna para el nombre"),
    col_number: str = Query(..., description="Nombre de la columna para el teléfono"),
    col_review: str = Query(..., description="Nombre de la columna para la reseña"),
    col_category: str = Query(..., description="Nombre de la columna para la categoría"),
    col_adress: str = Query(..., description="Nombre de la columna para la dirección"),
    col_web: str = Query(..., description="Nombre de la columna para la web"),
    col_mail: str = Query(..., description="Nombre de la columna para el email"),
    col_latitude: str = Query(..., description="Nombre de la columna para la latitud"),
    col_length: str = Query(..., description="Nombre de la columna para la longitud"),
    col_ubication: str = Query(..., description="Nombre de la columna para la ubicación")
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