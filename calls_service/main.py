from fastapi import FastAPI, HTTPException, Query
from typing import List
import threading
from infrasctructure.database.client_schema import ClientResponse, ClientList
from config.db import get_clients, init_database
from application.service.clients_service import ClientService

app = FastAPI()
init_database()

clientes_actuales = []
lock = threading.Lock()

@app.get("/clients/pending", response_model=ClientList)
async def get_pending_clients(
    page: int = 1,
    limit: int = 10
):
    global clientes_actuales

    try:
        service = ClientService()
        resultado = service.get_pending_clients(page=page, limit=limit)

        with lock:
            clientes_actuales = resultado["clients"]

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/clients/mark-called-by-phone", response_model=ClientResponse)
async def mark_client_as_called_by_phone(phone: str = Query(..., description="Número de teléfono del cliente")):
    try:
        service = ClientService()
        updated_client = service.mark_as_called_by_phone(phone)
        return updated_client
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_names")
async def get_nombres():
    global clientes_actuales

    with lock:
        if not clientes_actuales:
            return {
                "type": "conversation_initiation_client_data",
                "dynamic_variables": {
                    "person_name": "no hay más clientes"
                },
                "status": "done"
            }

        cliente = clientes_actuales.pop(0)

        return {
            "type": "conversation_initiation_client_data",
            "dynamic_variables": {
                "person_name": cliente["name"] if isinstance(cliente, dict) else cliente.name
            },
            "status": "success"
        }
