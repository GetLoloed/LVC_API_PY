from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de données
SQLALCHEMY_DATABASE_URL = "sqlite:///./items.db"

# Création du moteur de la base de données
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Configuration de la classe de session pour établir toutes les connexions à la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclaration de la base de données principale que nos modèles hériteront
Base = declarative_base()
