# stagehand_reader.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_fineprint_text(url: str) -> str:
    """
    1. GET the provided URL
    2. Find an <a> whose text contains 'term', 'conditions', or 'use'
    3. Follow that link (resolve relative URL)
    4. Scrape all <p> paragraphs from the Terms page
    5. Return joined text
    """
    # Step 1: fetch initial page
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Step 2: find the Terms link
    link = None
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True).lower()
        if any(k in text for k in ("term of use", "terms of use", "terms", "conditions")):
            link = a["href"]
            break

    # If we found a Terms link, resolve and fetch it
    if link:
        terms_url = urljoin(url, link)
        resp = requests.get(terms_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

    # Step 3: scrape all paragraphs
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
    return "\n\n".join(paragraphs)
