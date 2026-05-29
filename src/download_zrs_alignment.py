"""Download a five-species ZRS alignment from Ensembl REST.

This reproduces the ZRS alignment step in the original notebook.
"""
from __future__ import annotations

import csv
from itertools import combinations
from pathlib import Path
import requests

ENSEMBL = "https://rest.ensembl.org"
REF_SPECIES = "homo_sapiens"
REF_REGION = "7:156791102-156791874"
TARGET_SPECIES = [
    "homo_sapiens",
    "mus_musculus",
    "gallus_gallus",
    "anolis_carolinensis",
    "pseudonaja_textilis",
]


def get_json(url: str, params: dict | None = None):
    response = requests.get(
        url,
        params=params,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def wrap_fasta(seq: str, width: int = 60) -> str:
    return "\n".join(seq[i:i + width] for i in range(0, len(seq), width))


def pairwise_stats(seq1: str, seq2: str) -> dict:
    matches = mismatches = gaps = comparable = 0
    for a, b in zip(seq1, seq2):
        if a == "-" or b == "-":
            gaps += 1
            continue
        comparable += 1
        if a == b:
            matches += 1
        else:
            mismatches += 1
    return {
        "alignment_length": len(seq1),
        "matches": matches,
        "mismatches": mismatches,
        "gaps": gaps,
        "comparable_sites": comparable,
        "identity_alignment_%": round(matches / len(seq1) * 100, 2),
        "identity_ungapped_%": round(matches / comparable * 100, 2) if comparable else 0,
    }


def main() -> None:
    outdir = Path("data/zrs")
    resultdir = Path("results")
    outdir.mkdir(parents=True, exist_ok=True)
    resultdir.mkdir(parents=True, exist_ok=True)

    endpoint = f"{ENSEMBL}/alignment/region/{REF_SPECIES}/{REF_REGION}"
    params = {"species_set_group": "amniotes", "method": "PECAN", "aligned": 1}
    blocks = get_json(endpoint, params=params)
    sequences = {}

    for block in blocks:
        for item in block.get("alignments", []):
            species = item.get("species")
            if species in TARGET_SPECIES:
                sequences[species] = item.get("seq", "").upper()

    missing = [sp for sp in TARGET_SPECIES if sp not in sequences]
    if missing:
        raise ValueError(f"Missing species from Ensembl response: {missing}")

    with open(outdir / "zrs_5species_aligned.fasta", "w") as f:
        for sp in TARGET_SPECIES:
            f.write(f">{sp}\n{wrap_fasta(sequences[sp])}\n")

    with open(outdir / "zrs_5species_ungapped.fasta", "w") as f:
        for sp in TARGET_SPECIES:
            ungapped = sequences[sp].replace("-", "")
            f.write(f">{sp}\n{wrap_fasta(ungapped)}\n")

    with open(resultdir / "zrs_sequence_lengths.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["species", "aligned_length", "ungapped_length"])
        writer.writeheader()
        for sp in TARGET_SPECIES:
            writer.writerow({
                "species": sp,
                "aligned_length": len(sequences[sp]),
                "ungapped_length": len(sequences[sp].replace("-", "")),
            })

    with open(resultdir / "zrs_pairwise_stats.csv", "w", newline="") as f:
        fields = ["species1", "species2", "alignment_length", "matches", "mismatches", "gaps", "comparable_sites", "identity_alignment_%", "identity_ungapped_%"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for sp1, sp2 in combinations(TARGET_SPECIES, 2):
            row = {"species1": sp1, "species2": sp2}
            row.update(pairwise_stats(sequences[sp1], sequences[sp2]))
            writer.writerow(row)

    print("Saved ZRS alignment and pairwise statistics.")


if __name__ == "__main__":
    main()
