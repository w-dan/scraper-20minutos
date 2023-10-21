import re
import requests
import pandas as pd
from globals import HEADERS, BASE_URL

class News:
    def __init__(self):      # n_jobs??
        self.related_news = []
        # self.date = None                 # <span class="article-date">
        # self.author = None               # <span class="article-author">, contains a href with author name
        # self.url = None
        # self.title = None


def get_page_text(url: str) -> str:
    """
        Gets a news page in plain HTML as a string, for depth 0 news.
        This is the starting point to get the first batch of links to news. 

        Returns: string
    """
    response = requests.get(url)

    if response.status_code != 200:
        response = "error"

    return response.text


def extract_related_links(html_text: str) -> list:
    """
        Extracts news links from a page, be it the landing page or any news page.
        By news we understand exclusively this newspaper's articles.
        This is achieved by detecting <a> tags and extracting the links they contain.
        
        Parameters: a string object 
        Returns: list
    """
    regex = r'<a[^>]*\s*href=["\'](https?://[^"\']+)["\']'
    matches = re.findall(regex, html_text)

    related_links = [link for link in matches if 'www.20minutos.es/noticia/' in link]

    return related_links


if __name__ == '__main__':
    data = pd.DataFrame(columns=['link', 'depth'])
    main_news = get_page_text(BASE_URL)
    relevant_links = extract_related_links(main_news)

    print("----------------------------------------------------------------------------------")
    print(relevant_links)    
    print("----------------------------------------------------------------------------------")
    print(type(relevant_links))
    print(len(relevant_links))
