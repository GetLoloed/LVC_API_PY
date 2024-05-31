#!/bin/bash

# Mettre à jour le système
sudo apt-get update -y

# Installer python3, pip et venv
sudo apt-get install -y python3 python3-pip python3-venv git


# Créer un environnement virtuel
python3 -m venv env

# Activer l'environnement virtuel
. env/bin/activate

# Installer les dépendances
pip install --isolated -r requirements.txt

openssl req -x509 -out server.crt -keyout server.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")

# Démarrer le serveur uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-certfile server.crt --ssl-keyfile server.key