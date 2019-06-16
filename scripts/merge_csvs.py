"""
Merge the cleaned csvs into:

- studis_fach.csv
    All csvs merged. Has NA values for newer columns like n_female and n_foreign
- studis_fach_older.csv
    csvs until incl. summer 2019
- studis_fach_newer.csv
    csvs from incl. winter 2019


Also add some additional columns

Columns added:
- pctg_female: float
- year: int
- season: str (one of "summer", "winter")

"""
import argparse
from pathlib import Path

import pandas as pd


def main(args: argparse.Namespace):
    csv_files = sorted(list(args.csvs.glob("*.csv")))
    semester_dfs = [pd.read_csv(csv_file) for csv_file in csv_files]

    # add extra info to semester DataFrames
    for csv_file, semester_df in zip(csv_files, semester_dfs):
        name = csv_file.stem[12:]
        year, season = name.split(sep="-")
        semester_df["year"] = year
        semester_df["season"] = season

    df = pd.concat(semester_dfs, sort=False, ignore_index=True)
    df_older = pd.concat(semester_dfs[:5], sort=False, ignore_index=True)
    df_newer = pd.concat(semester_dfs[5:], sort=False, ignore_index=True)

    dfs = (df, df_older, df_newer)

    # add extra columns to merged DataFrames
    for df in dfs:
        if "n_women" in df.columns:
            df["pctg_women"] = df.n_women / df.n_total

    # save to disk
    args.outdir.mkdir(exist_ok=True, parents=True)
    df.to_csv(args.outdir / "studis_fach.csv", index=False)
    df_older.to_csv(args.outdir / "studis_fach_older.csv", index=False)
    df_newer.to_csv(args.outdir / "studis_fach_newer.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--csvs",
                        type=Path, help="folder with cleaned csvs",
                        default=Path("data/csvs/cleaned"))
    parser.add_argument("--outdir", "-o",
                        type=Path, help="Directory where csvs will be saved",
                        default=Path("data/csvs/final"))

    args = parser.parse_args()
    main(args)
