from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connexion à la base de données SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./items.db"

# Création de la session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création de la base de données
Base = declarative_base()
