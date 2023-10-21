import re
import requests
import json
from globals import HEADERS, BASE_URL

class News:
    def __init__(self):      # n_jobs??
        self.related_news = []
        # self.date = None                 # <span class="article-date">
        # self.author = None               # <span class="article-author">, contains a href with author name
        # self.url = None
        # self.title = None


def get_top_news():
    # Realiza la solicitud GET
    response = requests.get(BASE_URL)

    # Verifica si la solicitud fue exitosa (código de respuesta 200)
    if response.status_code != 200:
        response = "error"

    return response


def extract_related_links(html_text):
    regex = r'<a[^>]*\s*href=["\'](https?://[^"\']+)["\']'
    matches = re.findall(regex, html_text)

    related_links = [link for link in matches if 'www.20minutos.es' in link]

    return related_links


if __name__ == '__main__':
    top_news = get_top_news()
    relevant_links = extract_related_links(top_news.text)

    print(relevant_links)    
    print(type(relevant_links))
