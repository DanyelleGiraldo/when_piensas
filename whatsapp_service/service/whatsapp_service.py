import httpx
import os
from dotenv import load_dotenv


load_dotenv()


n8n_webhook= os.getenv("N8N_WEBHOOK")

async def send_message_n8n (phone: str, message: str):
    payload = {
        "phone": phone,
        "message": message
    }
    print(f"Intentando enviar a n8n el payload: {payload}")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(n8n_webhook, json=payload)
            
            # Me devuelve el error
            response.raise_for_status() 
            
            print(f"Petición a n8n enviada exitosamente. Status Code: {response.status_code}")

    except httpx.HTTPStatusError as exc:
        print(f"Error en la respuesta HTTP de n8n: {exc.response.status_code}")
        print(f"Cuerpo de la respuesta de error: {exc.response.text}")
    except httpx.RequestError as exc:
        print(f"Error de red al intentar conectar con n8n: {exc}")
    except Exception as e:
        print(f"Se ha producido un error inesperado en send_message_n8n: {e}")