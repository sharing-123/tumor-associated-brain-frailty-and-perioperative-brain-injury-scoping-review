import os, sys, shutil
sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import figs as F
import figs2 as F2
import fig_prisma as FP

DST = "../outputs/JNA_submission/Figures"
os.makedirs(DST, exist_ok=True)
MAP = {"fig1_prisma.png": "Figure 1", "fig3_evidence_map.png": "Figure 2", "fig5_twohit_jna.png": "Figure 3"}
orig = Figure.savefig

def patched(self, fname, *a, **k):
    orig(self, fname, *a, **k)
    base = os.path.basename(str(fname))
    if base in MAP:
        k2 = {kk: vv for kk, vv in k.items() if kk != "dpi"}
        k2["pad_inches"] = 0.02
        orig(self, os.path.join(DST, MAP[base] + ".pdf"), *a, format="pdf", **k2)

Figure.savefig = patched

def fig_twohit_jna():
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(3.7, 8.0)
    ax.axis("off")
    cols = [
        (0.1, F2.AMBER, "#fdf1dc", "FIRST HIT, TUMOR",
         "Mass effect and peritumoral edema\nBarrier leak, microvessel defect\nMacrophage-rich inflammation\n\nBaseline impairment\nCognition impaired before surgery\nin 8 of 8 studies that tested it"),
        (3.5, F2.RED, "#f9e4e0", "SECOND HIT, SURGERY",
         "Craniotomy, retraction, vessel injury\nAnesthetic and hemodynamic load\n\nNew DWI lesions in 19% to 46%\nS100B, GFAP, NfL rise after surgery\nInflammatory amplification\n(hypothesized)"),
        (6.9, F2.TEAL, "#e3f2f4", "OBSERVED OUTCOMES",
         "Delirium or agitation, 4.2% to 35%\nEarly cognitive decline, often\nrecovering\nNew neurologic deficit\nLonger stay, non-home discharge,\nmortality across frailty strata"),
    ]
    for x, ec, fc, head, body in cols:
        F2.rbox(ax, x, 3.9, 3.0, 3.9, fc, ec, 1.8)
        ax.text(x + 1.5, 7.35, head, ha="center", va="center", fontsize=7.2, fontweight="bold", color=ec)
        ax.text(x + 1.5, 5.5, body, ha="center", va="center", fontsize=6.2, linespacing=1.45)
    F2.arrow(ax, 3.1, 5.85, 3.5, 5.85)
    F2.arrow(ax, 6.5, 5.85, 6.9, 5.85)
    fig.savefig(F.OUT + "/fig5_twohit_jna.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

if __name__ == "__main__":
    FP.fig_prisma()
    F2.fig_map()
    fig_twohit_jna()
    F.fig_characteristics()
    F2.fig_framework()
    for f in sorted(os.listdir(DST)):
        print(f, os.path.getsize(os.path.join(DST, f)))
