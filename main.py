from fastapi import FastAPI
from db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()