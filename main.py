"""
This is the main file where the FastAPI application is created and the router is included.
It also creates all the tables in the database.
"""

from fastapi import FastAPI
from db.database import engine, Base
from routes.item_routes import router

# Create all the tables in the database
Base.metadata.create_all(bind=engine)

# Create an instance of FastAPI
app = FastAPI()

# Include the router in the FastAPI application
app.include_router(router)
