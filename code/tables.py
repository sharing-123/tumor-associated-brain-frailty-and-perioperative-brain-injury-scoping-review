import sys
sys.path.insert(0, ".")
from data_core import *
from content_b import ORDER, tok, wd, YEAR, S, PROTO, MEN, GLI, MIX

FLAGNAME = {"F": "Frailty index", "C": "Cognition", "N": "Neurological or functional", "I": "Imaging", "B": "Injury biomarker", "M": "Inflammatory marker", "D": "Delirium", "H": "Hemodynamic", "T": "Tumor biology"}

def lvl(n):
    v = level(n)
    return "Not graded" if v == "NG" else v

def t1():
    rows = []
    last = None
    for n in ORDER:
        if R[n][4] != last:
            last = R[n][4]
            rows.append(["__GROUP__", "%s (n = %d)" % (STREAMS[last], sum(1 for m in R if R[m][4] == last))])
        lab, country, design, tum, st, nn, pop, ctx, fnd, fl = R[n]
        pop = pop.replace("; ", ", ")
        rows.append([f"{lab} {{c:s{n}}}", country, design, pop, ctx, fnd, ", ".join(FLAGNAME[f] for f in fl), lvl(n)])
    return dict(
        caption="Table 1. Characteristics of the 70 studies in the core evidence base, grouped by evidence stream and ordered by year within stream.",
        header=["Study", "Country", "Design", "Population", "Surgical context or intervention", "Main findings", "Domains", "Level"],
        widths=[1.15, 0.7, 0.9, 1.25, 1.25, 3.1, 1.0, 0.45], rows=rows, landscape=True, fs=6.5,
        group_by=("S", None),
        note="Level is the OCEBM 2011 level assigned from design alone and does not judge quality. Domains are the review team coding for each study. CSF, cerebrospinal fluid. DWI, diffusion-weighted imaging. GFAP, glial fibrillary acidic protein. MEP, motor evoked potential. mFI, modified frailty index. MoCA, Montreal Cognitive Assessment. NfL, neurofilament light chain. NSE, neuron-specific enolase. TIVA, total intravenous anesthesia.")

def cnt(ids):
    return len(wd(ids))

def t2():
    ft = FRAILTY_TOOLS
    rows = [
        ["1. Systemic frailty", "7",
         f"mFI-5 (3) {tok(ft['mFI-5'])}, mFI-11 (1) {tok(ft['mFI-11'])}, Hopkins Frailty Score (1) {tok(ft['Hopkins Frailty Score'])}, Risk Analysis Index (1) {tok(ft['Risk Analysis Index'])}, Fried phenotype (1) {tok(ft['Fried phenotype'])}, comorbidity count (1) {tok(ft['Comorbidity count (proxy)'])}",
         "Higher frailty linked to worse outcome or improved by rehabilitation in 7 of 7",
         "General-surgery indices, no brain-specific item, thresholds differ, no glioma-only or meningioma-only sample"],
        ["2. Cognitive", f"{len(wd(S['flag_members']['C']))} (plus 1 protocol)",
         f"Multidomain batteries (14), domain-specific tests (4), brief screeners (7), computerized batteries (4), patient-reported scale (1). MMSE in 5, MoCA in 2 with data, no MoCA-INA",
         "Impaired before surgery in 8 of 8 studies that tested it. After surgery, among 18 cohorts, improved 6, no change 3, decline 3, transient decline 3, others 3",
         "No shared tool or time point, early decline in glioma cohorts, improvement in meningioma cohorts, MMSE-J missed deficits in one study"],
        ["3. Neurological", "16",
         "Binary new deficit (8), Barthel index (5), GOS or GOSE (3), KPS (2), mRS (3), GCS (2), NIHSS (1), House-Brackmann (1), intraoperative MEP (2). No NANO",
         "Deficit rates 6.7% to 50% depending on definition",
         "Nine instruments or definitions, none designed for neuro-oncology"],
        ["4. Imaging", "32",
         "DWI for ischemic lesions (6), volumetric MRI (13), perfusion or permeability (4), functional connectivity (7), CT findings (7), contrast-enhanced ultrasound (1)",
         "New DWI lesions after 18.8% to 45.7% of resections",
         "Imaging describes tumor or injury, no brain frailty score, no CT-based or muscle-based metric"],
    ]
    return dict(caption="Table 2. Candidate domains of tumor-associated brain frailty, instruments identified in the core evidence base, and remaining gaps.",
                header=["Domain", "Studies with data (n)", "Instruments or measures identified", "Direction of the evidence", "Main limitation"],
                widths=[1.0, 0.8, 3.0, 2.1, 2.1], rows=rows, landscape=False, fs=7.0,
                note="Counts are studies, and a study can contribute to more than one row. GCS, Glasgow Coma Scale. GOS, Glasgow Outcome Scale. GOSE, extended Glasgow Outcome Scale. KPS, Karnofsky Performance Status. mRS, modified Rankin Scale. NIHSS, National Institutes of Health Stroke Scale.")

def t3():
    ids = lambda t: S["tumor_members"][t]
    rows = [
        ["Glioma only", str(len(GLI)), f"n = 2 {tok([9, 27])}", f"n = 1 {tok([10])}",
         f"n = 4 {tok([7, 10, 21, 22])}. 44.2%, 45.7%, 31% (new) and 80% (recurrent)", f"n = 3 {tok([11, 19, 35])}", "Not stratified within glioma-only samples"],
        ["Meningioma only", str(len(MEN)), "n = 0", f"n = 3 {tok([15, 28, 61])}",
         f"n = 1 {tok([6])}. 34.9%", f"n = 4 {tok([24, 26, 52, 57])}", f"Meningioma protective in 1 mixed sample {tok([31])}"],
        ["Mixed tumor types", str(len(MIX)), f"n = 5 {tok([1, 33, 62, 66, 69])}", f"n = 8 {tok([23, 39, 50, 51, 53, 64, 66, 69])}",
         f"n = 1 {tok([32])}. 18.8%", f"n = 1 {tok([30])}", f"Higher risk with glioma or malignant tumor in 5 of 6 {tok(HISTOLOGY_DELIRIUM_POS + HISTOLOGY_DELIRIUM_NULL)}"],
        ["Brain metastasis only", "1", "n = 0", "n = 0", "n = 0", "n = 0", "Not applicable"],
    ]
    return dict(caption="Table 3. Neuroinflammation, injury, and vulnerability evidence by tumor category, from the 70 core studies (protocols excluded from counts of data).",
                header=["Tumor category", "Studies (n)", "Inflammatory or tumor-tissue markers", "Brain injury biomarkers", "New DWI lesions after surgery", "Baseline cognitive impairment", "Delirium risk by histology"],
                widths=[1.0, 0.6, 1.1, 1.1, 1.7, 1.1, 1.6], rows=rows, landscape=False, fs=7.0,
                note="Cells show the number of studies with data and, where relevant, the reported incidence. No core study compared inflammatory markers between meningioma and glioma.")

def t4():
    b = BIOMARK
    rows = [
        ["S100B", "Astrocytic calcium-binding protein with a serum half-life of about 30 minutes. Rise marks astrocytic injury or barrier permeability", "Baseline, end of surgery, 24 to 48 h, daily to day 7 in one study", "10", f"Rose after meningioma surgery {tok([15, 28])}. Lower with magnesium {tok([51, 53])}, electroacupuncture {tok([50])}, dexmedetomidine {tok([66])}, lidocaine {tok([69])}. No primary difference with magnesium {tok([39])}. Higher with ciprofol {tok([61])}"],
        ["Neuron-specific enolase", "Neuronal glycolytic enzyme. Rise reflects neuronal injury", "Same schedule as S100B", "7 (plus 1 protocol)", f"Lower with electroacupuncture, dexmedetomidine, lidocaine, and goal-directed fluids {tok([50, 66, 69, 64])}. No difference with magnesium {tok([53])}. Higher with ciprofol {tok([61])}"],
        ["GFAP", "Astrocytic intermediate filament. Also released by glioma cells through a leaky barrier", "Baseline, day 1, 3, 5, 7, 10", "4", f"Rose after surgery and higher with new deficits {tok([10])}. No link with residual tumor {tok([23])}. Lower with fluid strategy and dexmedetomidine {tok([64, 66])}"],
        ["Tau", "Axonal and cortical interneuron protein", "Baseline to day 10", "1", f"Rose on days 1 and 3 {tok([10])}"],
        ["Neurofilament light chain", "Large-caliber axon filament. Late peak suggests continuing axonal degeneration", "Baseline to day 10", "1", f"Rose on days 1 and 3 with a second peak at day 10 {tok([10])}"],
        ["IL-6, IL-8, TNF-alpha", "Cytokines from tumor cells, immune cells, endothelium, injured neurons and astrocytes, and surgical trauma", "Microdialysis every 6 h for 96 h, single tissue samples, or end of surgery and day 1 in trials", "IL-6 5, IL-8 2, TNF-alpha 2 (plus 1 protocol)", f"Rose with grade and necrosis {tok([27])}, peaked early after surgery {tok([1])}, and were lower with dexmedetomidine and lidocaine {tok([66, 69])}"],
        ["VEGF", "Endothelial mitogen and permeability inducer from tumor cells", "Single tissue or CSF sample", "3", f"Correlated with capillary permeability {tok([33])} and with IL-8 {tok([27])}"],
        ["CD45, CD68, CD163", "Tissue markers of leukocytes, macrophages and microglia, and M2 macrophages", "Single sample at resection", "1", f"Macrophage-dominated infiltrate in glioblastoma {tok([9])}"],
    ]
    return dict(caption="Table 4. Biomarkers measured in the core evidence base, with source, interpretation, sampling, and main findings.",
                header=["Marker", "Source and interpretation", "Typical sampling", "Studies with data (n)", "Main findings"],
                widths=[0.9, 2.0, 1.4, 0.8, 3.2], rows=rows, landscape=False, fs=6.8,
                note="IL, interleukin. TNF, tumor necrosis factor. VEGF, vascular endothelial growth factor. Marker interpretation follows the source studies.")

def t5():
    rows = [
        ["New diffusion-weighted lesions after resection", f"{tok([6, 7, 10, 21, 22, 32])}", "18.8% to 45.7% of operations or patients. 31% newly diagnosed versus 80% recurrent glioma", "Linked to permanent deficit, incomplete recovery, and larger tumor, bleeding, and age"],
        ["Postoperative release of injury markers", f"{tok([10, 15, 23, 28])}", "S100B, GFAP, tau, and NfL rose in 4 of 4 studies", "Related to deficits, bleeding, midline shift, and MMSE decline in 3 of 4"],
        ["Delirium or agitation", f"{tok([5, 31, 38, 40, 43, 62, 65])}", "4.2% to 35% in observational cohorts. 28.7% to 46% in control arms", "Higher with frailty, age, malignant histology, frontal approach, longer surgery"],
        ["Cerebral perfusion and autoregulation", f"{tok([8, 64, 65])}", "Autoregulation impaired before surgery in 20% and persisting after. New neurologic events 17.5% versus 40% by fluid strategy", "Mean arterial pressure below 65 mmHg not associated with delirium"],
        ["Preoperative state predicting postoperative course", f"{tok([5, 24, 34, 60])}", "Frailty strata, raised intracranial pressure, presurgical cognition, and connectivity each predicted outcome", "Fits a two-hit sequence, interaction untested"],
        ["Interventions aimed at the second hit", f"{tok([39, 47, 49, 51, 53, 55, 61, 64, 66, 67, 69])}", "Delirium 46% to 22% with dexmedetomidine. 28.7% to 15.6% with frailty-directed rehabilitation. Four magnesium trials with mixed results", "Mostly small single-center trials with surrogate endpoints"],
    ]
    return dict(caption="Table 5. Evidence on perioperative brain injury as a second hit after tumor-related vulnerability.",
                header=["Evidence type", "Studies", "Quantitative range or finding", "Interpretation"],
                widths=[1.7, 1.5, 2.9, 2.2], rows=rows, landscape=False, fs=7.0,
                note="Ranges are the lowest and highest values reported by the cited studies and are not pooled estimates.")

def t6():
    rows = []
    for k in ("nayak2017", "angelita2026", "jammula2022", "bangun2018", "rambe2017", "wonggo2025"):
        lab, ctry, des, pop, aim, inst, fnd = NEW[k]
        rows.append([f"{lab} {{c:{k}}}", ctry, des, pop, inst, fnd])
    return dict(caption="Table 6. Instrument-focused stratum, studies of MoCA-INA, NANO-Ina, and their parent instruments.",
                header=["Study", "Country", "Design", "Population", "Instrument", "Main findings"],
                widths=[0.9, 1.0, 1.0, 1.55, 1.0, 3.05], rows=rows, landscape=False, fs=7.0,
                note="These six studies were reported separately from the core evidence base. Two included no patients with tumors and are included as evidence on the Indonesian MoCA. IQR, interquartile range. MDASI-BT, MD Anderson Symptom Inventory for brain tumor. RANO, Response Assessment in Neuro-Oncology.")

def t7():
    rows = [
        ["RQ1. How is frailty or brain frailty defined and measured?", "No brain-specific definition. Frailty is borrowed through seven general indices, in mixed tumor samples, with differing thresholds", "7 core studies", "Answered, and the answer is a gap"],
        ["RQ2. Which domains and instruments characterize it?", "Four domains map onto existing studies (systemic, cognitive, neurological, imaging). Each has several instruments and no shared standard", "7, 30, 16, and 32 core studies", "Answered descriptively"],
        ["RQ3. Is neuroinflammation present in benign as well as malignant tumors?", "Documented in glioma tissue, cerebrospinal fluid, and microdialysate. Benign tumor evidence rests on external reviews, and meningioma-only studies show injury and vulnerability but no cytokines", "3 glioma or mixed studies, 0 meningioma", "Partly answered"],
        ["RQ4. Which biomarkers can detect neuroinflammation and injury?", "S100B, NSE, GFAP, tau, and NfL track injury. Cytokines require tissue, cerebrospinal fluid, or microdialysis. No validated neuroinflammation panel", "12 injury and 7 inflammatory studies", "Partly answered"],
        ["RQ5. What supports perioperative brain injury as a second hit?", "New DWI lesions after 18.8% to 45.7% of resections, marker rise in 4 of 4 studies, delirium in 4.2% to 35%. Interaction with preoperative state untested", "Table 5", "Partly answered"],
        ["RQ6. Which instruments exist, including MoCA-INA and NANO-Ina?", "None of the core studies used either. Six supplementary studies document both, without perioperative testing", "0 core, 6 supplementary", "Answered, with a gap"],
        ["RQ7. Where are the gaps?", "No definition, no brain-specific index, no CT or muscle metric, no meningioma cytokine data, no interaction test, no perioperative validation of the Indonesian instruments", "All of the above", "Answered"],
    ]
    return dict(caption="Table 7. Answers to the seven review questions and the status of the mapped evidence.",
                header=["Question", "Answer from the mapped evidence", "Basis", "Status"],
                widths=[1.8, 3.6, 1.2, 1.1], rows=rows, landscape=False, fs=7.0,
                note="Status describes how fully the mapped evidence answers the question. Partly answered and gap findings are reported as results of a scoping review.")

def all_tables():
    return {"t1": t1(), "t2": t2(), "t3": t3(), "t4": t4(), "t5": t5(), "t6": t6(), "t7": t7()}
