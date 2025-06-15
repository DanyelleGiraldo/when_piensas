from openpyxl import load_workbook
from fastapi import UploadFile
from io import BytesIO
from sqlalchemy.orm import Session
from models.clients import Client
from config.db import SessionLocal

def process_excel(file: UploadFile, col_name, col_number, col_review, col_category, col_adress, col_web, col_mail, col_latitude, col_length, col_ubication):
    content = file.file.read()
    wb = load_workbook(filename=BytesIO(content))
    sheet = wb.active
    clients = []
    
    headers = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
    col_index = {name: idx for idx, name in enumerate(headers)}
    required_cols = [col_name, col_number, col_review, col_category, col_adress,
                     col_web, col_mail, col_latitude, col_length, col_ubication]
    for col in required_cols:
        if col not in col_index:
            raise ValueError(f"Columna '{col}' no encontrada en el Excel.")

    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        clients.append({
            "name": row[col_index[col_name]],
            "phone": row[col_index[col_number]],
            "review": row[col_index[col_review]],
            "category": row[col_index[col_category]],
            "adress": row[col_index[col_adress]],
            "web": row[col_index[col_web]],
            "mail": row[col_index[col_mail]],
            "latitude": row[col_index[col_latitude]],
            "length": row[col_index[col_length]],
            "ubication": row[col_index[col_ubication]],
            "state": "pending"
        })
    return clients

async def save_clients(client_list: list[dict]):
    db: Session = SessionLocal()
    try:
        for client_data in client_list:
            client = Client(**client_data)
            db.add(client)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f'Error al guardar clientes: {e}')
        raise
    finally:
        db.close()
        