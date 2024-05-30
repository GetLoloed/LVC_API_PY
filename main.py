from fastapi import FastAPI
from db.database import engine, Base
from routes.item_routes import router

# Crée toutes les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Crée une instance de FastAPI
app = FastAPI()

# Inclus le router dans l'application FastAPI
app.include_router(router)
