from pathlib import Path

DATA_PATH = Path("data")
LINKS_PATH = DATA_PATH / "pdf_links.csv"
PDFS_PATH = DATA_PATH / "pdfs"
CSVS_PATH = DATA_PATH / "csvs"

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

COLUMNS = [
    "subject", "degree", "n_total", "n_women", "n_foreign", "sem_0", "sem_1",
    "sem_2", "sem_3", "sem_4", "sem_5", "sem_6", "sem_7", "sem_8", "sem_9",
    "sem_10", "sem_11", "sem_12", "sem_l12",
]

AREA = (108, 14.7, 554, 827)
