from celery import Celery, shared_task
import asyncio
from service.whatsapp_service import send_message_n8n
from threading import Lock
import os
from dotenv import load_dotenv

load_dotenv()

celery_url= os.getenv("CELERY_BROKER_URL")

celery_app = Celery("whatsapp_tasks", broker=celery_url)

message_queue = []
queue_lock = Lock()


@celery_app.task(name="send_message_task")
def send_message_task(phone: str, message: str):
    print(f"Enviando mensaje a n8n desde Celery: {phone} -> {message}")
    asyncio.run(send_message_n8n(phone, message))


@celery_app.task(name="process_batch_task")
def process_batch_task():
    with queue_lock:
        if not message_queue:
            print("No hay mensajes para procesar.")
            return

        batch = message_queue.copy()
        message_queue.clear()

    print(f"Procesando lote de {len(batch)} mensajes...")

    for item in batch:
        phone = item["phone"]
        message = item["message"]
        asyncio.run(send_message_n8n(phone, message))
