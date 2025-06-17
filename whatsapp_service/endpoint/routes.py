from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from service.whatsapp_service import send_message_n8n
import os
from dotenv import load_dotenv
import json

load_dotenv()


router = APIRouter()
verify_tokenz = os.getenv("VERIFY_TOKEN")

@router.post("/webhook")
async def recive_whatsapp_message(request: Request):
    data = await request.json()
    
    print("="*50)
    print("CUERPO COMPLETO RECIBIDO DE WHATSAPP:")
    print(json.dumps(data, indent=2))
    print("="*50)

    try:
        if isinstance(data, list):
            data = data[0]

        if "entry" in data:
            messages = data["entry"][0]["changes"][0]["value"].get("messages", [])
        else:
            messages = data.get("messages", [])

        for msg in messages:
            if msg.get("type") == "text":
                message = msg.get("text", {}).get("body")
                phone = msg.get("from")
                if message and phone:
                    print(f"MENSAJE VÁLIDO ENCONTRADO. Enviando a n8n...")
                    print(f"  -> Teléfono: {phone}")
                    print(f"  -> Mensaje: {message}")
                    await send_message_n8n(phone, message)
            else:
                print(f"Mensaje recibido no es de texto (tipo: {msg.get('type')}). Ignorando.")

    except Exception as e:
        print(f"Ha ocurrido un error al momento de enviar el mensaje: {e}")
        import traceback
        traceback.print_exc()

    return {"status": "ok"}



@router.get("/webhook")
async def verify_token(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == verify_tokenz:
        return PlainTextResponse(content=challenge, status_code=200)
    return PlainTextResponse(content="Forbidden", status_code=403)