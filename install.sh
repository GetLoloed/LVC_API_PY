#!/bin/bash

# Mettre à jour le système
sudo apt-get update -y

# Installer python3, pip et venv
sudo apt-get install -y python3 python3-pip python3-venv git

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur uvicorn
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &