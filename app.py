#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Bastien Roques <bastien.roques971@gmail.com>
"""

import mysql.connector
import sys
import argparse
import csv
import locale
import requests
import config
import json
import os

from database import Database
from movie import Movie
from person import Person
from moviefactory import MovieFactory
from peoplefactory import PeopleFactory
from scrapper import ScrapperWikipedia
from moviedb import MovieDatabase
from bs4 import BeautifulSoup
from datetime import datetime

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
OMDB_API_KEY = os.environ.get('OMDB_API_KEY')

# Parser
parser = argparse.ArgumentParser(description='Process MoviePredictor data')

parser.add_argument('context', choices=('people', 'movies'), help='Le contexte dans lequel nous allons travailler')

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitées du contexte')
list_parser.add_argument('--export', help='Chemin du fichier exporté')

find_parser = action_subparser.add_parser('find', help='Trouve une entité selon un paramètre')
find_parser.add_argument('--id', help='Identifant à rechercher dans la base de données', type=int)
find_parser.add_argument('--imdb_id', help='Identifiant IMDB à rechercher dans la base de données')

search_parser = action_subparser.add_parser('search', help='Trouve une entité selon un paramètre')
search_parser.add_argument('--imdb', help='Trouver IMDB ID depuis API')

scrapper_parser = action_subparser.add_parser('scrapper', help='Trouve une entité selon un paramètre')
scrapper_parser.add_argument('--url', help='Trouver IMDB ID depuis API')

import_parser = action_subparser.add_parser('import', help='Importer un fichier ou des données')
import_parser.add_argument('--file', help='Chemin vers le fichier à importer')
import_parser.add_argument('--api', help='Import depuis API', choices=('all') )
import_parser.add_argument('--year', help='Année de sortie des films importés', type=int)
import_parser.add_argument('random', help='Importés de films de films aléatoire')

insert_parser = action_subparser.add_parser('insert', help='Insert une nouvelle entité')
known_args = parser.parse_known_args()[0]

if known_args.context == "people":
    insert_parser.add_argument('--firstname', help='Prénom de la nouvelle personne', required=True)
    insert_parser.add_argument('--lastname', help='Nom de la nouvelle personne', required=True)

if known_args.context == "movies":
    insert_parser.add_argument('--title', help='Titre en France', required=True)
    insert_parser.add_argument('--original-title', help='Titre original', required=True)
    insert_parser.add_argument('--duration', help='Durée du film', type=int, required=True)
    insert_parser.add_argument('--release-date', help='Date de sortie en France', required=True)
    insert_parser.add_argument('--rating', help='Classification du film', choices=('TP', '-12', '-16'), required=True)

args = parser.parse_args()

# People actions
if args.context == "people":

    if args.action == "list":
        people = PeopleFactory().find_all()
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].__dict__.keys())
                for person in people:
                    writer.writerow(person.__dict__.values())
        else:
            for person in people:
                Person().__repr__(person)

    if args.action == "find":
        person_id = args.id
        person = PeopleFactory().find_one_by_id(person_id)
        if (person == None):
            print(f"Aucun people n'a été trouvé avec l'id {person_id}")
        else:
            Person().__repr__(person)

    if args.action == "insert":
        print(f"Insertion d'une nouvelle personne: {args.firstname} {args.lastname}")
        person = Person(
            args.firstname,
            args.lastname
        )
        person_id = PeopleFactory().insert(person)
        print(f"Nouvelle personne insérée avec l'id {person_id}")

# Movies actions
if args.context == "movies":

    if args.action == "list":  
        movies = MovieFactory().find_all()
        for movie in movies:
            print(movie)

    if args.action == "find":
        if args.id:
            movie_id = args.id
            movie = MovieFactory().find_one_by_id(movie_id)
            if (movie == None):
                print(f"Aucun film n'a été trouvé avec l'id {movie_id}")
            else:
                print(movie)
    
    if args.action == "search":
        if args.imdb:
            movie_query = args.imdb
            movie_imdb = MovieDatabase(TMDB_API_KEY, OMDB_API_KEY).get_imdb_id(movie_query)
           
            if (movie_imdb == None):
                print(f"Aucun IMDb ID n'a été trouvé pour ce film : {movie_query}")
            else:
                print(movie_imdb)

    if args.action == "scrapper":
        if args.url:
            ScrapperWikipedia().scrapper_movie_wikipedia(args.url)


    if args.action == "insert":
        print(f"Insertion d'un nouveau film: {args.title}")
        movie = Movie(
            title = args.title,
            original_title = args.original_title,
            duration = args.duration,
            rating = args.rating,
            release_data = args.release_date
        )      
        movie_id = MovieFactory().insert(movie)
        print(f"Nouveau film inséré avec l'id {movie_id}")

    if args.action == "import":

        if args.file:
            with open(args.file, 'r', encoding='utf-8', newline='\n') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    movie_id = Movie(
                        title = row['title'],
                        original_title = row['original_title'],
                        duration = row['duration'],
                        rating = row['rating'],
                        release_date = row['release_date']
                    )
                    MovieFactory().insert(movie_id)
                    print(f"Nouveau film inséré avec l'id {movie_id}")

        if args.api:
            if args.year:
                MovieDatabase().get_movies_by_year(args.year)
            if args.random:
                MovieDatabase(TMDB_API_KEY, OMDB_API_KEY).get_random_movie()
          
