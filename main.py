from fastapi import FastAPI, Request
import pandas as pd
from typing import List
import threading
import time

app = FastAPI()

# Leer archivo Excel
df = pd.read_excel("agenciasdeviajebarranquilla.xlsx")
nombres: List[str] = df["Nombre"].dropna().tolist()
numeros: List[str] = df["Número de teléfono móvil"].dropna().tolist()

# Control de índice y estado de consulta
index_lock = threading.Lock()
current_index = 0
last_request_time = time.time()
estado_peticion = {"nombre": False, "numero": False}

def reset_index():
    global current_index, last_request_time, estado_peticion
    current_index = 0
    last_request_time = time.time()
    estado_peticion = {"nombre": False, "numero": False}

def check_and_reset_timeout():
    global last_request_time
    current_time = time.time()
    if current_time - last_request_time > 300:
        reset_index()
    last_request_time = current_time

@app.post("/webhook")
async def get_nombre():
    global current_index, estado_peticion
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
        estado_peticion["nombre"] = True

        # Si ya se pidió nombre y número, avanzar al siguiente
        if estado_peticion["nombre"] and estado_peticion["numero"]:
            current_index += 1
            estado_peticion = {"nombre": False, "numero": False}

        return {
            "type": "conversation_initiation_client_data",
            "dynamic_variables": {
                "person_name": nombre
            },
            "status": "success"
        }

@app.get("/numero")
async def get_numero():
    global current_index, estado_peticion
    with index_lock:
        check_and_reset_timeout()

        if current_index >= len(numeros):
            reset_index()
            return {"phone_number": "no hay mas clientes"}

        numero = numeros[current_index]
        estado_peticion["numero"] = True

        # Si ya se pidió nombre y número, avanzar al siguiente
        if estado_peticion["nombre"] and estado_peticion["numero"]:
            current_index += 1
            estado_peticion = {"nombre": False, "numero": False}

        return {"phone_number": f"{numero}"}


@app.get("/")
async def health_check():
    return {"status": "healthy", "total_names": len(nombres)}