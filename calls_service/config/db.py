import os
from dotenv import load_dotenv
import logging
from pymongo import MongoClient

load_dotenv()

logger= logging.getLogger(__name__)

DB_CLUSTER = os.getenv("DB_CLUSTER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME  = os.getenv("DB_NAME")

MONGO_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}?retryWrites=true&w=majority"

def get_clients():
    try:
        mongo_client = MongoClient(MONGO_URI)
        db= mongo_client[DB_NAME]
        clients_collection = db["clients"]
        logger.info("Conectando exitosamente a clients.")
        return clients_collection
    except Exception as e :
        logger.error(f"Ocurrio un error al conectarse a clients: {e}")
        return None

def init_database():
    collection = get_clients()
    if collection is None:
        logger.error("No se pudo inicializar la base de datos porque la coleccion es Nula.")                                                                                                      
        return
    
    