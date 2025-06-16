from fastapi import FastAPI
from endpoint.routes import router as whastapp_router

app = FastAPI()

app.include_router(whastapp_router)