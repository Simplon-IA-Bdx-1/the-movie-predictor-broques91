#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Arnaud de Mouhy <arnaud@admds.net>
"""

import mysql.connector
import sys
import argparse
import csv

def connect_to_database():
    return mysql.connector.connect(user='predictor', password='predictor', host='127.0.0.1', database='predictor')

def disconnect_database(cnx):
    cnx.close()

def create_cursor(cnx):
    return cnx.cursor(dictionary=True)

def close_cursor(cursor):    
    cursor.close()

def find_query(table, id):
    return ("SELECT * FROM {} WHERE id = {}".format(table, id))

def find_all_query(table):
    return ("SELECT * FROM {}".format(table))

def find(table, id):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    query = find_query(table, id)
    cursor.execute(query)
    results = cursor.fetchall()
    close_cursor(cursor)
    disconnect_database(cnx)
    return results

def find_all(table):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(find_all_query(table))
    results = cursor.fetchall()
    close_cursor(cursor)
    disconnect_database(cnx)
    return results


def insert_people(firstname, lastname):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    sql = "INSERT INTO people (firstname, lastname) VALUES (%s, %s)"
    val = (firstname, lastname)
    cursor.execute(sql, val)
    cnx.commit()
    print("People ajouté avec succès !")
    close_cursor(cursor)
    disconnect_database(cnx)

def insert_movie(title, duration, original_title, rating, release_date):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    sql = "INSERT INTO movies (title, duration, original_title, rating, release_date) VALUES (%s, %s, %s, %s, %s)"
    val = (title, duration, original_title, rating, release_date)
    cursor.execute(sql, val)
    cnx.commit()
    print("Film ajouté avec succès !")
    close_cursor(cursor)
    disconnect_database(cnx)


def import_data(csv_file_name):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    with open(args.file) as csv_data_file:
        csv_reader = csv.reader(csv_data_file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute("INSERT INTO movies (title, original_title, duration, rating, release_date) VALUES (%s, %s, %s, %s, %s)", row)
    cnx.commit()
    print("Données importées avec succès !")
    close_cursor(cursor)
    disconnect_database(cnx)


def print_person(person):
    print("#{}: {} {}".format(person['id'], person['firstname'], person['lastname']))


def print_movie(movie):
    print("#{}: {} released on {}".format(movie['id'], movie['title'], movie['release_date']))

parser = argparse.ArgumentParser(description='Process MoviePredictor data')

parser.add_argument('context', choices=['people', 'movies'], help='Le contexte dans lequel nous allons travailler')

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitÃ©es du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exportÃ©')

find_parser = action_subparser.add_parser('find', help='Trouve une entitÃ© selon un paramÃ¨tre')
find_parser.add_argument('id' , help='Identifant Ã  rechercher')

insert_parser = action_subparser.add_parser('insert', help='Insérer une entitÃ© selon un paramÃ¨tre')
insert_parser.add_argument('--firstname' ,help='Prénom')
insert_parser.add_argument('--lastname', help='Nom')
insert_parser.add_argument('--title', help='Titre')
insert_parser.add_argument('--duration', help='Durée')
insert_parser.add_argument('--original-title', help='Titre original')
insert_parser.add_argument('--rating', help='Classification')
insert_parser.add_argument('--release-date', help='Date de sortie')

import_parser = action_subparser.add_parser('import', help='Importer une entitÃ© selon des paramÃ¨tres')
import_parser.add_argument('--file' , help='Nom du fichier importé')

args = parser.parse_args()

if args.context == "people":
    if args.action == "list":
        people = find_all("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].keys())
                for person in people:
                    writer.writerow(person.values())
        else:
            for person in people:
                print_person(person)
    if args.action == "find":
        people_id = args.id
        people = find("people", people_id)
        for person in people:
            print_person(person)
    if args.action == "insert":
        people_firstname = args.firstname
        people_lastname = args.lastname
        insert_people(people_firstname, people_lastname)

if args.context == "movies":
    if args.action == "list":  
        movies = find_all("movies")
        for movie in movies:
            print_movie(movie)
    if args.action == "find":  
        movie_id = args.id
        movies = find("movies", movie_id)
        for movie in movies:
            print_movie(movie)
    if args.action == "insert":
        movie_title = args.title
        movie_duration = args.duration
        movie_original_title = args.original_title
        movie_rating = args.rating
        movie_release_date = args.release_date
        insert_movie(
            movie_title, 
            movie_duration, 
            movie_original_title, 
            movie_rating, 
            movie_release_date
        )
    if args.action == "import":
        csv_file_name = args.file
        import_data(csv_file_name)