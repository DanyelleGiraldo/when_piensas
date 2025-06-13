# Proyecto FastAPI

Este es un proyecto base para trabajar con FastAPI.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

2. Activar el entorno virtual:
- En Windows:
```bash
.\venv\Scripts\activate
```
- En Linux/Mac:
```bash
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Para iniciar el servidor de desarrollo:
```bash
uvicorn main:app --reload
```

El servidor se iniciará en `http://localhost:8000`

## Documentación

- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

## Endpoints disponibles

- GET `/`: Mensaje de bienvenida
- GET `/health`: Verificación del estado de la API 