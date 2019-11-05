import requests # to make TMDB API calls
import config # to hide TMDB API keys
import json

api_key = config.tmdb_key # get TMDB API key from config.py file

def movie_search(query):
    url = 'https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&language=fr'
    title = query.replace(' ', '+')
    final_url = url + "&query=" + title
    print(final_url)
    r = requests.get(final_url)
    data = r.json()
    for item in data['results']:
        movie_id = item['id']

        if item['title'] == title:
            url_details = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=' + api_key + '&language=fr'
            # print(url_details)
            r = requests.get(url_details)
            details = r.json()
            print(f"Titre: {details['title']}")
            print(f"Titre original: {details['original_title']}")
            print(f"Durée: {details['runtime']}")
            print(f"Date de sortie: {details['release_date']}")
            print(f"Bénéfices: {details['revenue']}")
            print(f"Synopsis: {details['overview']}")

def movie_search_year(year):
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_key + '&language=fr'
    final_url = url + "&primary_release_year=" + year + '&sort_by=revenue.desc'
    print(final_url)
    req = requests.get(final_url)
    data = req.json()
    #print(data)
    total_pages = data['total_pages']
    print(total_pages)
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
        
        page += 1
            
# movie_search('Ted')

movie_search_year('2018')


