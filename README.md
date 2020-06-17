# TitleGenerator
This Python program was written by:
- Jacob Hillock ([jmanh128](https://github.com/jmanh128))
- Tangeni Shikomba ([dev-mtshikomba](https://github.com/dev-mtshikomba))
- Chisulo Mukabe ([NuMellow](https://github.com/NuMellow))

For the COSC462 `Introduction to Information Retrieval and Recommendor Systems` class at Eastern Michigan University.

Our methodes include:
- Algorithms

Our sources include:
- Sources

# Python version

- Python 3.8 recommended
- Currently testing Python 3.7 

# How to use python venv
## **Make venv**
`python -m venv [venv]`

> NOTE: [venv] can be whatever, I usually just leave it as "venv"

> NOTE: if you don't name it as "venv" please add what ever you name it to the .gitignore and commit that

> NOTE: this *probably* does not work with anaconda/conda, please use normal python.

## **Activate venv**
MAC/LINUX: `source venv/bin/activate`

WINDOWS: `venv\Scripts\Activate`

## **Load requirements**
`pip install -r requirements.txt`

> NOTE: Make sure to activate the venv

## **Update requirements**
`pip freeze > requirements.txt`

> NOTE: Make sure the venv is activated

> NOTE: Make sure to commit and push update


# Updating this readme:
If you need to update the README.md, follow the style guide here: 
> https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax

# Using the Wikipedia webscrape:
1. Add the directory `scrapes` to the folder the wikipedia scrapes are in
2. Scrape:
   - if you wish to do a single scrape:
     - go into `wikipedia_scrape.py`, go down to the `if __name__ == "__main__":`
     - edit `url = ""` to be a wikiepedia article url
   - if you wish to do a recursive scrape:
     - go into `wikipedia_scrape_rec.py`, go down to the `if __name__ == "__main__":`
     - edit `url = ""` to be a wikiepedia article url

# Passing arguments from the terminal
- using the following command shows you all the arguments available for this tool:
```python
python main.py -h
```
- The parameter below allows you scrape the web using keywords, the tools will scrape for a documents from wikipedia using the keyword "Artificial Intelligence", and saves the scraped content to a named text file.
```python
python main.py --doc='Artificial Interlligence'
```