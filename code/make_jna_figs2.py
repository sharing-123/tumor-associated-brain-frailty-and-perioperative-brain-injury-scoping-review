import os, sys, json, collections
sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["font.family"] = "Arial"
matplotlib.rcParams["font.size"] = 8
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
from data_core import R, level
import figs as F
matplotlib.rcParams["font.family"] = "Arial"
matplotlib.rcParams["font.size"] = 8
matplotlib.rcParams["axes.spines.top"] = False
matplotlib.rcParams["axes.spines.right"] = False

FIGS = "figs"
NAVY, TEAL, GOLD, BRICK, SLATE, LIGHT, INK, MUTE = "#0E4A6B", "#3A8F8F", "#D6A64E", "#B5573F", "#8795A1", "#D9DCDF", "#1F2933", "#5F6B76"
ST = json.load(open("stats.json"))
YEAR = {int(k): v for k, v in ST["YEAR"].items()}

def save(fig, name, pad=0.04):
    fig.savefig(os.path.join(FIGS, name + ".png"), dpi=300, bbox_inches="tight", pad_inches=pad, facecolor="white")
    fig.savefig(os.path.join(FIGS, name + ".pdf"), bbox_inches="tight", pad_inches=pad, facecolor="white")
    plt.close(fig)

def evidence_map():
    M = F.map_matrix()
    rows = [(f, lab) for f, lab in F.ROWS]
    cols = ["Glioma", "Meningioma", "Mixed", "Metastasis"]
    col_lab = {"Glioma": "Glioma", "Meningioma": "Meningioma", "Mixed": "Mixed tumor\ntypes", "Metastasis": "Brain\nmetastasis"}
    ncol = {t: sum(1 for n in R if R[n][3] == t) for t in cols}
    nr = len(rows)
    fig = plt.figure(figsize=(7.4, 5.2))
    ax = fig.add_axes([0.27, 0.10, 0.55, 0.74])
    ax.set_xlim(-0.6, len(cols) - 0.4)
    ax.set_ylim(nr - 0.45, -0.55)
    for i in range(nr):
        ax.axhline(i, color="#E6E8EA", lw=0.8, zorder=0)
    for j in range(len(cols)):
        ax.axvline(j, color="#E6E8EA", lw=0.8, zorder=0)
    def colr(share):
        if share is None:
            return LIGHT
        return NAVY if share >= 0.75 else (GOLD if share >= 0.25 else SLATE)
    for i, (f, lab) in enumerate(rows):
        for j, t in enumerate(cols):
            n, share, ids = M[(f, t)]
            if n == 0:
                ax.scatter(j, i, s=60, facecolor="white", edgecolor=SLATE, lw=0.8, zorder=2)
                ax.text(j, i, "0", ha="center", va="center", fontsize=6.5, color=MUTE, zorder=3)
                continue
            s = 150 + 21 * n
            c = colr(share)
            ax.scatter(j, i, s=s, facecolor=c, edgecolor="white", lw=0.8, zorder=2)
            ax.text(j, i, str(n), ha="center", va="center", fontsize=7, color="white" if c in (NAVY, SLATE) else INK, fontweight="bold", zorder=3)
    ax.set_yticks(range(nr))
    ax.set_yticklabels([lab for _, lab in rows], fontsize=8, color=INK)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(["%s\n(n = %d)" % (col_lab[t], ncol[t]) for t in cols], fontsize=8, color=INK)
    ax.xaxis.tick_top()
    ax.tick_params(length=0, pad=6)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xlabel("Tumor category of the study sample", fontsize=8.5, color=INK, labelpad=8)
    ax.xaxis.set_label_position("bottom")
    size_h = [Line2D([0], [0], marker="o", ls="", markerfacecolor="white", markeredgecolor=SLATE, markersize=((150 + 21 * n) ** 0.5), label=str(n)) for n in (1, 5, 10, 20)]
    l1 = fig.legend(handles=size_h, title="Studies, n", loc="upper left", bbox_to_anchor=(0.835, 0.86), frameon=False, labelspacing=1.5, fontsize=8, title_fontsize=8.5, handletextpad=1.0, borderpad=0)
    l1._legend_box.align = "left"
    col_h = [Line2D([0], [0], marker="o", ls="", markerfacecolor=c, markeredgecolor=SLATE if c == LIGHT else "white", markersize=9, label=lb) for c, lb in
             ((NAVY, "75% or more"), (GOLD, "25% to 74%"), (SLATE, "Under 25%"), (LIGHT, "No graded study"))]
    fig.legend(handles=col_h, title="Share of graded studies\nat level 2", loc="upper left", bbox_to_anchor=(0.835, 0.42), frameon=False, labelspacing=0.9, fontsize=8, title_fontsize=8.5, handletextpad=0.6, borderpad=0)
    save(fig, "jna_fig2_evidence_map")

def rbox(ax, x, y, w, h, fc, ec, lw=1.0, r=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=%s" % r, fc=fc, ec=ec, lw=lw, zorder=1))

def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.4, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=11, lw=lw, color=color, shrinkA=0, shrinkB=0, linestyle=ls, zorder=3))

def two_hit():
    rows = [
        ("H", "FIRST HIT, THE TUMOR", GOLD),
        ("R", "Systemic frailty linked to worse outcome", 7, "c"),
        ("R", "Cognition impaired before surgery", 8, "c"),
        ("R", "Inflammatory or tumor-tissue markers", 7, "m"),
        ("H", "SECOND HIT, SURGERY AND ANESTHESIA", NAVY),
        ("R", "New diffusion-weighted lesions after resection", 6, "c"),
        ("R", "Postoperative rise of brain injury markers", 4, "c"),
        ("R", "Delirium or agitation", 7, "m"),
        ("R", "Hemodynamic findings", 3, "m"),
        ("H", "LINK BETWEEN THE TWO HITS", BRICK),
        ("R", "Preoperative state predicts postoperative course", 4, "c"),
        ("R", "Interventions aimed at the second hit", 11, "m"),
        ("R", "Interaction between the hits tested", 0, "n"),
    ]
    col = {"c": NAVY, "m": GOLD, "n": BRICK}
    n = len(rows)
    fig = plt.figure(figsize=(7.4, 4.9))
    ax = fig.add_axes([0.42, 0.14, 0.38, 0.82])
    ax.set_ylim(n - 0.4, -0.7)
    ax.set_xlim(-0.6, 13)
    for x in (0, 2, 4, 6, 8, 10, 12):
        ax.axvline(x, color="#E6E8EA", lw=0.8, zorder=0)
    ax.set_yticks([])
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(SLATE)
    ax.tick_params(axis="x", length=0, labelsize=7.6, colors=INK)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
    ax.set_xlabel("Core studies, n", fontsize=8.4, color=INK, labelpad=6)
    ytrans = ax.get_yaxis_transform()
    for i, r in enumerate(rows):
        if r[0] == "H":
            ax.text(-0.03, i, r[1], transform=ytrans, fontsize=7.2, fontweight="bold", color=r[2], ha="right", va="center")
            if i > 0:
                ax.axhline(i - 0.55, color="#C9CED3", lw=0.8, zorder=1)
            continue
        _, lab, v, k = r
        c = col[k]
        ax.text(-0.03, i, lab, transform=ytrans, fontsize=8, color=INK, ha="right", va="center")
        if v == 0:
            ax.scatter(0, i, s=95, facecolor="white", edgecolor=c, lw=1.4, zorder=3)
            ax.text(0.55, i, "0", fontsize=8, color=c, fontweight="bold", va="center")
        else:
            ax.plot([0, v], [i, i], color=c, lw=2.2, solid_capstyle="round", zorder=2)
            ax.scatter(v, i, s=95, facecolor=c, edgecolor="white", lw=0.8, zorder=3)
            ax.text(v + 0.5, i, str(v), fontsize=8, color=INK, fontweight="bold", va="center")
    leg = [Line2D([0], [0], marker="o", ls="", markerfacecolor=NAVY, markeredgecolor="white", markersize=8, label="Studies point the same way"),
           Line2D([0], [0], marker="o", ls="", markerfacecolor=GOLD, markeredgecolor="white", markersize=8, label="Studies differ or are not\ncomparable"),
           Line2D([0], [0], marker="o", ls="", markerfacecolor="white", markeredgecolor=BRICK, markeredgewidth=1.4, markersize=8, label="No study")]
    fig.legend(handles=leg, title="Direction of findings", loc="upper left", bbox_to_anchor=(0.83, 0.56), frameon=False, labelspacing=1.0, fontsize=7.6, title_fontsize=8.2, handletextpad=0.5, borderpad=0)
    save(fig, "jna_fig3_two_hit")

def characteristics():
    fig, axs = plt.subplots(2, 2, figsize=(7.4, 6.0))
    plt.subplots_adjust(hspace=0.36, wspace=0.62, left=0.2, right=0.97, top=0.93, bottom=0.08)

    def style(ax, horizontal):
        for s in ("top", "right", "left" if horizontal else "bottom"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom" if horizontal else "left"].set_color(SLATE)
        ax.tick_params(length=0, labelsize=7.4, colors=INK)
        ax.grid(axis="x" if horizontal else "y", color="#E6E8EA", lw=0.8)
        ax.set_axisbelow(True)

    def hbars(ax, labels, vals, color, letter, title, xmax=None):
        y = list(range(len(labels)))[::-1]
        ax.barh(y, vals, color=color, height=0.62)
        ax.set_yticks(y)
        ax.set_yticklabels(labels)
        for yy, v in zip(y, vals):
            ax.text(v + (xmax or max(vals)) * 0.02, yy, str(v), va="center", fontsize=7.4, color=INK)
        ax.set_xlim(0, (xmax or max(vals)) * 1.15)
        style(ax, True)
        ax.set_title(letter + "   " + title, loc="left", fontsize=8.8, fontweight="bold", color=INK, x=-0.9 if letter in ("B", "D") else -0.62)

    a = axs[0, 0]
    bins = [(1985, 1999), (2000, 2004), (2005, 2009), (2010, 2014), (2015, 2019), (2020, 2026)]
    lab = ["1987 to 1999", "2000 to 2004", "2005 to 2009", "2010 to 2014", "2015 to 2019", "2020 to 2026"]
    cnt = [sum(1 for y in YEAR.values() if lo <= y <= hi) for lo, hi in bins]
    hbars(a, lab, cnt, NAVY, "A", "Publication period")
    order = ["Prospective cohort", "RCT", "Retrospective cohort", "Registry cohort", "Case-control", "Case series", "Mechanistic laboratory study", "Trial protocol", "Cross-sectional study", "Non-randomized pilot trial", "Secondary analysis of RCT"]
    nice = {"RCT": "Randomized trial", "Secondary analysis of RCT": "Secondary analysis of trial", "Mechanistic laboratory study": "Mechanistic laboratory", "Non-randomized pilot trial": "Non-randomized pilot"}
    des = collections.Counter(R[n][2] for n in R)
    hbars(axs[0, 1], [nice.get(o, o) for o in order], [des[o] for o in order], TEAL, "B", "Study design")
    tu = collections.Counter(R[n][3] for n in R)
    names = ["Mixed", "Glioma", "Meningioma", "Metastasis"]
    nm = {"Mixed": "Mixed tumor types", "Metastasis": "Brain metastasis"}
    hbars(axs[1, 0], [nm.get(k, k) for k in names], [tu[k] for k in names], GOLD, "C", "Tumor category")
    st = collections.Counter(R[n][4] for n in R)
    short = {"S1": "Tumor biology and barrier", "S2": "Systemic frailty", "S3": "Cognitive trajectories", "S4": "Delirium or agitation", "S5": "Perioperative brain injury", "S6": "Interventions and protocols"}
    keys = ["S3", "S6", "S5", "S1", "S4", "S2"]
    hbars(axs[1, 1], [short[k] for k in keys], [st[k] for k in keys], BRICK, "D", "Evidence stream")
    save(fig, "jna_sdc_characteristics")

def framework():
    fig, ax = plt.subplots(figsize=(7.4, 6.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10.6)
    ax.axis("off")
    rbox(ax, 3.0, 9.35, 6.0, 1.05, NAVY, NAVY)
    ax.text(6.0, 9.88, "Tumor-associated brain frailty", color="white", fontsize=10.5, fontweight="bold", ha="center", va="center", zorder=4)
    ax.text(6.0, 9.55, "working construct proposed in this review", color="#D5E3EC", fontsize=7.4, ha="center", va="center", zorder=4)
    doms = [
        (NAVY, "Systemic frailty", "7", ["mFI-5 and mFI-11", "Hopkins Frailty Score", "Risk Analysis Index", "Fried phenotype"], ["General-surgery indices", "No brain-specific item", "Thresholds differ"]),
        (TEAL, "Cognition", "30", ["Test batteries", "MMSE and MoCA", "Computerized tests", "Patient-reported scale"], ["No shared tool or time point", "No MoCA-INA in the", "mapped studies"]),
        (GOLD, "Neurological function", "16", ["KPS, mRS, GOS", "NIHSS, Barthel index", "Binary new deficit", "Motor evoked potentials"], ["Nine definitions", "None from neuro-oncology", "No NANO or NANO-Ina"]),
        (BRICK, "Imaging", "32", ["DWI ischemic lesions", "Volumetry, perfusion", "Functional connectivity", "CT findings"], ["No brain frailty score", "No CT or muscle metric"]),
    ]
    W = 2.78
    gap = (12 - 4 * W) / 5
    ax.plot([gap + W / 2, 12 - gap - W / 2], [8.95, 8.95], color=SLATE, lw=1.0, zorder=0)
    ax.plot([6, 6], [8.95, 9.35], color=SLATE, lw=1.0, zorder=0)
    for k, (c, title, n, tools, gaps) in enumerate(doms):
        x = gap + k * (W + gap)
        ax.plot([x + W / 2, x + W / 2], [8.35, 8.95], color=SLATE, lw=1.0, zorder=0)
        rbox(ax, x, 2.75, W, 5.6, "white", c, 1.4)
        ax.add_patch(FancyBboxPatch((x, 7.45), W, 0.9, boxstyle="round,pad=0,rounding_size=0.12", fc=c, ec=c, zorder=2))
        ax.text(x + W / 2, 7.9, title, color="white", fontsize=8.2, fontweight="bold", ha="center", va="center", zorder=4)
        ax.text(x + 0.2, 6.85, n, fontsize=17, fontweight="bold", color=c, va="center", zorder=4)
        ax.text(x + 0.3 + 0.42 * len(n), 6.8, "core studies", fontsize=7, color=MUTE, va="center", zorder=4)
        ax.text(x + 0.2, 6.15, "INSTRUMENTS", fontsize=5.8, fontweight="bold", color=c, va="center", zorder=4)
        for i, t in enumerate(tools):
            ax.text(x + 0.2, 5.78 - 0.38 * i, t, fontsize=6.8, color=INK, va="center", zorder=4)
        ax.text(x + 0.2, 4.1, "GAPS", fontsize=5.8, fontweight="bold", color=c, va="center", zorder=4)
        for i, t in enumerate(gaps):
            ax.text(x + 0.2, 3.72 - 0.33 * i, t, fontsize=6.8, color=INK, va="center", zorder=4)
        ax.plot([x + W / 2, x + W / 2], [2.75, 2.45], color=SLATE, lw=1.0, linestyle=(0, (3, 2)), zorder=0)
    rbox(ax, 0.35, 1.2, 11.3, 1.25, "#F2F4F6", SLATE, 1.0)
    ax.text(6.0, 2.17, "Shared candidate mechanism, neuroinflammation and barrier injury", fontsize=8.2, fontweight="bold", color=INK, ha="center", va="center", zorder=4)
    ax.text(6.0, 1.83, "IL-6, IL-8, TNF-alpha, CD68, CD163, VEGF, S100B, NSE, GFAP, tau, NfL", fontsize=7, color=MUTE, ha="center", va="center", zorder=4)
    ax.text(6.0, 1.5, "Seven studies measured inflammatory or tumor-tissue markers, and 12 measured brain injury markers", fontsize=7, color=MUTE, ha="center", va="center", zorder=4)
    arrow(ax, 6.0, 1.2, 6.0, 0.95, SLATE, 1.2)
    rbox(ax, 0.35, 0.05, 11.3, 0.9, "#E8F0F5", NAVY, 1.0)
    ax.text(6.0, 0.5, "The tumor supplies a first hit, and craniotomy and anesthesia can supply a second hit", fontsize=7.6, fontweight="bold", color=NAVY, ha="center", va="center", zorder=4)
    save(fig, "jna_sdc_framework")

if __name__ == "__main__":
    evidence_map()
    two_hit()
    characteristics()
    framework()
    print("ok")
