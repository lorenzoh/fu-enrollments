"""
Scrapes the links to all PDF files from the FU website
"""
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

from config import KIND_MAPPING

URL = "https://www.fu-berlin.de"
LIST_PATH = "/studium/studienorganisation/immatrikulation/weitere-angebote/statistik/index.html"
OUT_PATH = Path("data/links.csv")


def main():
    list_soup = get_soup(URL + LIST_PATH)
    semester_paths = [el.attrs["href"] for el in list_soup.select("h3 a")]

    pdfs = []

    for semester_url in tqdm([URL + path for path in semester_paths]):
        pdfs.extend(scrape_pdfs_semester(semester_url))

    df = pd.DataFrame(pdfs)

    df.to_csv(OUT_PATH, index=None)


def get_soup(url):
    r = requests.get(url)
    assert r.status_code == 200
    return BeautifulSoup(r.text, features="html.parser")


def scrape_pdfs_semester(semester_url):

    soup = get_soup(semester_url)
    semester = " ".join(soup.select_one("h1:nth-child(1)").text.split()
                        [-2:])  # Parse semester from title
    pdf_links = soup.select(".editor-content.hyphens a")

    pdfs = []
    for link in pdf_links:
        pdf = {"semester": semester}
        pdf["url"] = URL + link.attrs["href"]
        pdf["kind"] = KIND_MAPPING[link.text]
        pdf["filename"] = link.attrs["href"].split(sep="/")[-1]
        pdfs.append(pdf)

    return pdfs


if __name__ == "__main__":
    main()
