import requests # to make API calls
import config # to hide API keys
import json
from movie import Movie

api_key = config.tmdb_key # get TMDB API key from config.py file
omdb_key = config.omdb_key # get OMDB API key from config.py file

def movie_search(query):
    url = 'https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&language=fr'
    title = query.replace(' ', '+')

    final_url_tmdb = url + "&query=" + title
    final_url_omdb = 'http://www.omdbapi.com/?s=' + title + '?&apikey=' + omdb_key + '&language=fr'
    
    # Requests
    r_tmdb = requests.get(final_url_tmdb)
    r_omdb = requests.get(final_url_omdb)

    # Convert data to JSON
    data_tmdb = r_tmdb.json()
    data_omdb = r_omdb.json()

    # Import data from OMDB API
    for item in data_omdb['Search']:
        imdb_id = item['imdbID']

        if item['Title'] == title:
            url_omdb_details = f'http://www.omdbapi.com/?i={imdb_id}&apikey=' + omdb_key
            print(url_omdb_details)
            r_omdb = requests.get(url_omdb_details)
            details_omdb = r_omdb.json()
            #print(details_omdb)
            
    # Import data from TMDB API
    for item in data_tmdb['results']:
        imdb_id = item['id']

        if item['title'] == title:
            url_tmdb_details = f'https://api.themoviedb.org/3/movie/{imdb_id}?api_key=' + api_key + '&language=fr'
            print(url_tmdb_details)
            r_tmdb = requests.get(url_tmdb_details)
            details_tmdb = r_tmdb.json()

    print(f"Titre: {details_tmdb['title']}")
    print(f"Titre original: {details_tmdb['original_title']}")
    print(f"Durée: {details_tmdb['runtime']}")
    print(f"Rating: {details_omdb['Rated']}")
    print(f"Date de sortie: {details_tmdb['release_date']}")
    print(f"Bénéfices: {details_tmdb['revenue']}")
    print(f"Budget: {details_tmdb['budget']}")
    print(f"Synopsis: {details_tmdb['overview']}")
    

def movie_search_year(year):
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_key + '&language=fr'
    final_url = url + "&primary_release_year=" + year + '&sort_by=revenue.desc'
    print(final_url)
    req = requests.get(final_url)
    data = req.json()
    #print(data)
    total_pages = 3
    #print(total_pages)

    page = 0
    while page < total_pages:

        for item in data['results']:

            movie_id = item['id']
            url_details = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=' + api_key + '&language=fr'
                    
            r = requests.get(url_details)
            details = r.json()
            print(f"Titre: {details['title']}")
            print(f"Titre original: {details['original_title']}")
            print(f"Durée: {details['runtime']}")
            print(f"Date de sortie: {details['release_date']}")
            print(f"Bénéfices: {details['revenue']}")
            print(f"Synopsis: {details['overview']}")
            print("\n")
        
        page += 1
            
movie_search('Ted')

#movie_search_year('2018')


