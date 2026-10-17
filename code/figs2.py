import sys
sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D
from data_core import *
import figs as F

OUT = F.OUT
NAVY, TEAL, BLUE, AMBER, RED, GRAY = F.NAVY, F.TEAL, F.BLUE, F.AMBER, F.RED, F.GRAY

def rbox(ax, x, y, w, h, fc, ec, lw=1.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08", fc=fc, ec=ec, lw=lw))

def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=10, lw=1.2, color=NAVY, shrinkA=0, shrinkB=0))

def fig_map():
    M = F.map_matrix()
    nr, nc = len(F.ROWS), len(F.COLS)
    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    ax.set_xlim(-0.6, 1.6 * (nc - 1) + 0.6)
    ax.set_ylim(nr - 0.45, -0.75)
    ax.set_aspect("equal")
    for i, (f, lab) in enumerate(F.ROWS):
        for j, t in enumerate(F.COLS):
            n, share, ids = M[(f, t)]
            if n == 0:
                ax.text(1.6 * j, i, "0", ha="center", va="center", fontsize=7, color="#9aa5ae")
                continue
            col = GRAY if share is None else (TEAL if share >= 0.75 else (AMBER if share >= 0.25 else GRAY))
            r = min(0.14 + 0.075 * n ** 0.5, 0.46)
            ax.add_patch(Circle((1.6 * j, i), r, fc=col, ec="white", lw=1.2))
            ax.text(1.6 * j, i, str(n), ha="center", va="center", fontsize=8, color="white", fontweight="bold")
    ax.set_yticks(range(nr))
    ax.set_yticklabels([r[1] for r in F.ROWS], fontsize=7.6)
    ax.set_xticks([1.6 * j for j in range(nc)])
    ax.set_xticklabels(["Glioma", "Meningioma", "Mixed tumor\ntypes", "Metastasis"], fontsize=7.8)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    ax.grid(True, color="#e3e8ec", lw=0.7)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)
    leg = [Line2D([0], [0], marker="o", color="w", markerfacecolor=TEAL, markersize=8, label="75% or more at level 2"),
           Line2D([0], [0], marker="o", color="w", markerfacecolor=AMBER, markersize=8, label="25% to 74% at level 2"),
           Line2D([0], [0], marker="o", color="w", markerfacecolor=GRAY, markersize=8, label="Under 25% or ungraded")]
    ax.legend(handles=leg, loc="upper center", bbox_to_anchor=(0.45, -0.01), ncol=3, frameon=False, fontsize=6.8)
    fig.savefig(OUT + r"\fig3_evidence_map.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

def fig_framework():
    fig, ax = plt.subplots(figsize=(7.6, 6.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    rbox(ax, 2.2, 8.7, 5.6, 1.0, NAVY, NAVY)
    ax.text(5.0, 9.2, "Tumor-associated brain frailty\nworking construct proposed in this review", ha="center", va="center", color="white", fontsize=7.8, fontweight="bold", linespacing=1.4)
    doms = [
        (0.1, "1  Systemic frailty", TEAL, "7 studies", "mFI-5, mFI-11,\nHopkins score,\nRisk Analysis Index,\nFried phenotype", "General-surgery indices\nwith no brain item\nThresholds vary"),
        (2.6, "2  Cognitive", BLUE, "30 studies", "Test batteries,\nMMSE and MoCA,\ncomputerized tests,\npatient report", "No common tool\nNo MoCA-INA in the\nmapped trials"),
        (5.1, "3  Neurological", AMBER, "16 studies", "KPS, NIHSS, mRS,\nGOS, Barthel,\nbinary new deficit", "No study used NANO\nor NANO-Ina"),
        (7.6, "4  Imaging", RED, "32 studies", "DWI infarcts,\nvolumetry, perfusion,\nconnectivity,\nCT findings", "No brain frailty score\nNo CT or temporal\nmuscle metric"),
    ]
    W = 2.3
    ax.plot([0.1 + W / 2, 7.6 + W / 2], [8.35, 8.35], color=NAVY, lw=1.1)
    ax.plot([5.0, 5.0], [8.35, 8.7], color=NAVY, lw=1.1)
    for x, t, c, n, tools, gap in doms:
        ax.plot([x + W / 2, x + W / 2], [7.75, 8.35], color=NAVY, lw=1.1)
        rbox(ax, x, 3.9, W, 3.85, "white", c, 1.8)
        rbox(ax, x, 7.1, W, 0.65, c, c, 1.8)
        ax.text(x + W / 2, 7.42, t, ha="center", va="center", color="white", fontsize=7.6, fontweight="bold")
        ax.text(x + W / 2, 6.75, n, ha="center", va="center", fontsize=7.4, fontweight="bold", color=NAVY)
        ax.text(x + 0.12, 6.0, tools, ha="left", va="center", fontsize=6.3, linespacing=1.35)
        ax.text(x + 0.12, 5.0, "Gap", ha="left", va="center", fontsize=6.3, fontweight="bold", color=c)
        ax.text(x + 0.12, 4.75, gap, ha="left", va="top", fontsize=6.0, linespacing=1.3)
        ax.plot([x + W / 2, x + W / 2], [3.9, 3.35], color=NAVY, lw=1.0, linestyle=(0, (3, 2)))
    rbox(ax, 0.1, 1.55, 9.8, 1.8, "#f4f6f8", NAVY, 1.1)
    ax.text(5.0, 2.45, "Shared candidate mechanism, neuroinflammation and barrier injury\n"
            "IL-6, IL-8, TNF-alpha, CD68, CD163, VEGF, S100B, NSE, GFAP, tau, NfL\n"
            "7 studies measured inflammatory or tumor-tissue markers and 12 measured brain injury markers\n"
            "No mapped study reported meningioma-specific cytokine data",
            ha="center", va="center", fontsize=6.6, linespacing=1.5)
    arrow(ax, 5.0, 1.55, 5.0, 1.15)
    rbox(ax, 0.1, 0.1, 9.8, 1.05, "#e3f2f4", NAVY, 1.1)
    ax.text(5.0, 0.62, "Working hypothesis for perioperative care\nThe tumor supplies a first hit. Craniotomy and anesthesia can supply a second hit.",
            ha="center", va="center", fontsize=6.8, linespacing=1.5)
    fig.savefig(OUT + r"\fig4_framework.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

def fig_twohit():
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    cols = [
        (0.1, AMBER, "#fdf1dc", "FIRST HIT, TUMOR",
         "Mass effect and peritumoral edema\nBarrier leak, microvessel defect\nMacrophage-rich inflammation\n\nBaseline impairment\nCognition impaired before surgery\nin 8 of 8 studies that tested it"),
        (3.5, RED, "#f9e4e0", "SECOND HIT, SURGERY",
         "Craniotomy, retraction, vessel injury\nAnesthetic and hemodynamic load\n\nNew DWI lesions in 19% to 46%\nS100B, GFAP, NfL rise after surgery\nInflammatory amplification\n(hypothesized)"),
        (6.9, TEAL, "#e3f2f4", "OBSERVED OUTCOMES",
         "Delirium or agitation, 4.2% to 35%\nEarly cognitive decline, often\nrecovering\nNew neurologic deficit\nLonger stay, non-home discharge,\nmortality across frailty strata"),
    ]
    for x, ec, fc, head, body in cols:
        rbox(ax, x, 3.9, 3.0, 3.9, fc, ec, 1.8)
        ax.text(x + 1.5, 7.35, head, ha="center", va="center", fontsize=7.2, fontweight="bold", color=ec)
        ax.text(x + 1.5, 5.5, body, ha="center", va="center", fontsize=6.2, linespacing=1.45)
    arrow(ax, 3.1, 5.85, 3.5, 5.85)
    arrow(ax, 6.5, 5.85, 6.9, 5.85)
    rbox(ax, 0.1, 2.0, 3.0, 1.4, "#f4f6f8", NAVY, 1.0)
    ax.text(1.6, 2.7, "Reserve is described by the four domains\nsystemic frailty, cognition,\nneurological function, imaging", ha="center", va="center", fontsize=6.0, linespacing=1.45)
    arrow(ax, 1.6, 3.9, 1.6, 3.4)
    rbox(ax, 3.5, 2.0, 6.4, 1.4, "#f4f6f8", NAVY, 1.0)
    ax.text(6.7, 2.7, "No core study tested the interaction between the two hits\nPresurgical cognition predicted early postsurgical cognition and frailty strata\npredicted delirium, which fits the model without proving it",
            ha="center", va="center", fontsize=6.0, linespacing=1.45)
    rbox(ax, 0.1, 0.1, 9.8, 1.5, "#e9edf2", NAVY, 1.0)
    ax.text(5.0, 0.85, "Outcome after surgery reflects the combined load of both hits\nStudies that measure the tumor-related state before surgery and the injury signal after surgery\nin the same patients are needed to estimate each contribution and their interaction",
            ha="center", va="center", fontsize=6.6, linespacing=1.5)
    fig.savefig(OUT + r"\fig5_twohit.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

if __name__ == "__main__":
    fig_map()
    fig_framework()
    fig_twohit()
