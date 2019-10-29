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
import requests
import locale
from movie import Movie
from person import Person
from scrapper import Scrapper
from bs4 import BeautifulSoup
from datetime import datetime

# Scrapper
# locale.setlocale(locale.LC_ALL, 'fr_FR')

# url = 'https://fr.wikipedia.org/wiki/Joker_(film,_2019)'
# page = requests.get(url)

# soup = BeautifulSoup(page.content, 'html.parser')

# fiche_technique = soup.find(id="Fiche_technique")

# h2_tag = fiche_technique.parent
# ul_tag = h2_tag.find_next_sibling('ul')
# li_tags = ul_tag.find_all('li')

# for li_tag in li_tags:
#     splitted_li = li_tag.get_text().split(':')
#     data_type = splitted_li[0].strip()
#     data_value = splitted_li[1].strip()

#     if data_type == "Titre original":
#         title = data_value
#     if data_type == "Durée":
#         duration = data_value.replace('minutes', '').strip()
#     if data_type == "Date de sortie":
#         release_dates_li_list = li_tag.find_all("li")
#         for release_date_li in release_dates_li_list:
#             release_date_splitted = release_date_li.get_text().split(':')
#             release_country = release_date_splitted[0].strip()
#             release_date_as_string = release_date_splitted[1].strip()
#             if release_country == "France":
#                 release_date_object = datetime.strftime(release_date_as_string, '%d %B %Y')
#                 release_date_sql_string = release_date_object.strftime('%Y-%m-%d')
#                 # print('Sortie en France:', release_date_sql_string)          
#     if data_type == "Classification":
#         rating_li_list = li_tag.find_all("li")
#         for rating_li in rating_li_list:
#             rating_splitted = rating_li.get_text().split(':')
#             rating_country = rating_splitted[0].strip()
#             rating_string = rating_splitted[1].strip()
#             if rating_country == "France":
#                 if rating_string.find('12') != -1:
#                     rating = '-12'
                    
# print('title =', title)
# print('duration =', duration)
# print('release_date =', release_date_sql_string)
# print('rating =', rating)
    
# exit()

# Connect DB
def connect_to_database():
    return mysql.connector.connect(user='predictor', password='predictor',
                              host='127.0.0.1',
                              database='predictor')

# Disconnect BDD
def disconnect_database(cnx):
    cnx.close()

def create_cursor(cnx):
    return cnx.cursor(dictionary=True)

def close_cursor(cursor):    
    cursor.close()

# Query functions
def find_query(table, id):
    return ("SELECT * FROM {} WHERE id = {} LIMIT 1".format(table, id))

def find_all_query(table):
    return ("SELECT * FROM {}".format(table))

def insert_people_query(person):
    return (f"INSERT INTO `people` (`firstname`, `lastname`) VALUES ('{person.firstname}', '{person.lastname}');")

def insert_movie_query(movie):
    return (f"INSERT INTO `movies` (`title`, `original_title`, `duration`, `rating`, `release_date`) VALUES ('{movie.title}', '{movie.original_title}', {movie.duration}, '{movie.rating}', '{movie.release_date}');")

# Execute query functions
def find(table, id):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    query = find_query(table, id)
    cursor.execute(query)
    results = cursor.fetchall()
    
    entity = None
    if (cursor.rowcount == 1):
        row = results[0]
        if (table == "movies"):
            entity = Movie(
                row['title'],
                row['original_title'],
                row['duration'],
                row['rating'],
                row['release_date']
            )
            entity.id = row['id']

        if (table == "people"):
            entity = Person(
                row['firstname'],
                row['lastname']
            )
            entity.id = row['id']

    close_cursor(cursor)
    disconnect_database(cnx)

    return entity

def find_all(table):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(find_all_query(table))
    results = cursor.fetchall() # liste de données scalaires
    close_cursor(cursor)
    disconnect_database(cnx)
    if (table == 'movies'):
        movies = []
        for result in results: #result: dictionnaire
            movie = Movie(
                title = result['title'],
                original_title = result['original_title'],
                duration = result['duration'],
                rating = result['rating'],
                release_date = result['release_date']
            )
            movie.id = result['id']
            movies.append(movie)
        return movies

    if (table == 'people'):
        people = []
        for result in results: #result: dictionnaire
            person = Person(
                firstname = result['firstname'],
                lastname = result['lastname'],
            )
            person.id = result['id']
            people.append(person)
        return people


def insert_people(person):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(insert_people_query(person))
    cnx.commit()
    last_id = cursor.lastrowid
    close_cursor(cursor)
    disconnect_database(cnx)
    return last_id

def insert_movie(movie):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(insert_movie_query(movie))
    cnx.commit()
    last_id = cursor.lastrowid
    close_cursor(cursor)
    disconnect_database(cnx)
    return last_id

# Print functions
def print_person(person):
    print("#{}: {} {}".format(person.id, person.firstname, person.lastname))

def print_movie(movie):
    print("#{}: {} released on {}".format(movie.id, movie.title, movie.release_date))

# Parser
parser = argparse.ArgumentParser(description='Process MoviePredictor data')

parser.add_argument('context', choices=('people', 'movies'), help='Le contexte dans lequel nous allons travailler')

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitées du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exporté')

find_parser = action_subparser.add_parser('find', help='Trouve une entité selon un paramètre')
find_parser.add_argument('id' , help='Identifant à rechercher')

import_parser = action_subparser.add_parser('import', help='Importer un fichier CSV')
import_parser.add_argument('--file', help='Chemin vers le fichier à importer', required=True)

insert_parser = action_subparser.add_parser('insert', help='Insert une nouvelle entité')
known_args = parser.parse_known_args()[0]

if known_args.context == "people":
    insert_parser.add_argument('--firstname' , help='Prénom de la nouvelle personne', required=True)
    insert_parser.add_argument('--lastname' , help='Nom de la nouvelle personne', required=True)

if known_args.context == "movies":
    insert_parser.add_argument('--title' , help='Titre en France', required=True)
    insert_parser.add_argument('--duration' , help='Durée du film', type=int, required=True)
    insert_parser.add_argument('--original-title' , help='Titre original', required=True)
    insert_parser.add_argument('--release-date' , help='Date de sortie en France', required=True)
    insert_parser.add_argument('--rating' , help='Classification du film', choices=('TP', '-12', '-16'), required=True)

args = parser.parse_args()

# People actions
if args.context == "people":

    if args.action == "list":
        people = find_all("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].__dict__.keys())
                for person in people:
                    writer.writerow(person.__dict__.values())
        else:
            for person in people:
                print_person(person)

    if args.action == "find":
        person_id = args.id
        person = find("people", person_id)
        if (person == None):
            print(f"Aucun people n'a été trouvé avec l'id {person_id}")
        else:
            print_person(person)

    if args.action == "insert":
        print(f"Insertion d'une nouvelle personne: {args.firstname} {args.lastname}")
        person = Person(
            args.firstname,
            args.lastname
        )
        person_id = insert_people(person)
        print(f"Nouvelle personne insérée avec l'id {person_id}")

# Movies actions
if args.context == "movies":

    if args.action == "list":  
        movies = find_all("movies")
        for movie in movies:
            print_movie(movie)

    if args.action == "find":  
        movie_id = args.id
        movie = find("movies", movie_id)
        if (movie == None):
            print(f"Aucun film n'a été trouvé avec l'id {movie_id}")
        else:
            print_movie(movie)

    if args.action == "insert":
        print(f"Insertion d'un nouveau film: {args.title}")
        movie = Movie(
            args.title,
            args.original_title,
            args.duration,
            args.rating,
            args.release_date
        )      
        movie_id = insert_movie(movie)
        print(f"Nouveau film inséré avec l'id {movie_id}")

    if args.action == "import":
        with open(args.file, 'r', encoding='utf-8', newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                movie_id = insert_movie(
                    title = row['title'],
                    original_title = row['original_title'],
                    duration = row['duration'],
                    rating = row['rating'],
                    release_date = row['release_date']
                )
                print(f"Nouveau film inséré avec l'id {movie_id}")