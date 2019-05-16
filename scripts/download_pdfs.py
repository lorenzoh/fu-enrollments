import pandas as pd
from pathlib import Path
import requests
from tqdm import tqdm


from config import KIND_MAPPING, LINKS_PATH, PDFS_PATH


def main():
    assert LINKS_PATH.is_file(), "Did you download the links? (scrape_pdf_links.py)"
    df = pd.read_csv(LINKS_PATH)
    if not PDFS_PATH.is_dir():
        PDFS_PATH.mkdir()

    for (i, row) in tqdm(df.iterrows(), total=len(df)):
        folder = PDFS_PATH / row.kind
        if not folder.is_dir():
            folder.mkdir()
        path = folder / f"{row['name']}.pdf"
        if not path.is_file():
            download(row.url, path)


def download(url: str, path: Path):
    r = requests.get(url, stream=True)
    with path.open("wb") as f:
        for chunk in r.iter_content(2048):
            if chunk:
                f.write(chunk)


if __name__ == "__main__":
    main()
