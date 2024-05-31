#!/bin/bash

# Mettre à jour le système
sudo apt-get update -y && sudo apt-get upgrade -y

# Installer python3, pip et venv
sudo apt-get install -y python3 python3-pip python3-venv git

# Créer un environnement virtuel
python3 -m venv env

# Activer l'environnement virtuel
. env/bin/activate

# Installer les dépendances
pip install --isolated -r requirements.txt

# Définir l'adresse IP du serveur
SERVER_IP="10.17.10.7"

# Générer une nouvelle clé privée avec OpenSSL
openssl genrsa -out private.key 2048

# Générer une demande de signature de certificat (CSR)
openssl req -new -key private.key -out server.csr -subj "/CN=$SERVER_IP"

# Générer un certificat SSL auto-signé
openssl x509 -req -days 365 -in server.csr -signkey private.key -out certificate.crt

# Démarrer le serveur uvicorn en HTTPS
nohup uvicorn main:app --host $SERVER_IP --port 8000 --ssl-certfile certificate.crt --ssl-keyfile private.key &