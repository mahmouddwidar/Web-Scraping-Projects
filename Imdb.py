# Getting the Best 1000 Movies

import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
import csv

name = []
description = []
genre = []
director = []
txt = ''
movies = []
actors = []
year = []
source = []

page_num = 0


while True:
    url = f'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start={page_num}01&ref_=adv_nxt'
    page = requests.get(url)
    src = page.content
    soup = BeautifulSoup(src, 'lxml')

    page_limit = 9

    if page_num > page_limit:
        print("Pages ended, wait for file creation...")
        break

    ######################################
    ####### Name, Year and Source ########
    ######################################

    names = soup.find_all('h3', {"class": 'lister-item-header'})

    for i in range(len(names)):
        name.append(names[i].a.text.strip())
        source.append('https://www.imdb.com/' + names[i].a.attrs['href'])
        year.append(names[i].find('span', {'class': 'lister-item-year'}).text.strip())


    ######################################
    ######## Description, Genre ##########
    ######## Director and Stars ##########
    ######################################

    descriptions = soup.find_all('div', {'class': 'lister-item-content'})

    for i in range(len(descriptions)):
        description.append(descriptions[i].contents[7].text.strip())
        genre.append(descriptions[i].find('p').find('span', {'class': 'genre'}).text.strip())
        director.append(descriptions[i].contents[9].a.text.strip())
        movies.append(descriptions[i].contents[9].text.strip())

    page_num += 1
    print(f"Page Switched [{page_num}].")
    
for movie in movies:
        star_index = movie.find("Stars:") + 6
        stars = movie[star_index:].strip().replace('\n','')
        actors.append(stars)

file_list = [name, description, genre, director, actors, year, source]
exported = zip_longest(*file_list)

with open(r"File_Path\All_Data.csv", "w", encoding='utf-8-sig', newline='') as output_file:
    wr = csv.writer(output_file)
    wr.writerow(["Title", "Description", "Genre", "Director", "Key Actors", "Year", "Source"])
    wr.writerows(exported)
    print("File Created.")

# Coded By Mahmoud Dwidar
# Date: 8:22 PM 22/04/2023
# Eid Mubarak <3
# LinkedIn ==> https://www.linkedin.com/in/mahmoud-dwidar-2000/