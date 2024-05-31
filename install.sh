#!/bin/bash

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur uvicorn
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &