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
def analyze_movies(movies_list):
    df = pd.DataFrame(movies_list)
    df_sorted = df.sort_values('rating', ascending=False)
    df_filtered = df_sorted[df_sorted['rating'] > 8.0]
    
    print(f"Всего фильмов: {len(df)}")
    print(f"Средний рейтинг: {avg_rating:.2f}")
    print(f"Фильмов с рейтингом > 8.0: {len(df_filtered)}")
    
    return df_filtered
def main():
    url = "https://www.imdb.com/chart/top/"
    
    print("Начинаем скрапинг...")
    html = get_html(url)
    movies = parse_movies(html)
    result_df = analyze_movies(movies)
    result_df.to_csv('top_movies.csv', index=False)
    print("Данные сохранены в файл: top_movies.csv")
    print("\nТоп-5 фильмов:")
    print(result_df.head())

if __name__ == "__main__":
    main()
