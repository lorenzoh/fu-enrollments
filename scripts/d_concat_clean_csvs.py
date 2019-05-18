"""
Load multiple converted `.csv`s, clean them and concatenate them.

Exporting the .csvs by hand in Tabula, there are still some mistakes:
- some empty columns are being read in some of the tables
- the semester enrollment columns are read as strings because of the
  "-" indicating a 0.
"""
import csv
from typing import List
from pathlib import Path
import pandas as pd

from config import COLUMNS

CSVS_FOLDER = Path("data/csvs/studis-fach-abschluss")
OUT_FILE = Path("data/csvs/studis-fach-abschluss.csv")


def main(csvs_folder: Path = CSVS_FOLDER, out_file: Path = OUT_FILE):
    # Load into DataFrames
    csv_files: List[Path] = list(csvs_folder.glob("*.csv"))
    dfs: List[pd.DataFrame] = [pd.read_csv(
        csv_file, names=[str(x) for x in range(50)]) for csv_file in csv_files]

    # Clean
    for (df, file) in zip(dfs, csv_files):
        # delete NA columns
        for col in df.columns:
            if df[col].isna().sum() == len(df):
                del df[col]
        assert df.shape[1] == 19  # 19 columns should be detected
        assert df.isna().sum().sum() == 0  # there must not be NA values left
        df.columns = COLUMNS  # set proper column names

        # Convert columns to proper data type
        for col in df.columns:
            # parse `sem_*` columns
            if col.startswith("sem"):
                df[col] = df[col].apply(parse_int)
            # convert `n_*` columns to int
            if df[col].dtype == "float":
                df[col] = df[col].astype("int64")


        # Remove line breaks ("\n") from `subject` column
        df["subject"] = df["subject"].str.replace("\n", " ")

        # Add extra columns for year and season
        name = str(file).split(sep="/")[-1].split(sep=".")[-2]
        year, season, *_ = name.split("-")
        df["year"], df["season"] = year, season
        df["semester"] = season + year

    all_df: pd.DataFrame = pd.concat(dfs)

    all_df.to_csv(out_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
    return df


def parse_int(s: str) -> int:
    """
    Parses a string from a semester column
    """
    if s == "-":
        return 0
    return int(s)


if __name__ == "__main__":
    df = main()
