import re
import json
import requests
from itertools import chain
from multiprocessing import Manager, Pool, cpu_count
from globals import HEADERS, BASE_URL, MAX_DEPTH


def get_page_text(url: str) -> str:
    """
    Gets the content of a web page as a string.

    Parameters:
        url (str): A string representing the URL of the web page to fetch.

    Returns:
        str: The content of the web page as a string, or an empty string on error.
    """
    with requests.Session() as session:
        try:
            response = session.get(url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx HTTP status codes
            return response.text
        except requests.exceptions.RequestException as e:
            # Handle any request-related exceptions here
            print(f"An error occurred while fetching the page: {e}")
        except Exception as e:
            # Handle other unexpected exceptions here
            print(f"An unexpected error occurred: {e}")
    
    return None  # Return an empty string in case of error

def get_related_links(html_text: str) -> list:
    """
        Extracts news links from a page, be it the landing page or any news page.
        By news we understand exclusively this newspaper's articles.
        This is achieved by detecting <a> tags and extracting the links they contain.
        
        Parameters: HTML text as a string
        Returns: list
    """
    if html_text is None or html_text == "":
        return []

    regex = r'<a[^>]*\s*href=["\'](https?://[^"\']+)["\']'
    matches = re.findall(regex, html_text)

    related_links = [link for link in matches if 'www.20minutos.es/noticia/' in link]

    return related_links

# another approach is a map where the index is the depth
def crawl_links(urls: list):
    links = []
    for url in urls:
        html_text = get_page_text(url)
        news_links = get_related_links(html_text)
        # print(url, len(html_text), len(news_links))
        links.extend(news_links)

    return links

def list_of_lists_to_json(data_list, output_file):
    json_data = {}
    
    for i, values in enumerate(data_list):
        key = str(i)  # Convert the index to a string for the JSON key
        json_data[key] = values

    with open(output_file, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

def execute_search(to_json = True):
    landing_page_news = get_page_text(BASE_URL)
    news_links = get_related_links(landing_page_news)

    manager = Manager()
    link_map = manager.list()
    new_link_map = manager.list()
    link_map.append(news_links)
    new_link_map = link_map[0]

    cpus = cpu_count() - 1

    print("#"*50)
    print("CPUs:", cpus)
    print("MAX_DEPTH:", MAX_DEPTH)
    print("#"*50)
    print("Length of depth 0", len(link_map[0]))
    print("-"*50)
    with Pool(processes=cpus) as pool:
        for _ in range(0, MAX_DEPTH - 1):
            size = len(new_link_map) // cpus
            args_list = []
            results = []

            for i in range(cpus):
                init = i * size
                last = init + size
                args_list.append(new_link_map[init:last])

            print("Arg list", [len(args) for args in args_list])
            try:
                results = pool.map(crawl_links, args_list)
                print("Results", [len(result) for result in results])
            except Exception as e:
                # Handle exceptions in child processes here
                print(f"Exception in child process: {e}")

            new_link_map = list(chain.from_iterable(results))

            if to_json:
                link_map.append(new_link_map)
                print("Link map lenght", len(link_map))
            else:
                link_map.extend(new_link_map)

            print("-"*50)            

        pool.close()
        pool.join()

    if to_json:
        list_of_lists_to_json(link_map, "outputjson")

if __name__ == '__main__':
    execute_search()
