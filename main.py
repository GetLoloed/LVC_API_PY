from fastapi import FastAPI
from db.database import engine, Base
from routes.item_routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
