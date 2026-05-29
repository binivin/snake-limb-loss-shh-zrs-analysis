"""Summarize SHH protein FASTA sequence lengths."""
from __future__ import annotations

import csv
import re
from pathlib import Path
from Bio import SeqIO


def species_name(description: str) -> str:
    match = re.search(r"\[(.*?)\]", description)
    return match.group(1) if match else "Unknown"


def main() -> None:
    fasta = Path("data/shh/shh_selected.fasta")
    out = Path("results/shh_sequence_lengths.csv")
    out.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for record in SeqIO.parse(fasta, "fasta"):
        rows.append({
            "accession": record.id,
            "species": species_name(record.description),
            "length_aa": len(record.seq),
        })

    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["accession", "species", "length_aa"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
