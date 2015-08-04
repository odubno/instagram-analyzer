"""
This is the word bank.  Thank you for your patronage.

Section 1.

Current events are scraped from various news organizations and media outlets for buzzwords.
These buzzwords populate a wordbank titled "buzztags" and are given top priority in sentiment evaluation.


Section 2.

A collection of words is extracted from a sample stream to over-ride inaccuracies in standard, pre-defined word banks


Section 3.

Standardized word banks are imported from previous NLP-based programs.


These features utilize:
    - requests
    - urllib3
    - beautifulsoup
    - regex
"""

# Section 1. Headline, article retrieval and extraction
# Strip <head> and <footer>
# Exclude images
# Exlude links


import requests
from bs4 import BeautifulSoup as bs

wsj_url = 'http://www.wsj.com/'


def media_tokenize(url):
    r = requests.get(url)
    html = r.text
    soup = bs(html).get_text()
    
    


