import requests
import time
import csv
import re
import random
import concurrent.futures
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

MAX_THREADS = 10

def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    try:
      response = requests.get(movie_link, headers=headers)
      response.raise_for_status()
      movie_soup = BeautifulSoup(response.content, 'html.parser')

      title = None
      date = None
      rating = None
      plot_text = None

      movie_data = movie_soup.find('section', attrs={'class': 'sc-9a2a0028-2'})
      if movie_data:
        title_element = movie_data.find('span', attrs={'class': 'hero__primary-text'})
        if title_element:
          title = title_element.get_text().strip()
        date_element = movie_data.find('a', {'class': 'ipc-link', 'href': re.compile(r'/releaseinfo/')})
        if date_element:
          date = date_element.get_text().strip()
        rating_element = movie_soup.find('span', attrs={'class': 'sc-d541859f-1'})
        if rating_element:
          rating = rating_element.get_text().strip()

        plot_text_element = movie_soup.find('span', attrs={'class': 'sc-42125d72-0'})
        if plot_text_element:
          plot_text = plot_text_element.get_text().strip().replace('\n', '')
          print(plot_text)

    

      if all([title, date, rating, plot_text]):
        with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
          movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
          movie_writer.writerow([title, date, rating, plot_text])
      else:
        print("Detalhes incompletos, filme não adicionado.")  
        
    except requests.exceptions.RequestException as e:
      print(f"Erro na solicitação para {movie_link}: {e}")
    except AttributeError as e:
      print(f"Atributo não encontrado em {movie_link}: {e}")
    except Exception as e:
      print(f"Erro desconhecido em {movie_link}: {e}")

def extract_movies(soup):
    try:
      movies_list = soup.find('ul', {'class': 'ipc-metadata-list'})
      if movies_list:
        movies_list_items = movies_list.find_all('li')
        movie_links = ['https://imdb.com' + item.find('a')['href'] for item in movies_list_items if item.find('a')]
      else:
        print("Erro: Não foi possível encontrar a lista de filmes.")
        movie_links = []  


      if movie_links:
        threads = min(MAX_THREADS, len(movie_links))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
          executor.map(extract_movie_details, movie_links)
      else:
        print("Erro: Nenhum link de filme encontrado.")

    except Exception as e:
      print(f"Erro ao extrair links dos filmes: {e}")

def main():
    start_time = time.time()
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    try:
        response = requests.get(popular_movies_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        extract_movies(soup)
    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação inicial: {e}")
    except Exception as e:
        print(f"Erro desconhecido na função main: {e}")

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)

if __name__ == '__main__':
    main()