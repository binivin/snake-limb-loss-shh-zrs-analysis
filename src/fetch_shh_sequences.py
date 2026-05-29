"""Fetch selected SHH protein sequences from NCBI.

Usage:
    python src/fetch_shh_sequences.py --email your_email@example.com
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from Bio import Entrez, SeqIO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True, help="Email required by NCBI Entrez")
    parser.add_argument("--accessions", default="data/shh/accessions.csv")
    parser.add_argument("--out", default="data/shh/shh_selected.fasta")
    args = parser.parse_args()

    Entrez.email = args.email
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(args.accessions, newline="") as f:
        rows = list(csv.DictReader(f))

    with open(out_path, "w") as out_handle:
        for row in rows:
            accession = row["accession"]
            handle = Entrez.efetch(db="protein", id=accession, rettype="fasta", retmode="text")
            record = SeqIO.read(handle, "fasta")
            handle.close()
            SeqIO.write(record, out_handle, "fasta")
            print(record.id, record.description)


if __name__ == "__main__":
    main()
