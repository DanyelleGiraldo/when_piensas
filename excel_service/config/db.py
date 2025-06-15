import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT= os.getenv("DB_PORT")
DB_NAME= os.getenv("DB_NAME")
DB_USER= os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()

async def get_connection():
    try:
        conn = psycopg2.connect(
            host= DB_HOST,
            port= DB_PORT,
            dbname= DB_NAME,
            user= DB_USER,
            password= DB_PASSWORD
        )
        return conn
    except Exception as e: 
        logger.error(f"Error al conectar a la base de datos: {e}")
        return None

async def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_database():
    Base.metadata.create_all(bind=engine)
    
    conn= get_connection()
    
    try:
        await conn.execute('''              
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL UNIQUE,
                review TEXT,
                category VARCHAR(100),
                adress TEXT,
                web TEXT,
                mail VARCHAR(100),
                latitude VARCHAR(100),
                length VARCHAR(100),
                ubication TEXT,
                state VARCHAR(20) DEFAULT 'pending'
            )
        ''')
    except Exception as e:
        print(f'Error al inicializar la base de datos: {e}')
        raise
    finally:
        await conn.close()