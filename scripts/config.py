from pathlib import Path

DATA_PATH = Path("data")
LINKS_PATH = DATA_PATH / "links.csv"
PDFS_PATH = DATA_PATH / "pdfs"

KIND_MAPPING = {
    "Gesamtstatistik": "gesamt",
    "Studierende nach Staatsangehörigkeit": "studis-staat",
    "Studierende nach Studienfach und Abschluss": "studis-fach-abschluss",
    "Studierende nach Abschluss und Studienfach": "studis-abschluss-fach",
    "Abiturort": "abiort",
    "Erläuterungsbogen": "erlaeuterung",
    "Bestandene Abschlussprüfungen": "prüfungen",
    "Promotionen": "promotionen"
}
