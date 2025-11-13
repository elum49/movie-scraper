import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_html(url):
    response = requests.get(url)
    return response.text

def parse_movies(html):
    soup = BeautifulSoup(html, 'html.parser')
    movies = []
    movie_elements = soup.find_all('div', class_='lister-item')
    
    for movie in movie_elements:
        try:
            title = movie.find('h3').find('a').text
            year = movie.find('span', class_='lister-item-year').text.strip('()')
            rating = movie.find('div', class_='ratings-bar').find('strong').text
            genre = movie.find('span', class_='genre').text.strip()
            
            movies.append({
                'title': title,
                'year': year,
                'rating': float(rating),
                'genre': genre
            })
        except:
            continue
    
    return movies
