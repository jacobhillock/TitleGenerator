import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from wikipedia_scrape import scrape


def get_recursive_links(url, depth=0):
    urls = [url]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paras = soup.findAll('p')[1:]
    links = []

    for p in paras:
        paragraph_parse = BeautifulSoup(str(p), "html.parser")
        a_s = paragraph_parse.findAll('a', href=True)
        for link in a_s:
            if (h:=str(link['href']))[0] == '/':
                links.append(f'https://en.wikipedia.org{h}')
    links = list(set(links))

    if depth == 0:
        print(url)
        return links
    elif depth > 0:
        return_links = []
        for link in links:
            sub_links = get_recursive_links(link, depth-1)
            return_links = list(set(return_links + sub_links + [link]))
        return return_links


if __name__ == "__main__":
    urls = get_recursive_links("https://en.wikipedia.org/wiki/Python_(programming_language)", 1)
    print(len(urls))
    for i in range(len(urls)):
        print(f"{i+1}/{len(urls)}")
        try:
            scrape(urls[i])
        except:
            print(f"{urls[i]} could not print")