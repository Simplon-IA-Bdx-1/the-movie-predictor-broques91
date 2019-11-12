# Image de base
FROM python:3.7-alpine

# Installation de packages avec pip install
RUN pip3 install argparse mysql-connector-python beautifulsoup4 requests

# Ajout du repertoire courant
COPY . /usr/src/themoviepredictor

# On lance la commande suivante quand on démarre le conteneur
#CMD python /usr/src/themoviepredictor/app.py import --api all --for 7

WORKDIR /usr/src/themoviepredictor
# On partage un dossier de log
#VOLUME /app/log
