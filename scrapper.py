import requests
import locale

from bs4 import BeautifulSoup
from datetime import datetime

# Scrapper
locale.setlocale(locale.LC_ALL, 'fr_FR')

url = 'https://fr.wikipedia.org/wiki/Joker_(film,_2019)'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

fiche_technique = soup.find(id="Fiche_technique")

h2_tag = fiche_technique.parent
ul_tag = h2_tag.find_next_sibling('ul')
li_tags = ul_tag.find_all('li')

for li_tag in li_tags:
    splitted_li = li_tag.get_text().split(':')
    data_type = splitted_li[0].strip()
    data_value = splitted_li[1].strip()

    if data_type == "Titre original":
        title = data_value
    if data_type == "Durée":
        duration = data_value.replace('minutes', '').strip()
    if data_type == "Date de sortie":
        release_dates_li_list = li_tag.find_all("li")
        for release_date_li in release_dates_li_list:
            release_date_splitted = release_date_li.get_text().split(':')
            release_country = release_date_splitted[0].strip()
            release_date_as_string = release_date_splitted[1].strip()
            if release_country == "France":
                release_date_object = datetime.strftime(release_date_as_string, '%d %B %Y')
                release_date_sql_string = release_date_object.strftime('%Y-%m-%d')
                # print('Sortie en France:', release_date_sql_string)          
    if data_type == "Classification":
        rating_li_list = li_tag.find_all("li")
        for rating_li in rating_li_list:
            rating_splitted = rating_li.get_text().split(':')
            rating_country = rating_splitted[0].strip()
            rating_string = rating_splitted[1].strip()
            if rating_country == "France":
                if rating_string.find('12') != -1:
                    rating = '-12'
                    
print('title =', title)
print('duration =', duration)
print('release_date =', release_date_sql_string)
print('rating =', rating)