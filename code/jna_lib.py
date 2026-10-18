import re, json, random, string, sys
from xml.sax.saxutils import escape
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Pt
from docx.oxml import parse_xml
from docx.oxml.ns import qn
import content_jna as J

BUILD = "."
UID = 14681764
FONT = "Times New Roman"
REFS = json.load(open(BUILD + "/refs_master.json", encoding="utf-8"))
ZK = json.load(open(BUILD + "/zkeys.json"))["keys"]
CITE = re.compile(r"\{c:([^}]+)\}")
SDCTOK = re.compile(r"\{sdc:(\d+)\}")
HL = re.compile(r"\{hl:([^}]+)\}")
W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
random.seed(20261018)

def rk(k):
    k = k.strip()
    return "core" + k[1:] if re.fullmatch(r"s\d+", k) else k

def rid(n=8):
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

def esc(s):
    return escape(s, {'"': "&quot;"})

def keys_in(text):
    out = []
    for m in CITE.finditer(text):
        for k in m.group(1).split(","):
            out.append(rk(k))
    return out

def order_of(texts):
    order = []
    for t in texts:
        for k in keys_in(t):
            if k not in order:
                order.append(k)
    return order

def lower_after_colon(t):
    return re.sub(r": ([A-Z])(?=[a-z ])", lambda m: ": " + m.group(1).lower(), t)

def ref_text(k):
    r = REFS[k]
    au = ["%s %s" % (a["family"], a["ini"]) for a in r["authors"]]
    authors = ", ".join(au[:3]) + (", et al." if len(au) > 3 else ".")
    title = lower_after_colon(r["title"]).rstrip(".")
    t = title if title[-1] in "?!" else title + "."
    if k == "bangun2018":
        return "%s %s In: Stem Cell Oncology. CRC Press, 2018. DOI: %s" % (authors, t, r["doi"])
    if k == "mckenzie2019":
        return "%s %s In: Higgins JPT, Thomas J, Chandler J, Cumpston M, Li T, Page MJ, Welch VA, eds. Cochrane Handbook for Systematic Reviews of Interventions. 2nd ed. Wiley, 2019. DOI: %s" % (authors, t, r["doi"])
    s = "%s %s %s. %s" % (authors, t, r["abbr"], r["year"])
    loc = ""
    if r["volume"]:
        loc += r["volume"]
    if r["pages"]:
        loc += ":" + r["pages"]
    if loc:
        s += ";" + loc
    s += "."
    if r["doi"]:
        s += " DOI: " + r["doi"]
    return s

def csl_item(k, num):
    r = REFS[k]
    d = {"id": num}
    if k in ("bangun2018", "mckenzie2019"):
        d.update({"type": "chapter", "title": r["title"], "container-title": "Stem Cell Oncology" if k == "bangun2018" else "Cochrane Handbook for Systematic Reviews of Interventions",
                  "publisher": "CRC Press" if k == "bangun2018" else "Wiley", "page": r["pages"], "DOI": r["doi"]})
    else:
        d.update({"type": "article-journal", "title": r["title"], "container-title": r["journal"], "container-title-short": r["abbr"], "journalAbbreviation": r["abbr"]})
        for fld, key in (("volume", "volume"), ("issue", "issue"), ("page", "pages"), ("DOI", "doi")):
            if r[key]:
                d[fld] = r[key]
        if r.get("pmid"):
            d["PMID"] = r["pmid"]
    d["issued"] = {"date-parts": [[int(r["year"])]]}
    d["language"] = "en"
    d["author"] = [{"family": a["family"], "given": a["given"]} for a in r["authors"]]
    return {"id": num, "uris": ["http://zotero.org/users/%d/items/%s" % (UID, ZK[k])], "itemData": d}

def collapse(nums):
    nums = sorted(set(nums))
    out = []
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        if j - i >= 2:
            out.append("%d-%d" % (nums[i], nums[j]))
        else:
            out.extend(str(x) for x in nums[i:j + 1])
        i = j + 1
    return ",".join(out)

def fld_runs(instr, result_xml):
    return ('<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r><w:instrText xml:space="preserve"> %s </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>%s'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r>') % (instr, result_xml)

def add_xml(par, xml):
    for el in parse_xml("<w:p %s>%s</w:p>" % (W_NS, xml)):
        par._p.append(el)

def add_text(par, text, size=None, bold=False, italic=False):
    r = par.add_run(text)
    r.font.name = FONT
    r._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    if size:
        r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    return r

class Ctx:
    def __init__(self, order, live):
        self.order = order
        self.cnum = {k: i + 1 for i, k in enumerate(order)}
        self.live = live

    def cite_xml(self, keylist, size):
        keys = [rk(k) for k in keylist.split(",")]
        nums = [self.cnum[k] for k in keys]
        shown = collapse(nums)
        rpr = '<w:sz w:val="%d"/>' % int(size * 2) if size else ""
        res = '<w:r><w:rPr><w:rFonts w:ascii="%s" w:hAnsi="%s"/><w:vertAlign w:val="superscript"/>%s</w:rPr><w:t>%s</w:t></w:r>' % (FONT, FONT, rpr, esc(shown))
        if not self.live:
            return res
        props = {"unsorted": False, "formattedCitation": "\\super %s\\nosupersub{}" % shown, "plainCitation": shown, "noteIndex": 0}
        cj = {"citationID": rid(8), "properties": props, "citationItems": [csl_item(k, self.cnum[k]) for k in sorted(keys, key=lambda x: self.cnum[x])],
              "schema": "https://github.com/citation-style-language/schema/raw/master/csl-citation.json"}
        instr = "ADDIN ZOTERO_ITEM CSL_CITATION " + esc(json.dumps(cj, ensure_ascii=False, separators=(",", ":")))
        return fld_runs(instr, res)

    def fill(self, par, text, size=None):
        text = SDCTOK.sub(lambda m: J.sdc(int(m.group(1))), text)
        for idx, piece in enumerate(HL.split(text)):
            if idx % 2 == 1:
                add_text(par, piece, size).font.highlight_color = WD_COLOR_INDEX.YELLOW
            elif piece:
                self._fill_cites(par, piece, size)

    def _fill_cites(self, par, text, size):
        pos = 0
        for m in CITE.finditer(text):
            seg = text[pos:m.start()].rstrip(" ")
            if seg:
                add_text(par, seg, size)
            add_xml(par, self.cite_xml(m.group(1), size))
            pos = m.end()
        tail = text[pos:]
        if tail:
            add_text(par, tail, size)
