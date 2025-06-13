from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from typing import List
import threading

app = FastAPI()

# Leer archivo Excel
df = pd.read_excel("agenciasdeviajebarranquilla.xlsx")
nombres: List[str] = df["Nombre"].dropna().tolist()

# Control de índice
index_lock = threading.Lock()
current_index = 0

@app.post("/webhook")
@app.post("/get")
async def webhook(request: Request):
    global current_index
    with index_lock:
        if current_index >= len(nombres):
            raise HTTPException(status_code=404, detail="No hay más nombres disponibles.")
        
        nombre = nombres[current_index]
        current_index += 1
        
        return {
            "type": "conversation_initiation_client_data",
            "dynamic_variables": {
                "person_name": "{{ $json.person_name }}"
            },
            "status": "success"
        }

@app.get("/")
async def health_check():
    return {"status": "healthy", "total_names": len(nombres)}