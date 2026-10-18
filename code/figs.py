import sys, json, collections
sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from data_core import *
from prisma_numbers import P
from fig_prisma import fig_prisma

OUT = "figs"
ST = json.load(open("stats.json"))
YEAR = {int(k): v for k, v in ST["YEAR"].items()}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
TEAL, BLUE, AMBER, GRAY, RED, NAVY = "#1b7f8c", "#3b6ea5", "#e0a030", "#8c9aa5", "#b5483a", "#1f3b57"

def box(ax, x, y, w, h, text, fc="white", ec=NAVY, fs=7.4, bold=False, align="left", lw=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.06", fc=fc, ec=ec, lw=lw))
    ha = {"left": "left", "center": "center"}[align]
    tx = x + 0.1 if align == "left" else x + w / 2
    ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=fs, fontweight="bold" if bold else "normal", linespacing=1.35)

def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=9, lw=1.0, color=NAVY, shrinkA=0, shrinkB=0))

def fig_characteristics():
    fig, axs = plt.subplots(2, 2, figsize=(7.4, 6.2))

    a = axs[0, 0]
    bins = [(1985, 1999), (2000, 2004), (2005, 2009), (2010, 2014), (2015, 2019), (2020, 2026)]
    lab = ["1987-1999", "2000-2004", "2005-2009", "2010-2014", "2015-2019", "2020-2026"]
    cnt = [sum(1 for y in YEAR.values() if lo <= y <= hi) for lo, hi in bins]
    a.bar(lab, cnt, color=TEAL)
    for i, v in enumerate(cnt):
        a.text(i, v + 0.4, str(v), ha="center", fontsize=7.5)
    a.set_title("A  Publication period", loc="left", fontsize=8.5, fontweight="bold")
    a.set_ylabel("Studies"); a.tick_params(axis="x", labelrotation=35, labelsize=7)

    b = axs[0, 1]
    order = ["Prospective cohort", "RCT", "Retrospective cohort", "Registry cohort", "Case-control", "Case series", "Mechanistic laboratory study", "Trial protocol", "Cross-sectional study", "Non-randomized pilot trial", "Secondary analysis of RCT"]
    des = collections.Counter(R[n][2] for n in R)
    ys = [des[o] for o in order][::-1]
    b.barh([o for o in order][::-1], ys, color=BLUE)
    for i, v in enumerate(ys):
        b.text(v + 0.4, i, str(v), va="center", fontsize=7.5)
    b.set_title("B  Study design", loc="left", fontsize=8.5, fontweight="bold"); b.tick_params(axis="y", labelsize=7)

    c = axs[1, 0]
    tu = collections.Counter(R[n][3] for n in R)
    names = ["Mixed", "Glioma", "Meningioma", "Metastasis"]
    cols = [GRAY, AMBER, TEAL, RED]
    vals = [tu[k] for k in names]
    c.bar(names, vals, color=cols)
    for i, v in enumerate(vals):
        c.text(i, v + 0.6, str(v), ha="center", fontsize=7.5)
    c.set_title("C  Tumor category of study sample", loc="left", fontsize=8.5, fontweight="bold"); c.set_ylabel("Studies"); c.tick_params(axis="x", labelsize=7.5)

    d = axs[1, 1]
    st = collections.Counter(R[n][4] for n in R)
    short = {"S1": "Tumor biology and\nblood-brain barrier", "S2": "Systemic frailty indices", "S3": "Cognitive trajectories", "S4": "Delirium and agitation", "S5": "Brain injury, imaging,\nbiomarkers", "S6": "Perioperative\ninterventions"}
    keys = ["S3", "S6", "S5", "S1", "S4", "S2"]
    vv = [st[k] for k in keys][::-1]
    d.barh([short[k] for k in keys][::-1], vv, color=NAVY)
    for i, v in enumerate(vv):
        d.text(v + 0.3, i, str(v), va="center", fontsize=7.5)
    d.set_title("D  Evidence stream", loc="left", fontsize=8.5, fontweight="bold"); d.tick_params(axis="y", labelsize=7)
    fig.tight_layout()
    fig.savefig(OUT + "/fig2_characteristics.png", dpi=300, facecolor="white")
    plt.close(fig)

ROWS = [
    ("F", "Systemic frailty indices"),
    ("C", "Cognitive testing"),
    ("N", "Neurological or functional outcome"),
    ("I", "Imaging"),
    ("B", "Brain injury biomarkers"),
    ("M", "Neuroinflammatory or tumor-tissue markers"),
    ("D", "Delirium or agitation"),
    ("H", "Hemodynamic or cerebral physiology"),
    ("T", "Tumor biology and blood-brain barrier"),
]
COLS = ["Glioma", "Meningioma", "Mixed", "Metastasis"]

def map_matrix():
    M = {}
    for f, _ in ROWS:
        for t in COLS:
            ids = [n for n in R if f in R[n][9] and R[n][3] == t and R[n][2] != "Trial protocol"]
            graded = [n for n in ids if level(n) != "NG"]
            share = (sum(1 for n in graded if level(n) == "2") / len(graded)) if graded else None
            M[(f, t)] = (len(ids), share, ids)
    return M

def fig_map():
    M = map_matrix()
    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    ax.set_xlim(-0.6, 3.6); ax.set_ylim(-0.7, len(ROWS) - 0.3)
    ax.invert_yaxis()
    for i, (f, lab) in enumerate(ROWS):
        for j, t in enumerate(COLS):
            n, share, ids = M[(f, t)]
            if n == 0:
                ax.text(j, i, "0", ha="center", va="center", fontsize=7, color="#9aa5ae")
                continue
            col = GRAY if share is None else (TEAL if share >= 0.75 else (AMBER if share >= 0.25 else GRAY))
            r = 0.13 + 0.057 * (n ** 0.5) * 1.5
            ax.add_patch(Circle((j, i), min(r, 0.46), fc=col, ec="white", lw=1.2, alpha=0.95))
            ax.text(j, i, str(n), ha="center", va="center", fontsize=8, color="white", fontweight="bold")
    ax.set_yticks(range(len(ROWS))); ax.set_yticklabels([r[1] for r in ROWS], fontsize=7.8)
    ax.set_xticks(range(len(COLS))); ax.set_xticklabels([c if c != "Mixed" else "Mixed tumor types" for c in COLS], fontsize=8)
    ax.xaxis.tick_top(); ax.tick_params(length=0)
    ax.grid(True, color="#e3e8ec", lw=0.7); ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)
    from matplotlib.lines import Line2D
    leg = [Line2D([0], [0], marker="o", color="w", markerfacecolor=TEAL, markersize=9, label="75% or more of graded studies at level 2"),
           Line2D([0], [0], marker="o", color="w", markerfacecolor=AMBER, markersize=9, label="25% to 74% at level 2"),
           Line2D([0], [0], marker="o", color="w", markerfacecolor=GRAY, markersize=9, label="Under 25% at level 2, or ungraded")]
    ax.legend(handles=leg, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT + "/fig3_evidence_map.png", dpi=300, facecolor="white")
    plt.close(fig)
    return M

def fig_framework():
    fig, ax = plt.subplots(figsize=(7.4, 6.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    box(ax, 2.6, 8.6, 4.8, 1.0, "Tumor-associated brain frailty\n(working construct proposed by this review)", fc=NAVY, ec=NAVY, fs=8.4, bold=True, align="center")
    ax.texts[-1].set_color("white")
    doms = [
        (0.2, "1  Systemic frailty", "7 studies\nmFI-5, mFI-11, Hopkins score,\nRisk Analysis Index, Fried phenotype\n\nGap\nGeneral-surgery indices, no brain\nspecific item, thresholds vary", TEAL),
        (2.7, "2  Cognitive", "30 studies\nBatteries, screeners (MMSE, MoCA),\ncomputerized tests, patient report\n\nGap\nNo common tool, no MoCA-INA\nin the mapped trials", BLUE),
        (5.2, "3  Neurological", "16 studies\nKPS, NIHSS, mRS, GOS, Barthel,\nbinary new deficit\n\nGap\nNo study used NANO or NANO-Ina", AMBER),
        (7.7, "4  Imaging", "32 studies\nDWI infarcts, volumetry, perfusion,\nconnectivity, CT findings\n\nGap\nNo brain frailty score, no CT or\ntemporal muscle metric", RED),
    ]
    for x, t, body, c in doms:
        ax.add_patch(FancyBboxPatch((x, 3.9), 2.1, 3.9, boxstyle="round,pad=0,rounding_size=0.08", fc="white", ec=c, lw=1.8))
        ax.add_patch(FancyBboxPatch((x, 7.1), 2.1, 0.7, boxstyle="round,pad=0,rounding_size=0.08", fc=c, ec=c, lw=1.8))
        ax.text(x + 1.05, 7.45, t, ha="center", va="center", fontsize=7.8, fontweight="bold", color="white")
        ax.text(x + 0.1, 5.45, body, ha="left", va="center", fontsize=6.4, linespacing=1.4)
        arrow(ax, x + 1.05, 7.8, 5.0 if False else 5.0, 8.6) if False else None
        ax.plot([x + 1.05, x + 1.05], [7.8, 8.2], color=NAVY, lw=1.0)
    ax.plot([1.25, 8.75], [8.2, 8.2], color=NAVY, lw=1.0)
    ax.plot([5.0, 5.0], [8.2, 8.6], color=NAVY, lw=1.0)
    box(ax, 0.2, 1.6, 9.6, 1.7,
        "Shared candidate mechanism, neuroinflammation and barrier injury\n"
        "Cytokines (IL-6, IL-8, TNF-alpha), macrophage markers (CD68, CD163), VEGF, S100B, NSE, GFAP, tau, NfL\n"
        "7 studies measured inflammatory or tumor-tissue markers, 12 measured brain injury markers\n"
        "Meningioma-specific cytokine data in the mapped set: none", fc="#f4f6f8", fs=7.2, align="center")
    for x in (1.25, 3.75, 6.25, 8.75):
        ax.plot([x, x], [3.9, 3.3], color=NAVY, lw=1.0, linestyle=(0, (3, 2)))
    box(ax, 0.2, 0.15, 9.6, 1.0,
        "Hypothesis for perioperative care\nThe tumor supplies the first hit. Craniotomy and anesthesia can supply a second hit (perioperative brain injury).",
        fc="#e3f2f4", fs=7.3, align="center")
    arrow(ax, 5.0, 1.6, 5.0, 1.15)
    fig.savefig(OUT + "/fig4_framework.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

def fig_twohit():
    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off")
    box(ax, 0.1, 4.0, 3.0, 3.6,
        "FIRST HIT\nTumor\n\nMass effect and peritumoral edema\nBarrier leak and microvessel defect\nMacrophage dominated inflammation\n\nBaseline impairment\nCognition impaired before surgery\nin 8 of 8 studies that tested it",
        fc="#fdf1dc", ec=AMBER, fs=6.6, align="center", lw=1.6)
    box(ax, 3.5, 4.0, 3.0, 3.6,
        "SECOND HIT\nPerioperative brain injury\n\nCraniotomy, retraction, vessel injury\nAnesthetic and hemodynamic exposure\n\nNew DWI lesions in 19% to 46%\nS100B, GFAP, NfL rise after surgery\nNeuroinflammatory amplification (hypothesized)",
        fc="#f9e4e0", ec=RED, fs=6.6, align="center", lw=1.6)
    box(ax, 6.9, 4.0, 3.0, 3.6,
        "OBSERVED OUTCOMES\n\nDelirium or agitation 4.2% to 35%\nEarly cognitive decline, often recovering\nNew neurologic deficit\nLonger stay, non-home discharge,\nmortality (frailty strata)",
        fc="#e3f2f4", ec=TEAL, fs=6.6, align="center", lw=1.6)
    arrow(ax, 3.1, 5.8, 3.5, 5.8); arrow(ax, 6.5, 5.8, 6.9, 5.8)

    ax.text(5.0, 3.55, "Reduced reserve", ha="center", fontsize=7.4, fontweight="bold", color=NAVY)
    arrow(ax, 1.6, 4.0, 1.6, 3.2)
    box(ax, 0.1, 2.2, 3.0, 1.0, "Systemic frailty indices, cognitive screening,\nneurological scales, imaging, and markers\n(domains of the working construct)", fc="#f4f6f8", fs=6.3, align="center")
    box(ax, 3.5, 2.2, 6.4, 1.0, "Interaction between the two hits was not tested in any of the 70 core studies\nPresurgical cognition did predict early postsurgical cognition (Zangrossi), and frailty strata\npredicted delirium (Wang), which fits the model but does not prove it", fc="#f4f6f8", fs=6.3, align="center")
    box(ax, 0.1, 0.2, 9.8, 1.4, "Outcome after surgery reflects the combined load of both hits\nStudies that measure the tumor-related state before surgery and the injury signal after surgery in the same patients\nare needed to estimate each contribution and their interaction", fc="#e9edf2", fs=7.0, align="center")
    fig.savefig(OUT + "/fig5_twohit.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

if __name__ == "__main__":
    fig_prisma(); fig_characteristics(); M = fig_map(); fig_framework(); fig_twohit()
    for (f, t), (n, s, ids) in M.items():
        if n: print(f, t, n, None if s is None else round(s, 2), ids)
