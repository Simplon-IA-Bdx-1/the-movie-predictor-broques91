import requests # to make API calls
import config # to hide API keys
import random
import json
import os

from moviefactory import MovieFactory
from person import Person
from movie import Movie

class MovieDatabase:

    def __init__(self, tmdb_api_key, omdb_api_key):
        self.tmdb_api_key = tmdb_api_key
        self.omdb_api_key = omdb_api_key

    def get_imdb_id(self, query):

        """
        Get Imdb ID by movie query
        """
        base_url_omdb = 'http://www.omdbapi.com/?'
        final_url_omdb = base_url_omdb + '&apikey=' + self.omdb_api_key + '&s=' + query 
        # print(final_url_omdb)
        
        request_omdb = requests.get(final_url_omdb)
        response = request_omdb.status_code
        if response == 200:
            data_omdb = request_omdb.json()
            if data_omdb['Response'] == "True":
                # print(f"IMDB ID: {data_omdb['Search'][0]['imdbID']}")
                result = data_omdb['Search'][0]['imdbID']
            else:
                result = "IMDb ID not found"
        else:
            print("Request failed")
        return result

    def rating_movies(self, rating):
        if rating == "G" or rating == "PG" or rating == "PG-13":
            rating_fr = "TP"
        elif rating == "NC-17" or rating == "R":
            rating_fr = "-12"
        else:
            rating_fr = "-16"

        return rating_fr

    def get_random_movie(self):

        url = 'https://api.themoviedb.org/3/movie/latest?api_key=' + self.tmdb_api_key
        req_prepare = requests.get(url)
        data_prepare = req_prepare.json()
        latest_id = data_prepare['id']

        response = None
        
        while response != 200:

            random_id = random.randrange(latest_id)
            final_url = f'https://api.themoviedb.org/3/movie/{random_id}?api_key=' + self.tmdb_api_key
            req = requests.get(final_url)
            response = req.status_code

            if response == 404:
                continue

            data = req.json()
            print(final_url)

            imdb_id = self.get_imdb_id(data['title'])
            print(imdb_id)

            if imdb_id == "IMDb ID not found" or imdb_id == None:
                continue

            url_tmdb_details = f'https://api.themoviedb.org/3/movie/{imdb_id}?api_key=' + self.tmdb_api_key + '&language=fr'
            url_omdb_details = f'http://www.omdbapi.com/?i={imdb_id}&apikey=' + self.omdb_api_key

            print(url_tmdb_details)
            print(url_omdb_details)
                    
            r_tmdb = requests.get(url_tmdb_details)
            r_omdb = requests.get(url_omdb_details)

            details_tmdb = r_tmdb.json()
            details_omdb = r_omdb.json()

            movie_id = MovieFactory().insert(
                        Movie(
                            title = details_tmdb['title'],
                            original_title = details_tmdb['original_title'],
                            synopsis = details_tmdb['overview'],
                            duration = details_tmdb['runtime'],
                            rating = self.rating_movies(details_omdb['Rated']),
                            release_date = details_tmdb['release_date'],
                            imdb_id = details_tmdb['imdb_id']
                            # print(f"Budget: {details['budget']}")
                            # print(f"Bénéfices: {details['revenue']}")
                            # print(f"Synopsis: {details['overview']}")
                        )
                    )
            print(f"Nouveau film '{details_tmdb['title']}' inséré avec l'id {movie_id}")

            if response == 200: 
                break

    def get_movies_by_year(self, year):

        url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + self.tmdb_api_key
        final_url = url + "&primary_release_year=" + str(year) + '&sort_by=revenue.desc'

        req = requests.get(final_url)
        data = req.json()

        total_pages = data['total_pages']

        page = 0
        while page < total_pages:

            for item in data['results']:

                try:
                    imdb_id = get_imdb_id(item['title'])

                    url_details = f'https://api.themoviedb.org/3/movie/{imdb_id}?api_key=' + self.tmdb_api_key + '&language=fr'
                    url_omdb_details = f'http://www.omdbapi.com/?i={imdb_id}&apikey=' + self.omdb_api_key

                    print(url_details)
                    print(url_omdb_details)
                            
                    r = requests.get(url_details)
                    r_omdb = requests.get(url_omdb_details)

                    details = r.json()
                    details_omdb = r_omdb.json()

                    movie_id = MovieFactory().insert(
                        Movie(
                            title = details['title'],
                            original_title = details['original_title'],
                            synopsis = details['overview'],
                            duration = details['runtime'],
                            rating = rating_movies(details_omdb['Rated']),
                            release_date = details['release_date']
                            # print(f"Budget: {details['budget']}")
                            # print(f"Bénéfices: {details['revenue']}")
                            # print(f"Synopsis: {details['overview']}")
                        )
                    )
                    print(f"Nouveau film inséré avec l'id {movie_id}")
        
                except KeyError:
                    print('Cannot find "movie data"')
                    print("\n")
        
            page += 1

    def split_fullname(self, fullname):

        """
        Get firstname and lastname of person by fullname
        """
        fullname = fullname.strip().split(" ")      
        if len(fullname) == 3:
            firstname = fullname[0] + ' ' + fullname[1]
            lastname = fullname[2]
        else:
            firstname = fullname[0]
            lastname = fullname[1]
        person = Person(firstname,lastname)
        return person

    def get_people_by_movie(self, movie_title):

        """
        Get people by movie (actors, directors, writers)  
        """

        # get imdb ID of the movie 
        imdb_id = self.get_imdb_id(movie_title)
        url_omdb_details = f'http://www.omdbapi.com/?i={imdb_id}&apikey=' + self.omdb_api_key

        r_omdb = requests.get(url_omdb_details)
        details_omdb = r_omdb.json()

        # Actors
        actors = details_omdb['Actors'].split(",")
        for actor in actors:
            actor = actor.strip()
            actor = actor.split(" ")
            # print(actor)
            if len(actor) == 3:
                firstname = actor[0] + ' ' + actor[1]
                lastname = actor[2]
            else:
                firstname = actor[0]
                lastname = actor[1]
            print(f"Actor: {firstname}, {lastname}")

        # Directors
        directors = details_omdb['Director'].split(",")
        for director in directors:
            director = directors.strip()
            director = directors.split(" ")
            firstname_d = director[0]
            lastname_d = director[1]
            print(f"Director: {firstname_d}, {lastname_d}")

        # Writers
        writers = details_omdb['Writer'].split(",")
        for writer in writers:
            writer = writer.strip()
            writer = writer.split(" ")
            firstname_w = writer[0]
            lastname_w = writer[1]
            print(f"Writer: {firstname_w}, {lastname_w}")