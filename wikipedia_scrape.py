# https://www.guru99.com/reading-and-writing-files-in-python.html
# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
# https://towardsdatascience.com/how-to-web-scrape-with-python-in-4-minutes-bc49186a8460
# https://docs.python.org/3/howto/regex.html
# https://stackoverflow.com/questions/2136267/beautiful-soup-and-extracting-a-div-and-its-contents-by-id#2136323

# Writen by Jacob Hillock / jmanh128 on github. Using above for help to write


import requests
import urllib.request
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup
from io import StringIO
from html.parser import HTMLParser
from cross_platform_support import dir_separater

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def scrape(url):
    s = dir_separater()
    time.sleep(.05)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = strip_tags(str(soup.find("h1", {"id": "firstHeading"})))
    file_name = title.replace(" ", "_").replace("/", "_") + ".txt"
    
    if not Path(f"scrapes{s}{file_name}").is_file():
        paras = soup.findAll('p')[1:]
        for i in range(len(paras)):
            paras[i] = strip_tags(str(paras[i]))

        with open(f"scrapes{s}" + file_name, "w+") as file:
            data = f""
            for p in paras:
                data += p
            regex = re.compile("\[\d*\]")
            data = regex.sub("", data)
            file.write(data)
            print('File writen')

if __name__ == "__main__":
    url = ""
    scrape(url)