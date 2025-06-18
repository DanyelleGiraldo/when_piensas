from fastapi import FastAPI, HTTPException
from typing import List
from infrasctructure.database.client_schema import ClientResponse, ClientList
from config.db import get_clients, init_database
from application.service.clients_service import ClientService

app = FastAPI()
init_database()

@app.get("/clients/pending", response_model=ClientList)
async def get_pending_clients(
    page: int = 1,
    limit: int = 10
):

    try:
        service = ClientService()
        return service.get_pending_clients(page=page, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/clients/{client_id}/mark-called", response_model=ClientResponse)
async def mark_client_as_called(client_id: str):

    try:
        service = ClientService()
        updated_client = service.mark_as_called(client_id)
        return updated_client
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))