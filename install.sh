#!/bin/bash

# Créer un environnement virtuel
python3 -m venv env

# Activer l'environnement virtuel
source env/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur uvicorn
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &