"""
Downloads all pdf files
"""
import argparse
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm


def main(args: argparse.Namespace):
    assert args.linksfile.is_file(), "Did you download the links? (scrape_pdf_links.py)"
    df = pd.read_csv(args.linksfile)
    if not args.outdir.is_dir():
        args.outdir.mkdir()

    for (_, row) in tqdm(df.iterrows(), total=len(df), desc="Collecting .pdfs"):
        folder = args.outdir / row.kind
        if not folder.is_dir():
            folder.mkdir()
        path = folder / f"{row['name']}.pdf"
        if not path.is_file():
            download_file(row.url, path)


def download_file(url: str, path: Path) -> None:
    """Downloads and saves file at `url` to `path`"""
    r = requests.get(url, stream=True)
    with path.open("wb") as f:
        for chunk in r.iter_content(2048):
            if chunk:
                f.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--linksfile", "-i",
                        type=Path,
                        help=".csv file from `scrape_pdf_links.csv`",
                        default=Path("data/pdf_links.csv"))
    parser.add_argument("--outdir", "-o",
                        type=Path, help="Directory where pdfs will be saved",
                        default=Path("data/pdfs"))
    args = parser.parse_args()
    main(args)
