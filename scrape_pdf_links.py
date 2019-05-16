"""
Scrapes the links to all PDF files from the FU website and downloads the PDFs
"""
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.fu-berlin.de"
LIST_PATH = "/studium/studienorganisation/immatrikulation/weitere-angebote/statistik/index.html"


def main():
    list_soup = get_soup(URL + LIST_PATH)
    semester_paths = [el.attrs["href"] for el in list_soup.select("h3 a")]

    for semester_url in [URL + path for path in semester_paths]:
        scrape_pdfs_semester(semester_url)


def get_soup(url):
    r = requests.get(url)
    assert r.status_code == 200
    return BeautifulSoup(r.text)


def scrape_pdfs_semester(semester_url):
    
    soup = get_soup(semester_url)
    semester = " ".join(soup.select("h1").split()[-2:])  # Parse semester from title
    pdf_links = soup.select(".editor-content.hyphens a")
    for link in pdf_links:
        url = URL + link.attrs["href"]
        kind = link.text
        tags = link.attrs[""]


    print(pdf_links)


if __name__ == "__main__":
    main()
