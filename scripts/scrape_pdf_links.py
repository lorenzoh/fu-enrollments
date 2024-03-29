"""
Scrapes the links to all PDF files from the FU statistics website

.csv Fields:
-------
filename: str
    Name of the file on FU server
name: str
    Generated name with form "{kind}-{year}-{season}.csv"
kind: str
    What kind of statistic this file corresponds to
season: str
    One of {"summer", "winter"}
semestername: str
    The full name of a semester, e.g. "Wintersemester 2016/2017"
year: int

Checks:
- no NAN values
"""
import argparse
from pathlib import Path
from typing import Dict, List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

DOMAIN = "https://www.fu-berlin.de"
STATISTIC_PATH = ("/studium/studienorganisation/immatrikulation/"
                  "weitere-angebote/statistik/index.html")

KIND_MAPPING = {
    "Gesamtstatistik": "gesamt",
    "Studierende nach Staatsangehörigkeit": "studis_staat",
    "Studierende nach Studienfach und Abschluss": "studis_fach",
    "Studierende nach Abschluss und Studienfach": "studis_abschluss",
    "Abiturort": "abiort",
    "Erläuterungsbogen": "erlaeuterung",
    "Bestandene Abschlussprüfungen": "pruefungen",
    "Promotionen": "promotionen"
}


def main(args: argparse.Namespace):
    list_soup = get_soup(DOMAIN + STATISTIC_PATH)
    semester_paths = [el.attrs["href"] for el in list_soup.select("h3 a")]

    pdfs: List[Dict[str, str]] = []

    for semester_url in tqdm([DOMAIN + path for path in semester_paths]):
        soup = get_soup(semester_url)
        pdfs.extend(scrape_pdfs_semester(soup))

    df = pd.DataFrame(pdfs)

    check_integrity(df)

    df.to_csv(args.outfile, index=None)


def get_soup(url):
    r = requests.get(url)
    assert r.status_code == 200
    return BeautifulSoup(r.text, features="html.parser")


def scrape_pdfs_semester(soup: BeautifulSoup) -> List[Dict[str, str]]:
    semester = " ".join(soup.select_one("h1:nth-child(1)").text.split()
                        [-2:])  # Parse semester from title
    season = semester[:6].lower()
    year = semester.split()[-1][:4]
    pdf_links = soup.select(".editor-content.hyphens a")

    pdfs = []
    for link in pdf_links:
        pdf = {
            "semester_name": semester,
            "season": season,
            "year": year,
        }
        pdf["url"] = DOMAIN + link.attrs["href"]
        pdf["kind"] = KIND_MAPPING[link.text]
        pdf["name"] = f"{pdf['kind']}-{pdf['year']}-{pdf['season']}"
        pdf["filename"] = link.attrs["href"].split(sep="/")[-1]
        pdfs.append(pdf)

    return pdfs


def check_integrity(df: pd.DataFrame) -> None:
    assert df.isna().sum().sum() == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outfile", "-o",
                        type=Path, help="Path to .csv file where result will be stored",
                        default=Path("data/pdf_links.csv"))

    args = parser.parse_args()

    main(args)
