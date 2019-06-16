"""

After conversion from pdf to csv, there are still some parsing errors to be resolved:

1. empty rows
2. entries with long subject names span over multiple rows
3. empty columns
4. empty first column

After removing these, the following changes are made
- replace "-" with 0 for student counts
- decimal thousands punctuation from "." to ","

"""
import csv
import argparse
from pathlib import Path

import pandas as pd
from tqdm import tqdm

OLD_HEADER = [
    "subject", "degree", "n_total", "sem_1",
    "sem_2", "sem_3", "sem_4", "sem_5", "sem_6", "sem_7", "sem_8", "sem_9",
    "sem_10", "sem_11", "sem_12", "sem_l12",
]
NEW_HEADER = [
    "subject", "degree", "n_total", "n_women", "n_foreign", "sem_0", "sem_1",
    "sem_2", "sem_3", "sem_4", "sem_5", "sem_6", "sem_7", "sem_8", "sem_9",
    "sem_10", "sem_11", "sem_12", "sem_l12",
]


def get_header(filename: str):
    """
    Return the correct header for a statistic
    Statistics until incl. summer 2009 have 3 fewer fields
    """
    assert filename.startswith("studis_fach-")
    year = int(filename[12:16])
    season = filename[17:23]
    if (year <= 2008) or (year == 2009 and season == "sommer"):
        return OLD_HEADER
    else:
        return NEW_HEADER


def main(args: argparse.Namespace) -> None:
    csv_files = sorted(list(args.csvs.glob("studis_fach*.csv")))
    args.outdir.mkdir(exist_ok=True, parents=True)
    print(f"Found {len(csv_files)} .csv files.")

    for csv_file in tqdm(csv_files, desc="Cleaning .csvs"):
        out_file = args.outdir / csv_file.name
        clean_csv_step1(csv_file, out_file)
        clean_csv_step2(out_file)


def clean_csv_step1(csv_file: Path, out_file: Path) -> None:
    with csv_file.open() as f, (args.outdir / csv_file.name).open(mode="w") as o:
        reader = csv.reader(f)
        writer = csv.writer(o)

        prepend = ""
        for row in reader:
            # check for empty first or last entry
            if row[0] == "":
                row = row[1:]
            if row[-1] == "":
                row = row[:-1]

            # check for empty row (no non-empty column)
            if not any(map(lambda x: x != "", row)):
                continue
            # check if only first column has entry => prepend to subject name of next row
            elif not any(map(lambda x: x != "", row[1:])):
                if prepend:
                    prepend += " "
                prepend += row[0]
            else:
                if prepend:
                    row[0] = prepend + row[0]
                    prepend = ""

                row[0] = " ".join(row[0].split())
                writer.writerow(row)


def clean_csv_step2(csv_file: Path):
    """

    """
    df = pd.read_csv(
        csv_file,
        header=None,
        decimal=",",
        thousands=".",
    )

    # clean empty columns
    for col in df.columns:
        if df[col].isna().sum() == len(df):
            del df[col]

    # set header
    df.columns = get_header(csv_file.name)

    if df.isna().sum().sum() > 0:
        print(csv_file.name)
        #print(df.isna().sum())
        print(df.subject[df.n_foreign.isna()])

    # parse numerical columns
    #for col in df.columns:
    #    # parse `sem_*` columns
    #    if col.startswith("sem"):
    #        df[col] = df[col].apply(lambda x: 0 if x == "-" else int(x))
    #    # convert `n_*` columns to int
    #    if df[col].dtype == "float":
    #        df[col] = df[col].astype("int64")

    df.to_csv(csv_file, index=None)


def check_df(df: pd.DataFrame):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--csvs",
                        type=Path, help="folder with raw csvs",
                        default=Path("data/csvs/raw"))
    parser.add_argument("--outdir", "-o",
                        type=Path, help="Directory where csvs will be saved",
                        default=Path("data/csvs/cleaned"))

    args = parser.parse_args()
    main(args)
