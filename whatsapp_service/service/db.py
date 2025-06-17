import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

DB_HOST= os.getenv("DB_HOST")
DB_PORT= os.getenv("DB_PORT")
DB_NAME= os.getenv("DB_NAME")
DB_USER= os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_SCHEMA= os.getenv("DB_SCHEMA")

DATABASE= f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}"