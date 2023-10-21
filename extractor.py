import re
import requests
import pandas as pd
from globals import HEADERS, BASE_URL, MAX_DEPTH


def get_page_text(url: str) -> str:
    """
        Gets a news page in plain HTML as a string, for depth 0 news.

        Parameters: a string representing a URL
        Returns: string
    """
    response = requests.get(url)

    if response.status_code != 200:
        response = "error"

    return response.text


def crawl_links(url: str, depth: int):
    """
        Crawls through every link in the list to get related news to the
        specified depth.

        Parameters: URL (string), depth (int)
        Returns: itself XD

        [!!!!!!!!!] Problems: depth is not properly calculated
    """
    if depth == 0:
        return 

    html_text = get_page_text(url)
    news_links = get_related_links(html_text)

    # God forgive me for what I am about to code
    global news_data
    for link in news_links:
        news_data = news_data._append({'link': link, 'depth': MAX_DEPTH - depth}, ignore_index=True)

    # Recursively crawl related links
    for link in news_links:
        crawl_links(link, depth - 1)



def get_related_links(html_text: str) -> list:
    """
        Extracts news links from a page, be it the landing page or any news page.
        By news we understand exclusively this newspaper's articles.
        This is achieved by detecting <a> tags and extracting the links they contain.
        
        Parameters: HTML text as a string
        Returns: list
    """
    regex = r'<a[^>]*\s*href=["\'](https?://[^"\']+)["\']'
    matches = re.findall(regex, html_text)

    related_links = [link for link in matches if 'www.20minutos.es/noticia/' in link]

    return related_links



if __name__ == '__main__':
    news_data = pd.DataFrame(columns=['link', 'depth'])

    # This is the starting point to get the first batch of links to news. 
    landing_page_news = get_page_text(BASE_URL)
    news_links = get_related_links(landing_page_news)



    # Crawl related links with the specified depth
    for link in news_links:
        crawl_links(link, MAX_DEPTH)


    print(news_data)

