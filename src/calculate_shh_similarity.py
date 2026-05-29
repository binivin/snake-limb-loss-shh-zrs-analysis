"""Calculate pairwise SHH protein similarity using a global identity-style score.

The score follows the original notebook logic: global alignment score / max sequence length * 100.
"""
from __future__ import annotations

import csv
import re
from itertools import combinations
from pathlib import Path
from Bio import SeqIO
from Bio.Align import PairwiseAligner


def species_name(description: str) -> str:
    match = re.search(r"\[(.*?)\]", description)
    return match.group(1) if match else "Unknown"


def main() -> None:
    records = list(SeqIO.parse("data/shh/shh_selected.fasta", "fasta"))
    aligner = PairwiseAligner()
    aligner.mode = "global"
    aligner.match_score = 1
    aligner.mismatch_score = 0
    aligner.open_gap_score = 0
    aligner.extend_gap_score = 0

    out = Path("results/shh_pairwise_similarity.csv")
    out.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for r1, r2 in combinations(records, 2):
        seq1, seq2 = str(r1.seq), str(r2.seq)
        score = aligner.score(seq1, seq2)
        similarity = score / max(len(seq1), len(seq2)) * 100
        rows.append({
            "species1": species_name(r1.description),
            "species2": species_name(r2.description),
            "similarity_%": round(similarity, 2),
        })

    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["species1", "species2", "similarity_%"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
