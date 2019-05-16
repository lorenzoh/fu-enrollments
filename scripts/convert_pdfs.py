"""
Script for converting the tables of `.pdf`s of type 'Studierende nach Studienfach und Abschluss'
to `.csv`.
Only converts starting in 2010 since previous years used a different format.
"""
from pathlib import Path

import tabula
from tqdm import tqdm
import pandas as pd

from config import AREA, HEADER, LINKS_PATH, PDFS_PATH, CSVS_PATH


def df_from_pdf(path: Path) -> pd.DataFrame:
    df = tabula.read_pdf(
        str(path),
        pages="all",
        area=AREA,
        lattice=True,
        pandas_options={
            "names": HEADER, "index_col": False
        },
        #options="-u"
    )

    return df


def main():
    list_df = pd.read_csv(LINKS_PATH)
    to_convert = list_df[(list_df.year >= 2010) & (
        list_df.kind == "studis-fach-abschluss")]

    if not CSVS_PATH.is_dir():
        CSVS_PATH.mkdir()

    for (i, row) in tqdm(to_convert.iterrows(), total=len(to_convert)):
        in_path = PDFS_PATH / row.kind / f"{row['name']}.pdf"
        df = df_from_pdf(in_path)

        out_folder = CSVS_PATH / row.kind
        if not out_folder.is_dir():
            out_folder.mkdir()

        out_path = out_folder / f"{row['name']}.csv"
        df.to_csv(out_path, index=False)


if __name__ == "__main__":
    main()


# df = convert_studi_pdf(Path(
    # "data/pdfs/studis-fach-abschluss/WiSe1819_Stg_Abschl_Sem_Stand_Dez_2018.pdf"))
