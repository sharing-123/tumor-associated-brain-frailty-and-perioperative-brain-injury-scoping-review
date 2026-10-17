import sys
sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from prisma_numbers import P

OUT = "figs"
NAVY = "#1f3b57"
GREY = "#f4f6f8"
PALE = "#e3f2f4"

def box(ax, x, y, w, h, text, fc="white", ec=NAVY, fs=6.5, bold=False, align="left", color="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.06", fc=fc, ec=ec, lw=1.0))
    tx = x + 0.1 if align == "left" else x + w / 2
    ax.text(tx, y + h / 2, text, ha=align, va="center", fontsize=fs, fontweight="bold" if bold else "normal", linespacing=1.35, color=color)

def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=9, lw=1.0, color=NAVY, shrinkA=0, shrinkB=0))

def fig_prisma():
    d = P
    fig, ax = plt.subplots(figsize=(7.6, 9.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 13.2)
    ax.axis("off")
    L, Mx, Rx = 0.85, 4.1, 6.9
    LW, MW, RW = 3.0, 2.55, 2.95
    fs = 6.5

    box(ax, L, 12.45, LW + 0.25 + MW, 0.55, "Identification of studies via databases and preprint server", fc="#6a4c93", ec="#6a4c93", fs=6.9, bold=True, align="center", color="white")
    box(ax, Rx, 12.45, RW, 0.55, "Other methods", fc="#6a4c93", ec="#6a4c93", fs=6.9, bold=True, align="center", color="white")

    for y, h, t in ((9.45, 2.85, "Identification"), (3.0, 6.1, "Screening"), (1.75, 1.0, "Included")):
        ax.add_patch(FancyBboxPatch((0.05, y), 0.55, h, boxstyle="round,pad=0,rounding_size=0.08", fc="#7fc8d6", ec=NAVY, lw=1.0))
        ax.text(0.325, y + h / 2, t, rotation=90, ha="center", va="center", fontsize=7.6, fontweight="bold", color=NAVY)

    box(ax, L, 9.45, LW, 2.85,
        "Records identified from\nDatabases (n = %s)\n   PubMed (n = %d)\n   Scopus (n = %s)\n   ProQuest (n = %d)\n   Cochrane Library (n = %d)\nPreprint server\n   medRxiv (n = %d)\nTotal (n = %s)"
        % (f"{d['db_only']:,}", d["pubmed"], f"{d['scopus']:,}", d["proquest"], d["cochrane"], d["medrxiv"], f"{d['db_total']:,}"), fs=fs)
    box(ax, Mx, 10.15, MW, 1.45,
        "Records removed before screening\n   Duplicate records (n = %d)\n   Automation tools (n = 0)\n   Other reasons (n = 0)" % d["dups"], fc=GREY, fs=fs)
    arrow(ax, L + LW, 10.87, Mx, 10.87)
    box(ax, Rx, 9.45, RW, 2.85,
        "Records identified from\nWebsites\n   Google Scholar (n = %d)\nCitation searching (n = %d)\nClient-supplied instrument\nliterature (n = %d)\nOrganisations (n = 0)\nTotal (n = %d)"
        % (d["gscholar"], d["citation"], d["client"], d["other_total"]), fs=fs)

    box(ax, L, 8.0, LW, 0.85, "Records screened\n(n = %s)" % f"{d['screened']:,}", fs=fs)
    arrow(ax, L + LW / 2, 9.45, L + LW / 2, 8.85)
    box(ax, Mx, 8.0, MW, 0.85, "Records excluded at title\nand abstract (n = %s)" % f"{d['ta_excl']:,}", fc=GREY, fs=fs)
    arrow(ax, L + LW, 8.42, Mx, 8.42)
    box(ax, Rx, 8.0, RW, 0.85, "Reports sought for retrieval\n(n = %d)" % d["sought_ot"], fs=fs)
    arrow(ax, Rx + RW / 2, 9.45, Rx + RW / 2, 8.85)

    box(ax, L, 6.6, LW, 0.85, "Reports sought for retrieval\n(n = %d)" % d["sought_db"], fs=fs)
    arrow(ax, L + LW / 2, 8.0, L + LW / 2, 7.45)
    box(ax, Mx, 6.6, MW, 0.85, "Reports not retrieved\n(n = %d)" % d["nr_db"], fc=GREY, fs=fs)
    arrow(ax, L + LW, 7.02, Mx, 7.02)
    box(ax, Rx, 6.6, RW, 0.85, "Reports not retrieved\n(n = %d)" % d["nr_ot"], fc=GREY, fs=fs)
    arrow(ax, Rx + RW / 2, 8.0, Rx + RW / 2, 7.45)

    box(ax, L, 5.2, LW, 0.85, "Reports assessed for\neligibility (n = %d)" % d["assessed_db"], fs=fs)
    arrow(ax, L + LW / 2, 6.6, L + LW / 2, 6.05)
    box(ax, Mx, 3.4, MW, 2.65,
        "Reports excluded (n = %d)\n   Wrong outcome (n = %d)\n   Wrong population (n = %d)\n   Wrong publication type\n      (n = %d)\n   Wrong study design (n = %d)\n   Wrong intervention (n = %d)"
        % (d["excl_db"], d["r_outcome_db"], d["r_pop_db"], d["r_pub_db"], d["r_design_db"], d["r_int_db"]), fc=GREY, fs=fs)
    arrow(ax, L + LW, 5.62, Mx, 5.62)
    box(ax, Rx, 5.2, RW, 0.85, "Reports assessed for\neligibility (n = %d)" % d["assessed_ot"], fs=fs)
    arrow(ax, Rx + RW / 2, 6.6, Rx + RW / 2, 6.05)
    ex_w = RW - 0.45
    box(ax, Rx, 3.0, ex_w, 1.95,
        "Reports excluded (n = %d)\n   Wrong outcome (n = %d)\n   Wrong population (n = %d)\n   Wrong study design (n = %d)\n   Wrong publication type\n      (n = %d, instrument manual)"
        % (d["excl_ot"], d["r_outcome_ot"], d["r_pop_ot"], d["r_design_ot"], d["r_pub_ot"]), fc=GREY, fs=fs)
    arrow(ax, Rx + ex_w / 2, 5.2, Rx + ex_w / 2, 4.95)

    box(ax, L, 1.75, LW, 1.0, "Studies included from\ndatabases and preprint\nserver (n = %d)" % d["inc_db"], fc=PALE, fs=fs)
    arrow(ax, L + LW / 2, 5.2, L + LW / 2, 2.75)
    box(ax, Rx, 1.75, RW, 1.0, "Studies included from\nother methods (n = %d)" % d["inc_ot"], fc=PALE, fs=fs)
    xr = Rx + RW + 0.12
    ax.plot([xr, xr], [5.62, 2.9], color=NAVY, lw=1.0)
    ax.plot([Rx + RW, xr], [5.62, 5.62], color=NAVY, lw=1.0)
    arrow(ax, xr, 2.9, xr, 2.75)

    ax.add_patch(FancyBboxPatch((L, 0.2), 9.0, 0.95, boxstyle="round,pad=0,rounding_size=0.06", fc="#d3ebef", ec=NAVY, lw=1.3))
    ax.text(L + 4.5, 0.675, "Studies included in review (n = %d)\nCore evidence base (n = %d) and instrument-focused stratum (n = %d)" % (d["inc_total"], d["core"], d["instr"]),
            ha="center", va="center", fontsize=7.2, fontweight="bold", linespacing=1.4)
    arrow(ax, L + LW / 2, 1.75, L + LW / 2, 1.15)
    arrow(ax, Rx + RW / 2, 1.75, Rx + RW / 2, 1.15)
    fig.savefig(OUT + r"\fig1_prisma.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

if __name__ == "__main__":
    fig_prisma()
