# This is a file which contains all the utility functions for webscraping of data from the web
# Author: Theodor Jonsson   
# Date: 2023-01-02
# Path: DataScraping/utils.py
# 
#   These utility fynctions are used to scrape data from the web.
#   The functions are basic functions to be used in the webscraping.
#   Examples of these functions are:
#   - get_soup - Get the soup of a url
#   - get_html - Get the html of a url
#   - get_json - Get the json of a url
#   - get_text - Get the text of a url
#   - get_url - Get the url of a url
#   - find_element - Find an element in a soup
#   - visualize_soup - Visualize a soup, to see the structure of the html nicely
#   - get_all_links - Get all the links in a soup
#   - store_soup - Store a soup in a file
#   - store_html - Store the html of a soup in a file
#   - store_json - Store the json of a soup in a file
#   - store_text - Store the text of a soup in a file
#   - store_url - Store the url of a soup in a file
#

import requests
from bs4 import BeautifulSoup
import json
import re
import os
import sys

def get_soup(url:str,parser:str='html.parser',verbose:bool=False)->BeautifulSoup:
    """
    Get the soup of a url
    """
    if verbose:
        print(f"Getting soup from {url}")
    return BeautifulSoup(requests.get(url).text,parser)

def get_html(url:str,verbose:bool=False)->str:
    """
    Get the html of a url
    """
    if verbose:
        print(f"Getting html from {url}")
    return requests.get(url).text

def get_json(url:str,verbose:bool=False)->dict:
    """
    Get the json of a url
    """
    if verbose:
        print(f"Getting json from {url}")
    return json.loads(requests.get(url).text)

def get_text(url:str,verbose:bool=False)->str:
    """
    Get the text of a url
    """
    if verbose:
        print(f"Getting text from {url}")
    return requests.get(url).text

def get_url(url:str,verbose:bool=False)->str:
    """
    Get the url of a url
    """
    if verbose:
        print(f"Getting url from {url}")
    return requests.get(url).url

def find_element(soup:BeautifulSoup,element:str,verbose:bool=False)->BeautifulSoup:
    """
    Find an element in a soup
    """
    if verbose:
        print(f"Finding element {element} in soup")
    return soup.find(element)

def visualize_soup(soup:BeautifulSoup,verbose:bool=False)->None:
    """
    Visualize a soup, to see the structure of the html nicely
    """
    if verbose:
        print(f"Visualizing soup")
    print(soup.prettify())

def get_all_links(soup:BeautifulSoup,verbose:bool=False)->list[str]:
    """
    Get all the links in a soup
    """
    if verbose:
        print(f"Getting all links in soup")
    return [link.get('href') for link in soup.find_all('a')]

def store_soup(soup:BeautifulSoup,path:str,verbose:bool=False)->None:
    """
    Store a soup in a file
    """
    if verbose:
        print(f"Storing soup in {path}")
    with open(path,'w') as f:
        f.write(soup.prettify())


def store_html(soup:BeautifulSoup,path:str,verbose:bool=False)->None:
    """
    Store the html of a soup in a file
    """
    if verbose:
        print(f"Storing html in {path}")
    with open(path,'w') as f:
        f.write(soup.text)

def store_json(soup:BeautifulSoup,path:str,verbose:bool=False)->None:
    """
    Store the json of a soup in a file
    """
    if verbose:
        print(f"Storing json in {path}")
    with open(path,'w') as f:
        f.write(json.dumps(soup))

def store_text(soup:BeautifulSoup,path:str,verbose:bool=False)->None:
    """
    Store the text of a soup in a file
    """
    if verbose:
        print(f"Storing text in {path}")
    with open(path,'w') as f:
        f.write(soup.text)

def store_url(soup:BeautifulSoup,path:str,verbose:bool=False)->None:
    """
    Store the url of a soup in a file
    """
    if verbose:
        print(f"Storing url in {path}")
    with open(path,'w') as f:
        f.write(soup.url)


