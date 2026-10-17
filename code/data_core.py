STREAMS = {
 "S1": "Tumor biology, microenvironment, and blood-brain barrier",
 "S2": "Systemic frailty indices and perioperative risk",
 "S3": "Cognitive trajectories after tumor surgery",
 "S4": "Postoperative delirium and agitation",
 "S5": "Perioperative brain injury, imaging, and biomarkers",
 "S6": "Perioperative interventions and neuroprotective strategies",
}
DESIGN_LEVEL = {
 "RCT": "2", "Prospective cohort": "2", "Secondary analysis of RCT": "3", "Retrospective cohort": "3",
 "Registry cohort": "3", "Case-control": "4", "Cross-sectional study": "4", "Case series": "4", "Non-randomized pilot trial": "4",
 "Mechanistic laboratory study": "5", "Trial protocol": "NG",
}

R = {
1: ("Portnow, 2014","USA","Prospective cohort","Mixed","S1",10,"Primary or metastatic brain tumors; n = 10 with dialysate","Craniotomy with peritumoral microdialysis","Most cytokines peaked within 8 h after surgery and fell over 96 h (11 of 17 with significant decline). Intracerebral levels exceeded serum levels. No temsirolimus effect.","MT"),
2: ("de Sain, 2023","Netherlands","Prospective cohort","Glioma","S3",37,"Diffuse glioma; n = 37","Awake surgery with electrostimulation","Cognition stable overall. Inhibition reaction time slowed early (p = .004) and improved later (p = .017). Mean extent of resection 83.6%.","CI"),
3: ("Noll, 2021","USA","Prospective cohort","Glioma","S3",15,"Left perisylvian glioma; n = 15","Awake craniotomy with language mapping","87% declined (z <= -1.00) on at least one cognitive measure within 12 weeks. Connectomic changes correlated with cognitive change (rho -0.51 to -0.78).","CI"),
4: ("Grossman, 2025","USA","Non-randomized pilot trial","Glioma","S1",7,"Low-grade glioma; n = 7","Regadenoson dose escalation, no resection","Blood-brain barrier endpoint (Ktrans > 0.04 min-1) not met at any dose. T1 subtraction signal in normal-appearing white matter rose 74.0% (p = .0163). Trial closed early.","IT"),
5: ("Wang, 2021","China","Retrospective cohort","Mixed","S2",659,"Intracranial tumors; n = 659","Elective craniotomy under general anesthesia","Delirium 18.8% overall, and 12.8%, 27.0%, 37.5% in non-frail, pre-frail, frail groups (mFI). Frailty independently associated with delirium (adjusted OR 1.7, p = .032).","FD"),
6: ("Strand, 2022 (meningioma)","Norway","Prospective cohort","Meningioma","S5",327,"Meningioma WHO 1 to 3; 327 operations","Resection","DWI infarction in 34.9% (114 of 327). Permanent deficit in 6.7%, 72.7% of them with infarction (p < .001). Age predicted infarction (OR 1.03 per year).","IN"),
7: ("Strand, 2021 (glioma)","Norway","Prospective cohort","Glioma","S5",539,"Diffuse glioma; 539 operations","Resection or reoperation","DWI infarction in 44.2% (238 of 539), related to tumor volume (r = .267), bleeding (r = .176), and age (r = .193). Rates differed between surgeons (32% to 72%).","I"),
8: ("Sharma, 2010","India, USA","Prospective cohort","Mixed","S5",35,"Supratentorial tumors; n = 35","Resection under isoflurane and nitrous oxide","Autoregulation impaired before surgery in 7 of 35 (20%) and stayed impaired in all 7 afterward. Larger tumor and midline shift > 5 mm were risk factors. CO2 reactivity unchanged.","H"),
9: ("Kemmerer, 2021","Germany","Case-control","Glioma","S1",18,"High-grade glioma; n = 18, controls n = 14","Resection, tissue and CSF before adjuvant therapy","CD68+ macrophages (19% to 27%) outnumbered CD45+ leukocytes (3% to 7%). CSF IL-7 was lower in glioblastoma (p = .009). CD68+ infiltration correlated negatively with several cytokines (p < .01).","MT"),
10: ("Michaelsson, 2023","Sweden","Prospective cohort","Glioma","S5",34,"Glioma; n = 34","Resection","Plasma GFAP, tau, and NfL rose on days 1 and 3 (p < .001). NfL had a second peak at day 10 (p = .028). Day 1 GFAP and NfL were higher with new deficits (p = .048, p = .043).","BIN"),
11: ("Satoer, 2012","Netherlands","Prospective cohort","Glioma","S3",28,"Glioma near eloquent areas; n = 28","Resection","Impairment before and after surgery in language, memory, and executive domains. Postoperative decline in language (p = .027) and executive function (p = .022) at 3 to 4 months.","CI"),
12: ("Law, 2004","USA","Retrospective cohort","Glioma","S1",73,"Primary glioma; n = 73","Preoperative imaging, biopsy alone in 16","rCBV tracked tumor grade (Spearman r = .817). Ktrans separated only grade I from grades II and III (p = .027).","IT"),
13: ("Cha, 2006","USA","Prospective cohort","Mixed","S1",27,"Glioma n = 20, meningioma n = 7","Preoperative dynamic contrast MRI before resection","Ktrans from two methods separated grade IV from lower grades. The two methods agreed in gliomas (r = .95) but not in meningiomas (r = .16).","IT"),
14: ("van Dellen, 2013","Netherlands","Prospective cohort","Glioma","S3",10,"Low-grade glioma; n = 10","Resection","No group-level cognitive change. Default mode connectivity gain correlated with verbal memory (tau = .571, p = .048) and frontoparietal gain with attention (tau = .857, p = .003).","CI"),
15: ("Einav, 2006","Israel","Prospective cohort","Meningioma","S5",52,"Supratentorial meningioma; n = 52","Resection","S100B rose from 0.065 to 0.155 ug/L by 48 h (p < .0001), higher with bleeding and midline shift. MMSE deterioration correlated with S100B at all times (p = .005, .011, .036).","BCI"),
16: ("Sastry, 2020","USA","Registry cohort","Mixed","S2",20333,"Intracranial tumors; n = 20,333","Elective craniotomy (ACS NSQIP)","Low and medium-to-high mFI-5 raised odds of major complication (OR 1.41, 1.61) and 30-day mortality (OR 1.87, 2.42), all p < .001.","FN"),
17: ("Harland, 2020","USA","Prospective cohort","Mixed","S2",260,"Brain tumors; n = 260","Elective craniotomy","Frailty raised odds of non-home discharge (OR 10.36, 95% CI 3.6 to 30.1) and of any complication (OR 2.09). Slow walking speed was the most predictive item.","FN"),
18: ("Lang, 2017","Canada","Prospective cohort","Glioma","S3",16,"Diffuse glioma; n = 16","Resection, mostly with cortical mapping","Frontoparietal connectivity correlated inversely with preoperative composite cognition (p = .024). Non-tumor parietal connectivity predicted one-month change (p = .009).","CI"),
19: ("Satoer, 2014","Netherlands","Prospective cohort","Glioma","S3",45,"Glioma in eloquent areas; n = 45","Resection","Permanent decline only in category fluency (p = .030). Letter fluency and naming improved between 3 months and 1 year. Trail making normalized by 1 year.","CI"),
20: ("Schei, 2022","Norway","Prospective cohort","Glioma","S3",182,"Diffuse glioma; n = 182","Primary resection","High-grade glioma cognitive score rose from 70.9 to 85.1 at 1 month (p < .001). Low-grade glioma stayed near 80 to 81. Steroid use and tumor volume predicted improvement.","CI"),
21: ("Gempt, 2013 (MEP)","Germany","Prospective cohort","Glioma","S5",70,"Glioma in motor eloquent areas; n = 70","Resection with MEP monitoring","Ischemic lesions in 46% (32 of 70), present in 76% with MEP decline > 50% versus 33% without. Permanent motor deficit in 14%.","IN"),
22: ("Gempt, 2013 (recurrence)","Germany","Prospective cohort","Glioma","S5",100,"Glioma; n = 100 (109 operations)","Resection","New ischemic lesions in 31% of newly diagnosed and 80% of recurrent tumors (p < .01). New deficits were more frequent with lesions (p < .05).","IN"),
23: ("Baumgarten, 2018","Germany","Prospective cohort","Mixed","S5",32,"Glioma n = 25, metastasis n = 7","Resection","Serum GFAP rose after surgery in glioblastoma (p = .0172) and peaked on day 1. Baseline GFAP was higher in glioma than metastasis (0.18 vs 0.08 ug/L). No link with residual tumor.","BI"),
24: ("Bommakanti, 2016","India","Prospective cohort","Meningioma","S3",57,"Supratentorial meningioma; n = 57","Resection","73.7% impaired on at least one test before surgery. Raised intracranial pressure was linked to impairment (95.2% vs 61.1%, p = .005). Improvement at 3 months, no deterioration.","CI"),
25: ("Huq, 2021","USA","Retrospective cohort","Mixed","S2",1692,"Brain tumors; n = 1,692","Primary surgery","Each mFI-5 point added 0.32 ICU days and 1.38 hospital days (p = .007, p < .001) and predicted sepsis (OR 2.12) and respiratory failure (OR 1.55).","F"),
26: ("Tucha, 2003","Germany","Prospective cohort","Meningioma","S3",54,"Frontal meningioma; n = 54, controls n = 54","Total removal","Patients were impaired against controls in several attentional and executive functions before surgery. No domain deteriorated, and attention improved at 4 to 9 months.","CI"),
27: ("Piperi, 2011","Greece","Retrospective cohort","Glioma","S1",97,"Astrocytoma grade II to IV; n = 97","Resection, archival tissue","IL-8 and IL-6 expression rose with grade and necrosis (p < .05). IL-8 correlated with VEGF (r = .475) and independently predicted survival (p = .043).","MT"),
28: ("Stranjalis, 2005","Greece","Prospective cohort","Meningioma","S5",50,"Meningioma; n = 50","Resection","S100B above 0.4 ug/L carried a 9-fold risk of neurologic deterioration (95% CI 2.4 to 34) and an 11-fold risk of poor 6-month outcome. Early deterioration occurred in 50%.","BNI"),
29: ("Stewart, 1987","Canada","Mechanistic laboratory study","Glioma","S1",13,"Glial tumors; n = 13","Lobectomy specimens, electron microscopy","Peritumoral vessels had longer junctional clefts and more endothelial vesicles than normal vessels (p < .02 to .03), a structural barrier defect.","T"),
30: ("Hoffermann, 2017","Austria","Retrospective cohort","Mixed","S3",196,"Mixed intracranial tumors; n = 196","Craniotomy","No decline in any of eight computerized subtests at 3 to 4 months. Go/noGo (p = .003) and figural memory (p < .001) improved. Meningioma overall score rose from 93 to 98 (p = .001).","C"),
31: ("Chen, 2020","China","Cross-sectional study","Mixed","S4",893,"Mixed brain tumors; n = 893","Craniotomy","Delirium 14.78%. Independent predictors were restraint, age over 50, longer operation, electrolyte disturbance, and tobacco use. Meningioma was protective (AUC 0.787).","D"),
32: ("Khan, 2006","USA","Prospective cohort","Mixed","S5",80,"Mixed tumors, mainly glioma and metastasis; n = 80","Resection","Positive postoperative DWI in 19%. A new DWI lesion was the only multivariable predictor of incomplete recovery at day 7 and day 30 (both p = .005). New deficit in 30%.","IN"),
33: ("Machein, 1999","Germany","Mechanistic laboratory study","Mixed","S1",14,"Glial tumors n = 11, lymphoma n = 3","Stereotactic biopsy","VEGF mRNA correlated with capillary permeability (r = 0.667, p = .015) and plasma vascular volume (r = 0.778, p = .0017) in glial tumors.","MIT"),
34: ("Zangrossi, 2022","Italy","Retrospective cohort","Glioma","S3",47,"Glioma; n = 47","Awake surgery","85% of test scores were stable or improved at one week. Presurgical cognition was the strongest predictor of early outcome (leave-one-out r = 0.57).","CI"),
35: ("Barberis, 2022","France","Case series","Glioma","S3",18,"Right frontal IDH-mutant glioma; 20 cases in 18 patients","Awake mapping","Severe early deficits in executive function (75%) and attention (65%). Group scores stable at 4 months, but 45% of cases declined in at least one domain.","CI"),
36: ("Barzilai, 2019","Israel","Retrospective cohort","Glioma","S3",49,"Low-grade glioma; n = 49","Craniotomy, awake mapping in most","Memory (p < .001) and executive function (p = .031) improved at mean 6.06 months. No link with IDH1 status or extent of resection.","C"),
37: ("Capo, 2020","Italy","Retrospective cohort","Glioma","S3",40,"Recurrent glioma; n = 40","Awake repeat surgery","No significant change in normal-range counts after the second surgery except a small decline in oral praxis. Repeat surgery was feasible at 4 months.","C"),
38: ("Fu, 2024","USA","Registry cohort","Mixed","S4",28340,"Brain tumors; n = 28,340","Craniotomy (National Inpatient Sample)","Delirium 4.79% by ICD codes, with 4 days longer stay, higher mortality (2.36% vs 1.28%), and more frequent three or more comorbidities.","FD"),
39: ("Gracia, 2025","Spain","RCT","Mixed","S6",51,"Resective neurosurgery n = 51, tumor subgroup n = 35","Magnesium sulfate versus saline","Primary S100B at 2 h did not differ. At 6 months the cavity was smaller (10.0 vs 26.9 cm3, p = .02) and gliosis less frequent in the tumor subgroup (43.8% vs 85.7%, p = .02).","BCIN"),
40: ("Gu, 2022","China","Retrospective cohort","Mixed","S4",618,"Mixed brain tumors; n = 618","Craniotomy with ICU admission","Emergence delirium 21.2%, mostly hypoactive. Later postoperative delirium occurred in 58.8% with and 4.7% without emergence delirium.","D"),
41: ("Hernandez-Palazon, 2018","Spain","RCT","Mixed","S6",60,"Supratentorial tumors; n = 60","Hypertonic saline 3 versus 5 mL/kg","Brain relaxation score was identical (2.0 vs 2.0, p = .535). Both doses gave equal sustained rises in osmolality, with similar complications.","H"),
42: ("Ravindranath, 2025","India","Trial protocol","Glioma","S6",None,"Supratentorial glioma; planned n = 90","Propofol TIVA versus sevoflurane","No outcome data. Plans NSE, IL-6, CAM-ICU, MoCA, and Glasgow Outcome Scale.","BMCD"),
43: ("Huang, 2018","China","Prospective cohort","Mixed","S4",400,"Mixed brain tumors; n = 400","Craniotomy with ICU admission","Agitation 13.0%. Independent risks were bi-frontal pneumocephalus (OR 4.4) and delayed extubation. Agitation predicted poor mRS (OR 5.4).","DI"),
44: ("Jiang, 2023","China","RCT","Mixed","S6",110,"Supratentorial tumors; n = 110","Desflurane versus propofol TIVA","Satisfactory brain relaxation was similar (69% vs 73%). Desflurane gave better cognitive recovery at 15 min (16 vs 0, p = .003) but more nausea and tachycardia.","CH"),
45: ("Favre, 1995","Switzerland","RCT","Mixed","S6",24,"Cerebral tumors; n = 24","Clonidine versus placebo","No effect on intracranial pressure. Clonidine lowered mean arterial and cerebral perfusion pressure, with 8 of 12 patients below 60 mmHg versus 2 of 12.","H"),
46: ("Guy, 1997","USA","RCT","Mixed","S6",63,"Supratentorial lesions; n = 63","Remifentanil versus fentanyl","Intraoperative ICP and brain relaxation were similar. Neurologic examinations were broadly similar through day 7.","HN"),
47: ("Jitsinthunun, 2022","Thailand","RCT","Meningioma","S6",76,"Supratentorial meningioma; n = 76","Magnesium sulfate versus saline","Blood loss 500 vs 510 mL. Postoperative MoCA did not differ (underpowered). No magnesium toxicity.","C"),
48: ("Sriganesh, 2023","India","Trial protocol","Mixed","S6",None,"Supratentorial tumors; planned n = 500","Fentanyl versus dexmedetomidine","No outcome data. Emergence delirium and quality of recovery are secondary outcomes.","D"),
49: ("Li, 2023","China","RCT","Mixed","S6",260,"Frontotemporal tumors; n = 260","Dexmedetomidine versus placebo","Delirium 22% versus 46% (RR 0.51, p < .001) with higher day 5 MMSE. Gliomas were about twice as likely to develop delirium.","DC"),
50: ("Lu, 2010","China","RCT","Mixed","S6",32,"Mixed brain tumors; n = 32","Electroacupuncture preconditioning versus none","S100B (1.16 vs 1.47 ug/L) and NSE (24.7 vs 31.4 ug/L) were lower at end of surgery (p < .05).","B"),
51: ("Mahajan, 2019","India","RCT","Mixed","S6",41,"Supratentorial tumors; n = 41","Magnesium, lignocaine, or saline","S100B was lower at 24 h with magnesium than with either other arm. Pain and fentanyl use were lower with magnesium and lignocaine.","B"),
52: ("Meskal, 2015","Netherlands","Prospective cohort","Meningioma","S3",68,"Meningioma; n = 68","Resection","69% impaired in at least one domain before surgery and 44% at 3 months. Five of seven domains improved.","C"),
53: ("Mirrahimi, 2015","Iran","RCT","Mixed","S6",60,"Supratentorial tumors; n = 60","Magnesium versus placebo","Postoperative S100B rose less with magnesium. NSE and Barthel index did not differ between arms.","BN"),
54: ("Mousa, 2011","Egypt","RCT","Mixed","S6",60,"Supratentorial tumors; n = 60","Crystalloid, colloid, or blood","Colloid kept jugular venous oxygen saturation and flow-metabolism coupling higher than crystalloid.","H"),
55: ("Peng, 2016","China","RCT","Mixed","S6",80,"Supratentorial tumors; n = 80","Lidocaine versus saline","Cognitive decline at 6 months did not differ (about 10% in each arm), although lidocaine lowered cerebral oxygen extraction.","CH"),
56: ("Niki, 2020","Japan","Prospective cohort","Glioma","S3",54,"Glioma; n = 54","Resection with intraoperative MRI","Lesion-symptom mapping tied separate cognitive components to left temporoparietal and right frontal regions. MMSE-J stayed normal and missed these deficits.","CI"),
57: ("Schouwenaars, 2024","Netherlands","Prospective cohort","Meningioma","S3",23,"Meningioma; n = 23","Resection","Scores were below norms on three tests before and after surgery, with no improvement at 3 months. Network activity during the 2-back task was unchanged.","CI"),
58: ("Skandalakis, 2023","USA","Registry cohort","Metastasis","S2",11038,"Brain metastases; n = 11,038","Resection (ACS NSQIP)","Thirty-day mortality rose from 1.3% (robust) to 12.6% (severely frail) by Risk Analysis Index, which outperformed mFI-5 and age (C-statistic 0.65).","F"),
59: ("Stalnacke, 2021","Sweden","Case series","Glioma","S3",7,"Suspected low-grade glioma; n = 7","Awake resection of face motor cortex","Verbal processing speed declined, with no change in fluency, memory, or working memory. Six of seven had mild facial dysfunction.","CN"),
60: ("Tran, 2025","USA","Retrospective cohort","Mixed","S3",20,"Glioma n = 7, meningioma n = 13","Resection (public dataset, preprint)","Preoperative high-order resting-state features predicted the 6-month working memory group (accuracy 90%, AUC 0.95). Not peer reviewed.","CI"),
61: ("Tan, 2025","China","RCT","Meningioma","S6",78,"Meningioma; n = 78","Ciprofol versus propofol","S100B and NSE at 24 h were higher with ciprofol. Induction hypotension was less frequent with ciprofol (59% vs 95%).","BH"),
62: ("Budenas, 2018","Lithuania","Prospective cohort","Mixed","S4",522,"Mixed brain tumors; n = 522","Cranial surgery","Delirium 4.2%. Predictors were age 65 or older, low education, poor function, and low hemoglobin. Delirium predicted unfavorable discharge outcome (OR 5.3). Histology was not associated.","DMN"),
63: ("van Nieuwenhuizen, 2018","Netherlands","Case-control","Meningioma","S3",20,"WHO grade I meningioma n = 20, controls n = 20","Resection, assessed at mean 1.7 years","Working memory was lower than in controls and linked to lower theta-band default mode connectivity.","CI"),
64: ("Wu, 2017","Taiwan","RCT","Mixed","S6",80,"Supratentorial tumors; n = 80","Goal-directed fluids, SVV threshold 10% versus 18%","New neurologic events were fewer with low SVV (17.5% vs 40%), with smaller NSE and GFAP rises. S100B did not differ.","BHN"),
65: ("Wu, 2025","China","Secondary analysis of RCT","Mixed","S4",240,"Frontotemporal tumors; n = 240","Craniotomy, intraoperative hypotension","Delirium 35%. Mean arterial pressure below 65 mmHg was not associated with delirium. Glioma, age, and hypertension raised risk. Higher MMSE and dexmedetomidine were protective.","DHC"),
66: ("Wu, 2022","China","RCT","Mixed","S6",80,"Intracerebral tumors; n = 80","Dexmedetomidine versus saline","S100B, NSE, GFAP, IL-6, and TNF-alpha were lower and CCSE and MoCA higher at day 1. Differences converged by day 3.","BMCI"),
67: ("Yuan, 2023","China","RCT","Mixed","S6",291,"Mixed brain tumors; n = 291","Frailty-originated early rehabilitation versus usual care","Delirium 15.6% versus 28.7%. Frailty at discharge 19.9% versus 30.7%.","FDN"),
68: ("Zarino, 2021","Italy","Prospective cohort","Glioma","S3",35,"Insular glioma; n = 35","Resection with mapping","Language fell after surgery and partly recovered by 3 months. Aphasic symptoms in 92% of left-sided patients early and 44% at 3 months.","CN"),
69: ("Zhao, 2022","China","RCT","Mixed","S6",60,"Supratentorial tumors; n = 60","Lidocaine versus saline","QoR-40 was higher on days 1 and 2. S100B, NSE, IL-6, and TNF-alpha were lower at end of surgery.","BM"),
70: ("Zigiotto, 2026","Italy","Retrospective cohort","Glioma","S3",64,"Glioma; n = 64","Awake versus asleep surgery","Attention declined at 1 week and recovered by 1 month. Awake surgery was the only clinical predictor of decline. Default mode network lesions were linked to worse scores.","CI"),
}

COG_CLASS = {
 "Multidomain battery": [3,11,14,19,24,26,34,35,36,37,39,56,59,63],
 "Domain-specific tests": [2,60,68,70],
 "Brief screener": [15,42,44,47,49,55,65,66],
 "Computerized battery": [18,30,52,57],
 "Patient-reported cognition": [20],
}

COG_DIR = {
 "Improved or improved/stable": [20,24,26,30,36,52],
 "No change or persistent deficit": [14,37,57],
 "Stable at group level, individual decline": [35],
 "Decline (selective or global)": [3,11,59],
 "Transient decline with recovery": [2,68,70],
 "Early decline, single early timepoint": [34],
 "Selective persistent decline with partial recovery": [19],
}
BASELINE_COG_IMPAIRED = [11,19,24,26,30,35,52,57]
FRAILTY_TOOLS = {"mFI-11":[5],"mFI-5":[16,25,58],"Hopkins Frailty Score":[17],"Risk Analysis Index":[58],"Fried phenotype":[67],"Comorbidity count (proxy)":[38]}
NEURO_TOOLS = {"Binary new deficit on examination":[6,10,17,22,32,46,64,68],"KPS":[32,42,62],"NIHSS":[32],"mRS":[40,43,62],"GOS or GOSE":[28,39,42,62],"GCS":[40,43,48],"Barthel index":[53,62,63,64,67],"House-Brackmann":[59],"Intraoperative MEP":[21,59]}
IMG_MODS = {
 "Diffusion-weighted MRI for ischemic lesions":[6,7,10,21,22,32],
 "Volumetric MRI for extent of resection or tumor volume":[2,11,14,18,19,20,23,24,26,34,35,56,70],
 "Perfusion or permeability imaging":[4,12,13,33],
 "Functional connectivity (fMRI or MEG)":[3,14,18,57,60,63,70],
 "CT-based findings":[8,15,24,28,33,43,46],
 "Contrast-enhanced ultrasound":[66],
}
BIOMARK = {
 "S100B":[15,28,39,50,51,53,61,64,66,69],
 "NSE":[39,42,50,53,61,64,66,69],
 "GFAP":[10,23,64,66],
 "Tau":[10],
 "NfL":[10],
 "IL-6":[1,27,42,62,66,69],
 "IL-8":[1,27],
 "TNF-alpha":[66,69],
 "VEGF":[1,27,33],
 "Tissue or CSF immune cell markers (CD45, CD68, CD163)":[9],
}

DELIRIUM = {5:"18.8%",31:"14.78%",38:"4.79%",40:"21.2% (emergence)",43:"13.0% (agitation)",62:"4.2%",65:"35%",49:"22% to 46% by arm",67:"15.6% to 28.7% by arm"}
HISTOLOGY_DELIRIUM_POS = [5,31,40,49,65]
HISTOLOGY_DELIRIUM_NULL = [62]
DWI = {6:(114,327),7:(238,539),21:(32,70),32:(15,80)}

NEW = {
 "nayak2017": ("Nayak, 2017","Multinational","Multicenter reliability study","Brain tumor (RANO setting)","Instrument development","NANO scale, 9 neurologic domains, clinician-rated","Inter-observer agreement above 90% (kappa 0.35 to 0.83), median administration time 4 min (IQR 3 to 5)."),
 "angelita2026": ("Angelita, 2026","Indonesia","Cross-sectional validation","Brain tumors n = 30 (glioblastoma 7, meningioma 7, metastasis 9, other 7)","Translation and validation","NANO-Ina","Weighted kappa 0.629 (sensation) to 0.935 (facial strength) across reported domains. Most patients (77%) were untreated at assessment, and the work came from a single center."),
 "jammula2022": ("Jammula, 2022","USA","Cross-sectional feasibility study","Primary CNS tumors n = 71 (47 in person, 24 telehealth)","MoCA in clinic and telehealth","MoCA, abnormal at 25 or lower","Median 27 (range 6 to 30), 32% abnormal. Lower MoCA tracked KPS (r = 0.35), age (r = 0.27), and MDASI-BT cognitive burden (r = -0.27). Providers found it feasible."),
 "bangun2018": ("Bangun, 2018","Indonesia","Cross-sectional study","Brain tumors at diagnosis, n = 33","MMSE and MoCA-Ina side by side","MoCA-Ina, MMSE","Mean MoCA-Ina 21.79 (SD 4.93), MMSE 23.76 (SD 4.08). Abnormal scores clustered at 7 to 9 years of education. Attention and calculation impaired in 90.9% (MMSE) and delayed recall in 90.9% (MoCA-Ina)."),
 "rambe2017": ("Rambe, 2017","Indonesia","Cross-sectional study","Elderly adults (65 years or older), n = 83, no tumor","MoCA-INA versus MMSE","MoCA-INA, MMSE","MoCA-INA mean 21.06 (SD 4.56) against MMSE 24.96 (SD 3.38), Pearson r = 0.71. MoCA-INA below 26 in 85.5%."),
 "wonggo2025": ("Wonggo, 2025","Indonesia","Cross-sectional before-after study","Anesthesiology residents, n = 31, no tumor","MoCA-INA before and 24 h after on-call duty","MoCA-INA","Mean score fell from 26.84 to 25.00 (Wilcoxon Z = -3.778, p < .001), mainly in visuospatial, attention, and memory domains."),
}
LEVEL_NOTE = "Evidence level was assigned from study design alone (OCEBM 2011 prognosis and treatment tables) and is not a judgment of study quality."

def level(no):
    d = R[no][2]
    return DESIGN_LEVEL[d]
