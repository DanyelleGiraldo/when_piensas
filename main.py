from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from typing import List
import threading
import time

app = FastAPI()

# Leer archivo Excel
df = pd.read_excel("agenciasdeviajebarranquilla.xlsx")
nombres: List[str] = df["Nombre"].dropna().tolist()
numeros: List[str] = df["Número de teléfono móvil"].dropna().tolist()

# Control de índice
index_lock = threading.Lock()
current_index = 0
last_request_time = time.time()

def reset_index():
    global current_index, last_request_time
    current_index = 0
    last_request_time = time.time()

def check_and_reset_timeout():
    global last_request_time
    current_time = time.time()
    if current_time - last_request_time > 300:  # 300 segundos = 5 minutos
        reset_index()
    last_request_time = current_time

@app.post("/webhook")
@app.post("/get")
async def webhook(request: Request):
    global current_index
    with index_lock:
        check_and_reset_timeout()
        
        if current_index >= len(nombres):
            reset_index()
            return {
                "type": "conversation_initiation_client_data",
                "dynamic_variables": {
                    "person_name": "no hay mas clientes"
                },
                "status": "success"
            }
        
        nombre = nombres[current_index]
        current_index += 1
        
        return {
            "type": "conversation_initiation_client_data",
            "dynamic_variables": {
                "person_name": nombre
            },
            "status": "success"
        }
    
@app.get("/numero")
async def webhook(request: Request):
    global current_index
    with index_lock:
        check_and_reset_timeout()
        
        if current_index >= len(numeros):
            reset_index()
            return {
                "phone_number": "no hay mas clientes"
            }
        
        numero = numeros[current_index]
        current_index += 1
        
        return {
            "phone_number": f"{numero}"
        }

@app.get("/")
async def health_check():
    return {"status": "healthy", "total_names": len(nombres)}