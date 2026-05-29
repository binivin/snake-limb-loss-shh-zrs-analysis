"""Create simple figures for the GitHub README."""
from __future__ import annotations

import csv
from pathlib import Path
import matplotlib.pyplot as plt


def read_csv(path: str) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    Path("figures").mkdir(exist_ok=True)

    # ETS motif status
    rows = read_csv("results/zrs_ETS_motif_summary.csv")
    labels = [r["species"] for r in rows]
    conserved = [int(r["conserved"]) for r in rows]
    mutated = [int(r["mutated"]) for r in rows]
    gap = [int(r["gap_disrupted"]) for r in rows]
    x = range(len(labels))
    plt.figure(figsize=(8, 5))
    plt.bar(x, conserved, label="conserved")
    plt.bar(x, mutated, bottom=conserved, label="mutated")
    plt.bar(x, gap, bottom=[c + m for c, m in zip(conserved, mutated)], label="gap_disrupted")
    plt.xticks(list(x), labels, rotation=30, ha="right")
    plt.ylabel("Number of ETS candidate motifs")
    plt.title("ETS motif status relative to human ZRS candidates")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/zrs_ets_motif_status.png", dpi=200)
    plt.close()

    print("Saved figures.")


if __name__ == "__main__":
    main()
