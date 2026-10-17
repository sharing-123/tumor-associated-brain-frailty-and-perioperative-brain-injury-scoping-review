import json, re, html, sys
sys.path.insert(0, ".")
from refs_def import CORE, NEW, BG

cr = json.load(open("cr_all.json", encoding="utf-8"))

ABBR = {
 "Journal of Neuro-Oncology": "J Neurooncol", "Acta Neurochirurgica": "Acta Neurochir (Wien)", "Neurosurgery": "Neurosurgery",
 "Neuro-Oncology Advances": "Neurooncol Adv", "Surgery": "Surgery", "Neurosurgical Review": "Neurosurg Rev",
 "Journal of Neurosurgical Anesthesiology": "J Neurosurg Anesthesiol", "BMC Cancer": "BMC Cancer", "Journal of Neurosurgery": "J Neurosurg",
 "NeuroImage: Clinical": "Neuroimage Clin", "Critical Care": "Crit Care", "Journal of Clinical Neuroscience": "J Clin Neurosci",
 "World Neurosurgery": "World Neurosurg", "Clinical Neurology and Neurosurgery": "Clin Neurol Neurosurg", "Cytokine": "Cytokine",
 "Clinical Chemistry": "Clin Chem", "Scientific Reports": "Sci Rep", "Cancers": "Cancers (Basel)", "Minerva Anestesiologica": "Minerva Anestesiol",
 "The Surgeon": "Surgeon", "British Journal of Neurosurgery": "Br J Neurosurg", "Neurology India": "Neurol India", "PLOS ONE": "PLoS One", "PLOS One": "PLoS One",
 "BMC Anesthesiology": "BMC Anesthesiol", "Anesthesiology": "Anesthesiology", "Journal of Neuroanaesthesiology and Critical Care": "J Neuroanaesth Crit Care",
 "Indian Journal of Anaesthesia": "Indian J Anaesth", "British Journal of Anaesthesia": "Br J Anaesth", "Chinese Journal of Integrative Medicine": "Chin J Integr Med",
 "Saudi Journal of Anaesthesia": "Saudi J Anaesth", "Egyptian Journal of Anaesthesia": "Egypt J Anaesth", "Behavioural Neurology": "Behav Neurol",
 "European Journal of Neuroscience": "Eur J Neurosci", "Neurosurgical Focus": "Neurosurg Focus", "Journal of Clinical Medicine": "J Clin Med", "Medicine": "Medicine (Baltimore)",
 "Scientific Programming": "Sci Program", "Asia-Pacific Journal of Oncology Nursing": "Asia Pac J Oncol Nurs", "Drug Design, Development and Therapy": "Drug Des Devel Ther",
 "Neuro-Oncology Practice": "Neurooncol Pract", "Neuro-Oncology": "Neuro Oncol", "Asian Pacific Journal of Cancer Prevention": "Asian Pac J Cancer Prev",
 "Open Access Macedonian Journal of Medical Sciences": "Open Access Maced J Med Sci", "Medical Scope Journal": "Med Scope J",
 "The Journals of Gerontology Series A: Biological Sciences and Medical Sciences": "J Gerontol A Biol Sci Med Sci", "The Lancet": "Lancet",
 "Canadian Medical Association Journal": "CMAJ", "The Journal of nutrition, health and aging": "J Nutr Health Aging", "Neurology": "Neurology",
 "The Lancet Neurology": "Lancet Neurol", "Cancer Cell": "Cancer Cell", "Nature Neuroscience": "Nat Neurosci", "Anesthesia &amp; Analgesia": "Anesth Analg",
 "Anesthesia & Analgesia": "Anesth Analg", "Frontiers in Psychiatry": "Front Psychiatry", "EBioMedicine": "EBioMedicine", "Nature Reviews Neurology": "Nat Rev Neurol",
 "Glia": "Glia", "Frontiers in Neurology": "Front Neurol", "Annals of Internal Medicine": "Ann Intern Med", "JBI Evidence Synthesis": "JBI Evid Synth",
 "International Journal of Social Research Methodology": "Int J Soc Res Methodol", "Implementation Science": "Implement Sci",
 "BMC Medical Research Methodology": "BMC Med Res Methodol", "BMJ": "BMJ", "Systematic Reviews": "Syst Rev", "Journal of the American Geriatrics Society": "J Am Geriatr Soc",
 "Supportive Care in Cancer": "Support Care Cancer", "Brain, Behavior, and Immunity": "Brain Behav Immun", "Surgical Neurology": "Surg Neurol",
 "AJNR. American journal of neuroradiology": "AJNR Am J Neuroradiol",
}
KEEP = {"Indonesian", "Montreal", "Karnofsky", "Parkinson", "Hopkins", "Oxford", "I.A.N.A./I.A.G.G.", "(I.A.N.A./I.A.G.G.)", "Cochrane", "American", "European", "Asian", "African"}
SMALL = set("a an and as at but by for from in nor of on or per the to vs versus via with".split())

def clean(t):
    t = html.unescape(t or "")
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\s+", " ", t).strip().rstrip(".")
    return t

def is_title_case(t):
    ws = [w for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", t) if w.lower() not in SMALL and len(w) > 3]
    if len(ws) < 3:
        return False
    cap = sum(1 for w in ws if w[0].isupper())
    return cap / len(ws) >= 0.7

def _prot(seg):
    return bool(re.search(r"[A-Z].*[A-Z]|\d", seg)) or seg in KEEP or (seg.isupper() and len(seg) > 1)

def sentence_case(t):
    out = []
    first = True
    for w in t.split(" "):
        if not w:
            continue
        segs = w.split("-")
        res = []
        for i, sg in enumerate(segs):
            m = re.match(r"^([^A-Za-z0-9]*)(.*?)([^A-Za-z0-9]*)$", sg)
            pre, core, post = m.groups()
            if first and i == 0:
                core = core[:1].upper() + core[1:]
            elif _prot(core) or core in KEEP:
                pass
            else:
                core = core.lower()
            res.append(pre + core + post)
        out.append("-".join(res))
        first = False
    return " ".join(out)

def fix_name(n):
    if n and n.isupper() and len(n) > 2:
        return n[0] + n[1:].lower()
    if n and n.upper().startswith("DE ") and n[:3] == n[:3].upper():
        return n[:1] + n[1:].lower()
    return n

def initials(given):
    parts = re.split(r"[\s\-]+", (given or "").replace(".", " ").strip())
    return "".join(p[0].upper() for p in parts if p)

def year_of(m, key):
    for k in ("published-print", "issued", "published-online"):
        v = (m.get(k) or {}).get("date-parts")
        if v and v[0] and v[0][0]:
            return v[0][0]

OVERRIDE = {

 "core39": dict(pages="45-57", issue="1-2"),
 "appleton2020": dict(pages="e439-e452"),
 "core47": dict(volume="9", issue="3"),
 "core56": dict(pages="7941689"),
 "core66": dict(pages="7717075"),
 "core69": dict(volume="16"),
 "core2": dict(year=2023), "core6": dict(year=2022), "core35": dict(year=2022), "core37": dict(year=2020), "core43": dict(year=2018),
 "core44": dict(year=2023), "core59": dict(year=2021), "core65": dict(year=2025), "core54": dict(year=2011), "core55": dict(year=2016),
 "core36": dict(year=2019), "core62": dict(year=2018), "core28": dict(year=2005),
 "safavynia2019": dict(year=2019), "wonggo2025": dict(year=2025, language="en"), "hambardzumyan2016": dict(year=2016),
 "core10": dict(), "page2021": dict(volume="372"), "campbell2020": dict(volume="368"),
 "core14": dict(issue=""), "core5": dict(), "ostrom2023": dict(issue="Suppl 4", volume="25"),
}
PMIDS = {"core12": "15140713", "core13": "16484420", "appleton2020": "31882527", "core39": "40035733", "nayak2017": "28453751", "angelita2026": "41793672",
         "jammula2022": "36124322", "rambe2017": "29362618", "huq2022": "35843574", "qureshi2023": "37624530", "haslund2022": "34716512", "domingues2016": "26216710"}

MANUAL = {
 "core12": dict(type="article-journal", authors=[("Law", "Meng"), ("Yang", "Stanley"), ("Babb", "James S"), ("Knopp", "Edmond A"), ("Golfinos", "John G"), ("Zagzag", "David"), ("Johnson", "Glyn")],
                title="Comparison of cerebral blood volume and vascular permeability from dynamic susceptibility contrast-enhanced perfusion MR imaging with glioma grade",
                journal="AJNR American journal of neuroradiology", abbr="AJNR Am J Neuroradiol", year=2004, volume="25", issue="5", pages="746-755", doi=""),
 "core13": dict(type="article-journal", authors=[("Cha", "S"), ("Yang", "L"), ("Johnson", "G"), ("Lai", "A"), ("Chen", "M-H"), ("Tihan", "T"), ("Wendland", "M"), ("Dillon", "W P")],
                title="Comparison of microvascular permeability measurements, K(trans), determined with conventional steady-state T1-weighted and first-pass T2*-weighted MR imaging methods in gliomas and meningiomas",
                journal="AJNR American journal of neuroradiology", abbr="AJNR Am J Neuroradiol", year=2006, volume="27", issue="2", pages="409-417", doi=""),
 "core60": dict(type="preprint", authors=[("Tran", "Triet M"), ("Khanmohammadi", "Sina")],
                title="Presurgical neural energy landscapes predict postoperative working memory outcome after brain tumor resection",
                journal="arXiv", abbr="arXiv", year=2025, volume="", issue="", pages="", doi="10.48550/arXiv.2507.23057", archive="arXiv:2507.23057"),
}

TITLE_OVERRIDE = {
 "core6": "Brain infarction following meningioma surgery-incidence, risk factors, and impact on function, seizure risk, and patient-reported quality of life",
 "core31": "The incidence and predictors of postoperative delirium after brain tumor resection in adults: a cross-sectional survey",
 "core32": "Use of diffusion weighted MRI in predicting early postoperative outcome of new neurological deficits after brain tumor resection",
 "rambe2017": "Correlation between the Montreal Cognitive Assessment-Indonesian Version (MoCA-INA) and the Mini-Mental State Examination (MMSE) in elderly",
 "wonggo2025": "Cognitive function MoCA-INA scale of anaesthesiology and intensive therapy residents: a comparison of before and after on-call duty",
 "angelita2026": "Translation and validation of the Neurologic Assessment in Neuro-Oncology scale into Indonesian (NANO-Ina)",
 "nayak2017": "The Neurologic Assessment in Neuro-Oncology (NANO) scale: a tool to assess neurologic function for integration into the Response Assessment in Neuro-Oncology (RANO) criteria",
 "jammula2022": "The Montreal Cognitive Assessment (MoCA) in neuro-oncology: a pilot study of feasibility and utility in telehealth and in-person clinical assessments",
 "nasreddine2005": "The Montreal Cognitive Assessment, MoCA: a brief screening tool for mild cognitive impairment",
 "ostrom2023": "CBTRUS statistical report: primary brain and other central nervous system tumors diagnosed in the United States in 2016-2020",
 "evered2018": "Recommendations for the nomenclature of cognitive change associated with anaesthesia and surgery-2018",
 "bangun2018": "The difference of MMSE and MoCA-Ina scores in brain tumors",
}

def build():
    out = {}
    for key, m in cr.items():
        o = OVERRIDE.get(key, {})
        if key in MANUAL:
            r = dict(MANUAL[key]); r["key"] = key
            r["authors"] = [dict(family=a[0], given=a[1], ini=initials(a[1])) for a in r["authors"]]
            r["pmid"] = PMIDS.get(key, "")
            out[key] = r
            continue
        ctype = m.get("type")
        au = m.get("author") or []
        authors = []
        for a in au:
            fam = fix_name(a.get("family") or a.get("name") or "")
            giv = a.get("given") or ""
            if giv.isupper() and len(giv) > 3:
                giv = giv.title()
            authors.append(dict(family=fam, given=giv, ini=initials(giv)))
        title = clean((m.get("title") or [""])[0])
        if is_title_case(title):
            title = sentence_case(title)
        title = TITLE_OVERRIDE.get(key, title).replace("—", "-").replace("–", "-")
        title = re.sub(r": ([A-Z])([a-z]*)", lambda mm: ": " + mm.group(1).lower() + mm.group(2), title)
        title = title.replace("Serum s-100B", "Serum S-100B")
        cont = html.unescape((m.get("container-title") or [""])[0])
        r = dict(key=key, type="book-chapter" if ctype in ("book-chapter", "other") else "article-journal", authors=authors, title=title, journal=cont,
                 abbr=ABBR.get(cont, ""), year=o.get("year", year_of(m, key)), volume=o.get("volume", (m.get("volume") or "").lstrip("0") or ""),
                 issue=o.get("issue", m.get("issue") or ""), pages=o.get("pages", m.get("page") or m.get("article-number") or ""), doi=m.get("DOI", ""), pmid=PMIDS.get(key, ""),
                 language="en")
        out[key] = r
    return out

if __name__ == "__main__":
    refs = build()
    missing = [k for k, r in refs.items() if r["type"] == "article-journal" and not r["abbr"]]
    print("missing abbr:", [(k, refs[k]["journal"]) for k in missing])
    json.dump(refs, open("refs_master.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for k, r in refs.items():
        print(k, "|", r["title"][:110], "|", r["year"], r["volume"], r["issue"], r["pages"], "|", r["abbr"])
