import requests # to make API calls
import config # to hide API keys
import json
from movie import Movie

TMDB_API_KEY = config.tmdb_key # get TMDB API key from config.py file
OMDB_API_KEY = config.omdb_key # get OMDB API key from config.py file


def get_imdb_id(movie_title):
    
    base_url_omdb = 'http://www.omdbapi.com/?'
    final_url_omdb = base_url_omdb + '&apikey=' + OMDB_API_KEY + '&s=' + movie_title 
    
    request_omdb = requests.get(final_url_omdb)
    data_omdb = request_omdb.json()

    print(f"IMDB ID: {data_omdb['Search'][0]['imdbID']}")
    imdb_id = data_omdb['Search'][0]['imdbID']
    return imdb_id

    
def get_movies_by_year(year):

    url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + TMDB_API_KEY
    final_url = url + "&primary_release_year=" + str(year) + '&sort_by=revenue.desc'
    # print(final_url)
    req = requests.get(final_url)
    data = req.json()
    #print(data)
    total_pages = data['total_pages']
    #print(total_pages)

    page = 0
    while page < total_pages:

        for item in data['results']:

            try:
                imdb_id = get_imdb_id(item['title'])

                url_details = f'https://api.themoviedb.org/3/movie/{imdb_id}?api_key=' + TMDB_API_KEY + '&language=fr'
                url_omdb_details = f'http://www.omdbapi.com/?i={imdb_id}&apikey=' + OMDB_API_KEY
                
                print(url_details)
                print(url_omdb_details)
                        
                r = requests.get(url_details)
                r_omdb = requests.get(url_omdb_details)

                details = r.json()
                details_omdb = r_omdb.json()

                print(f"Titre: {details['title']}")
                print(f"Titre original: {details['original_title']}")
                print(f"Durée: {details['runtime']}")
                print(f"Rating: {details_omdb['Rated']}")
                print(f"Date de sortie: {details['release_date']}")
                print(f"Budget: {details['budget']}")
                print(f"Bénéfices: {details['revenue']}")
                print(f"Synopsis: {details['overview']}")
                print("\n")

            
            except KeyError:
                print('Cannot find "movie data"')
                print("\n")
    
        page += 1
            
# movie_search('')

get_movies_by_year(2019)

# get_imdb_id()


