"""Scan human ZRS ETS-core candidates and classify their state in aligned species."""
from __future__ import annotations

import csv
import re
from pathlib import Path
from Bio import SeqIO

SPECIES_ORDER = [
    "homo_sapiens",
    "mus_musculus",
    "gallus_gallus",
    "anolis_carolinensis",
    "pseudonaja_textilis",
]
ETS_PATTERNS = {"ETS_core_GGAA": r"GGAA", "ETS_core_GGAT": r"GGAT"}
FLANK = 8


def build_ungapped_to_aligned_map(aligned: str) -> dict[int, int]:
    mapping = {}
    ungapped_pos = 0
    for i, base in enumerate(aligned):
        if base != "-":
            ungapped_pos += 1
            mapping[ungapped_pos] = i
    return mapping


def classify(reference_site: str, query_site: str) -> str:
    if query_site == reference_site:
        return "conserved"
    if "-" in query_site:
        return "gap_disrupted"
    return "mutated"


def main() -> None:
    aligned_fasta = Path("data/zrs/zrs_5species_aligned.fasta")
    outdir = Path("results")
    outdir.mkdir(exist_ok=True)

    records = {rec.id: str(rec.seq).upper() for rec in SeqIO.parse(aligned_fasta, "fasta")}
    human = records["homo_sapiens"]
    human_ungapped = human.replace("-", "")
    pos_map = build_ungapped_to_aligned_map(human)

    rows = []
    site_no = 0
    for pattern_name, pattern in ETS_PATTERNS.items():
        for match in re.finditer(pattern, human_ungapped):
            site_no += 1
            start_u = match.start() + 1
            end_u = match.end()
            start_a = pos_map[start_u]
            end_a = pos_map[end_u]
            ref_site = human[start_a:end_a + 1]
            row = {
                "site_id": f"ETS_{site_no}",
                "pattern": pattern_name,
                "human_motif": ref_site,
                "human_start_ungapped": start_u,
                "human_end_ungapped": end_u,
                "aligned_start_1based": start_a + 1,
                "aligned_end_1based": end_a + 1,
                "human_context": human[max(0, start_a - FLANK):min(len(human), end_a + FLANK + 1)],
            }
            for sp in SPECIES_ORDER:
                site = records[sp][start_a:end_a + 1]
                row[f"{sp}_site"] = site
                row[f"{sp}_status"] = "reference" if sp == "homo_sapiens" else classify(ref_site, site)
                row[f"{sp}_context"] = records[sp][max(0, start_a - FLANK):min(len(records[sp]), end_a + FLANK + 1)]
            rows.append(row)

    fieldnames = list(rows[0].keys())
    with open(outdir / "zrs_ETS_motif_scan.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with open(outdir / "zrs_ETS_motif_summary.csv", "w", newline="") as f:
        fields = ["species", "conserved", "mutated", "gap_disrupted", "total_sites"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for sp in SPECIES_ORDER[1:]:
            statuses = [row[f"{sp}_status"] for row in rows]
            writer.writerow({
                "species": sp,
                "conserved": statuses.count("conserved"),
                "mutated": statuses.count("mutated"),
                "gap_disrupted": statuses.count("gap_disrupted"),
                "total_sites": len(statuses),
            })

    print("Saved ETS motif scan and summary.")


if __name__ == "__main__":
    main()
