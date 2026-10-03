"""Prepare the course CSV for import into the Supabase knowledge_items table."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "base de connaissance.csv"
TARGET = ROOT / "data" / "import_supabase.csv"

SOURCE_COLUMNS = {
    "nom": "Nom",
    "note_alex": "Note Alex",
    "texte": "Texte",
    "url": "URL",
    "date_maj_n8n": "date de mise à jour n8n",
    "etiquettes": "Étiquettes",
}


def main() -> None:
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        missing = set(SOURCE_COLUMNS.values()) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Colonnes absentes du CSV : {sorted(missing)}")

        with TARGET.open("w", encoding="utf-8", newline="") as target:
            writer = csv.DictWriter(
                target, fieldnames=["source_row", *SOURCE_COLUMNS], lineterminator="\n"
            )
            writer.writeheader()
            count = 0
            for count, row in enumerate(reader, start=1):
                writer.writerow(
                    {
                        "source_row": count,
                        **{
                            destination: row[source_name]
                            for destination, source_name in SOURCE_COLUMNS.items()
                        },
                    }
                )

    print(f"{count} lignes préparées : {TARGET}")


if __name__ == "__main__":
    main()

