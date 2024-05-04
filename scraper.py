import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_movies():
    url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:audience_highest?page=4"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    movies = []

    for film in soup.find_all('a', attrs={'data-qa': 'discovery-media-list-item-caption'}):
        try:
            title_element = film.find('span', {'data-qa': 'discovery-media-list-item-title'})
            if not title_element:
                continue
            title = title_element.get_text(strip=True)

            release_date_element = film.find('span', {'data-qa': 'discovery-media-list-item-start-date'})
            if not release_date_element:
                continue
            date_text = release_date_element.getText(strip=True)
            date_info = date_text.split(' ')[1:]  # remove the first "open"
            month_name = date_info[0]
            month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
            month = month_dict[month_name]  # transfer to integer format
            day = int(date_info[1][:-1])  # remove the comma
            year = int(date_info[2])
            release_date = datetime(year, month, day)

            scores = film.find('score-pairs-deprecated')
            if not scores:
                continue
            audience_score = scores.get('audiencescore')
            critics_score = scores.get('criticsscore')
            if audience_score and critics_score:
                score = (int(audience_score) + int(critics_score)) / 2
            elif audience_score:
                score = int(audience_score)
            elif critics_score:
                score = int(critics_score)
            else:
                continue  # No score available

            movies.append((title, release_date, score))
        except Exception as e:
            print(f"Error processing a movie block: {str(e)}")
            continue

    return movies