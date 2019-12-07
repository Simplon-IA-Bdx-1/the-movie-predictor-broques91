import requests # to make API calls
import config # to hide API keys
import random
import json
import os

from peoplefactory import PeopleFactory
from companyfactory import CompanyFactory
from moviefactory import MovieFactory
from moviepeoplerolefactory import MoviePeopleRoleFactory
from moviecompaniesrolefactory import MovieCompaniesRoleFactory
from person import Person
from company import Company
from movie import Movie

class MovieDatabase:

    def __init__(self, tmdb_api_key, omdb_api_key):
        self.tmdb_api_key = tmdb_api_key
        self.omdb_api_key = omdb_api_key

    def get_imdb_id(self, query):

        """
        Return the IMDb ID of the movie
        """
        base_url_omdb = 'http://www.omdbapi.com/?'
        final_url_omdb = base_url_omdb + '&apikey=' + str(self.omdb_api_key) + '&s=' + query 
        
        request_omdb = requests.get(final_url_omdb)
        response = request_omdb.status_code
        if response == 200:
            data_omdb = request_omdb.json()
            if data_omdb['Response'] == "True":
                result = data_omdb['Search'][0]['imdbID']
            else:
                result = "IMDb ID not found"
        else:
            result = "Request failed"
        return result

    def rating_movies(self, rating):
        if rating == "G" or rating == "PG":
            rating_fr = "TP"
        elif rating == "PG-13" or rating == "R":
            rating_fr = "-12"
        elif rating == "NC-17":
            rating_fr = "-16"
        else:
            rating_fr = ""

        return rating_fr

    def get_random_movie(self):

        """
        Return random movie with API call
        """

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

            # Si erreur 404 passe au tour de boucle suivant
            if response == 404:
                continue

            data = req.json()
            print(final_url)

            imdb_id = self.get_imdb_id(data['title'])
            print(imdb_id)

            # Si aucun IMDb n'a été trouvé, passe au tour de boucle suivant
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
                            rating = details_omdb['Rated'],
                            release_date = details_tmdb['release_date'],
                            budget = details_tmdb['budget'],
                            revenue = details_tmdb['revenue'],
                            imdb_id = details_tmdb['imdb_id'],
                            score = details_tmdb['vote_average']
                        )
                    )
            print(f"Nouveau film '{details_tmdb['title']}' inséré avec l'id {movie_id}")


            # Actors
            actors = details_omdb['Actors'].split(",")
            for actor in actors:
                actor = actor.strip().split(" ")

                if len(actor) == 3:
                    firstname_a = actor[0] + ' ' + actor[1]
                    lastname_a = actor[2]
                else:
                    firstname_a = actor[0]
                    lastname_a = actor[1]
                
                person_id = PeopleFactory().insert(
                    Person(
                        firstname = firstname_a,
                        lastname = lastname_a
                    )
                )
                print(f"{firstname_a} {lastname_a} inséré avec l'id {person_id}")

                MoviePeopleRoleFactory().insert(
                    movie_id = movie_id,
                    person_id = person_id,
                    role_id = 1
                )

            # Directors

            directors = details_omdb['Director'].split(",")
            for director in directors:
                director = director.strip().split(" ")
                if len(director) == 3:
                    firstname_d = director[0] + ' ' + director[1]
                    lastname_d = director[2]
                else:
                    firstname_d = director[0]
                    lastname_d = director[1]
                

                person_id = PeopleFactory().insert(
                    Person(
                        firstname = firstname_d,
                        lastname = lastname_d
                    )
                )
                print(f"{firstname_d} {lastname_d} inséré avec l'id {person_id}")

                MoviePeopleRoleFactory().insert(
                        movie_id = movie_id,
                        person_id = person_id,
                        role_id = 2
                    )

            # Writers

            writers = details_omdb['Writer'].replace('(screenplay by)', '').replace('(screenplay)', '').replace('(story)', '').split(",")      
            for writer in writers:
                writer = writer.strip().split(" ")

                if len(writer) == 3:
                    firstname_w = writer[0] + ' ' + writer[1]
                    lastname_w = writer[2]
                else:
                    firstname_w = writer[0]
                    lastname_w = writer[1]
                print(f"Writer: {firstname_w} {lastname_w}")

                person_id = PeopleFactory().insert(
                    Person(
                        firstname = firstname_w,
                        lastname = lastname_w
                    )
                )
                print(f"{firstname_w} {lastname_w} inséré avec l'id {person_id}")

                MoviePeopleRoleFactory().insert(
                    movie_id = movie_id,
                    person_id = person_id,
                    role_id = 3
                )

            # Companies
            companies_name = details_omdb['Production']
            company_id = CompanyFactory().insert(
                Company(
                    name = companies_name
                    )
            )
            print(f"{companies_name} inséré avec l'id {company_id}")

            MovieCompaniesRoleFactory().insert(
                movie_id = movie_id,
                company_id = company_id,
                role_id = 4
            )

            if response == 200: 
                break

    def get_movies_by_year(self, year):

        """
        Return movies by year with API call
        """

        url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + str(self.tmdb_api_key)
        final_url = url + "&primary_release_year=" + str(year) + '&sort_by=revenue.desc'
        print(final_url)

        req = requests.get(final_url)
        data = req.json()
        print(data)

        total_pages = data['total_pages']

        page = 0
        while page < total_pages:

            for item in data['results']:

                try:
                    imdb_id = self.get_imdb_id(item['title'])

                    url_tmdb_details = f'https://api.themoviedb.org/3/movie/{imdb_id}?api_key=' + str(self.tmdb_api_key) + '&language=fr'
                    url_omdb_details = f'http://www.omdbapi.com/?i={imdb_id}&apikey=' + str(self.omdb_api_key)

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
                            budget = details_tmdb['budget'],
                            revenue = details_tmdb['revenue'],
                            imdb_id = details_tmdb['imdb_id'],
                            score = details_tmdb['vote_average']
                        )
                    )
                    print(f"Nouveau film inséré avec l'id {movie_id}")

                    # Actors
                    actors = details_omdb['Actors'].split(",")
                    for actor in actors:
                        actor = actor.strip().split(" ")

                        if len(actor) == 3:
                            firstname_a = actor[0] + ' ' + actor[1]
                            lastname_a = actor[2]
                        else:
                            firstname_a = actor[0]
                            lastname_a = actor[1]
                        
                        person_id = PeopleFactory().insert(
                            Person(
                                firstname = firstname_a,
                                lastname = lastname_a
                            )
                        )
                        print(f"{firstname_a} {lastname_a} inséré avec l'id {person_id}")

                        MoviePeopleRoleFactory().insert(
                            movie_id = movie_id,
                            person_id = person_id,
                            role_id = 1
                        )

                    # Directors
                    directors = details_omdb['Director'].split(",")
                    for director in directors:
                        director = director.strip().split(" ")
                        if len(director) == 3:
                            firstname_d = director[0] + ' ' + director[1]
                            lastname_d = director[2]
                        else:
                            firstname_d = director[0]
                            lastname_d = director[1]

                        person_id = PeopleFactory().insert(
                            Person(
                                firstname = firstname_d,
                                lastname = lastname_d
                            )
                        )
                        print(f"{firstname_d} {lastname_d} inséré avec l'id {person_id}")

                        MoviePeopleRoleFactory().insert(
                                movie_id = movie_id,
                                person_id = person_id,
                                role_id = 2
                            )

                    # Writers
                    writers = details_omdb['Writer'].replace('(screenplay by)', '').replace('(story)', '').split(",")      
                    for writer in writers:
                        writer = writer.strip().split(" ")

                        if len(writer) == 3:
                            firstname_w = writer[0] + ' ' + writer[1]
                            lastname_w = writer[2]
                        else:
                            firstname_w = writer[0]
                            lastname_w = writer[1]
                        print(f"Writer: {firstname_w} {lastname_w}")

                        person_id = PeopleFactory().insert(
                            Person(
                                firstname = firstname_w,
                                lastname = lastname_w
                            )
                        )
                        print(f"{firstname_w} {lastname_w} inséré avec l'id {person_id}")

                        MoviePeopleRoleFactory().insert(
                            movie_id = movie_id,
                            person_id = person_id,
                            role_id = 3
                        )

                        # Companies
                        companies = details_omdb['Production']
                        company_id = CompanyFactory().insert(
                            Company(
                                name = companies
                                )
                        )
                        print(f"{companies} inséré avec l'id {company_id}")


                        MovieCompaniesRoleFactory().insert(
                            movie_id = movie_id,
                            company_id = company_id,
                            role_id = 4
                        )

                except KeyError:
                    print('Cannot find "movie data"')
                    print("\n")
        
            page += 1

    def split_fullname(self, fullname):

        """
        Return firstname and lastname of person
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
        Return people by movie (actors, directors, writers)  
        """

        # Get IMDb ID of the movie 
        imdb_id = self.get_imdb_id(movie_title)
        url_omdb_details = f'http://www.omdbapi.com/?i={imdb_id}&apikey=' + self.omdb_api_key

        r_omdb = requests.get(url_omdb_details)
        details_omdb = r_omdb.json()

        # Actors
        actors = details_omdb['Actors'].split(",")
        for actor in actors:
            actor = actor.strip()
            actor = actor.split(" ")

            if len(actor) == 3:
                firstname = actor[0] + ' ' + actor[1]
                lastname = actor[2]
            else:
                firstname = actor[0]
                lastname = actor[1]

            print(f"Actor: {firstname}, {lastname}")
            
            movie.role = "actor"
            person_id = PeopleFactory().insert(
                Person(
                    firstname = firstname,
                    lastname = lastname
                )
            )
            print(f"{firstname} {lastname} inséré avec l'id {person_id}")

                
        # Directors
        directors = details_omdb['Director'].split(",")
        for director in directors:
            director = director.strip()
            director = director.split(" ")
            firstname_d = director[0]
            lastname_d = director[1]
            Person.role = "director"
            print(f"Director: {firstname_d}, {lastname_d}")

            movie.role = "director"
            person_id = PeopleFactory().insert(
                Person(
                    firstname = firstname,
                    lastname = lastname
                )
            )
            print(f"{firstname} {lastname} inséré avec l'id {person_id}")

        # Writers
        writers = details_omdb['Writer'].split(",")
        for writer in writers:
            writer = writer.strip()
            writer = writer.split(" ")
            firstname_w = writer[0]
            lastname_w = writer[1]
            Person.role = "writer"
            print(f"Writer: {firstname_w}, {lastname_w}")

            movie.role = "writer"
            person_id = PeopleFactory().insert(
                Person(
                    firstname = firstname,
                    lastname = lastname
                )
            )
            print(f"{firstname} {lastname} inséré avec l'id {person_id}")