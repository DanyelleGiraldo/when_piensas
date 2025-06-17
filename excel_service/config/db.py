import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DB_CLUSTER = os.getenv("DB_CLUSTER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

MONGO_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}/{DB_NAME}?retryWrites=true&w=majority"

def get_clients():
    try:
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client[DB_NAME]
        clients_collection = db["clients"]
        logger.info("Conectado exitosamente a MongoDB.")
        return clients_collection
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return None

def init_database():
    collection = get_clients()
    if collection is None:
        logger.error("No se pudo inicializar la base de datos porque la colección es None.")
        return

    try:
        logger.info("Índices de MongoDB creados correctamente.")
    except Exception as e:
        logger.error(f"Error al crear índices en MongoDB: {e}")
