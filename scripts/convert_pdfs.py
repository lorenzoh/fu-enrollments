"""
Converts the "studis_fach" pdfs to csvs using Tabula and bounding box annotations for
the tables.

"""
import argparse
import fileinput
import shutil
from pathlib import Path
from typing import Dict, List

import tabula
from tabula.template import load_template
from tqdm import tqdm


def convert_page_df(pdf_file: str, csv_file: str, options: Dict) -> None:
    tabula.convert_into(pdf_file, csv_file, guess=False,
                        output_format="csv", **options)


def convert_pdf_with_annotation(pdf_file: Path, annotation_file: Path, csv_file: Path):
    assert csv_file.suffix == ".csv"
    options = load_template(str(annotation_file))

    tmp_dir = Path(".tmp")
    tmp_dir.mkdir(exist_ok=True)
    tmp_csv_files: List[Path] = [
        tmp_dir / f"{csv_file.stem}-{i}.csv" for i in range(len(options))]

    for page_options, tmp_csv_file in zip(options, tmp_csv_files):
        convert_page_df(str(pdf_file), str(tmp_csv_file), page_options)

    with csv_file.open(mode="w") as f:
        for line in fileinput.input(tmp_csv_files):
            f.write(line)

    shutil.rmtree(".tmp")


def main(args: argparse.Namespace):
    assert args.pdfs.is_dir()
    assert args.annotations.is_dir()

    args.outdir.mkdir(parents=True, exist_ok=True)
    pdf_files = list(args.pdfs.glob("*.pdf"))
    annotation_files = list(args.annotations.glob("*.json"))

    print(f"Found {len(pdf_files)} pdfs, and {len(annotation_files)} annotations")

    for pdf_file in tqdm(pdf_files, desc="Processing pdfs"):
        annotation_file = args.annotations / f"{pdf_file.stem}.json"
        if annotation_file not in annotation_files:
            print(f"Could not find annotation for '{str(pdf_file)}'")
        else:
            csv_file = args.outdir / f"{pdf_file.stem}.csv"
            convert_pdf_with_annotation(pdf_file, annotation_file, csv_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--pdfs",
                        type=Path,
                        help="folder with pdfs",
                        default=Path("data/pdfs/studis_fach"))
    parser.add_argument("--annotations",
                        type=Path,
                        help="folder with .json annotations",
                        default=Path("annotations/"))
    parser.add_argument("--outdir", "-o",
                        type=Path, help="Directory where csvs will be saved",
                        default=Path("data/csvs/raw"))

    args = parser.parse_args()
    import os
    print(os.listdir(args.pdfs))
    main(args)
