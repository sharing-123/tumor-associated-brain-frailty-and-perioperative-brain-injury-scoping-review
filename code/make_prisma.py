import copy, os, subprocess, sys, zipfile
from lxml import etree

SRC = "../inputs/PRISMA_Scoping_Risetku.docx"
WORK = "_prisma"
OUT = "../outputs/JNA_submission/Figures"
os.makedirs(WORK, exist_ok=True)
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ns = {"w": W}

NEW = {
    12: "Team-supplied sources (n = 7)", 18: "Team-supplied sources (n = 7)",
    27: "Records identified from:", 37: "Records identified from:",
    28: "Databases (n = 2302)", 38: "Databases (n = 2302)",
    33: "Preprint server (n = 16)", 43: "Preprint server (n = 16)",
    34: "medRxiv (n = 16)", 44: "medRxiv (n = 16)",
    62: "Records excluded", 64: "Records excluded",
    76: "(n = 158)", 78: "(n = 158)",
    97: "(n = 145)", 99: "(n = 145)",
    101: "Wrong outcome (n = 29)", 105: "Wrong outcome (n = 29)",
    113: "Wrong outcome (n = 56)", 120: "Wrong outcome (n = 56)",
    114: "Wrong population (n = 80)", 121: "Wrong population (n = 80)",
    134: "(n = 76)", 138: "(n = 76)", 136: "(n = 76)", 140: "(n = 76)",
}
NEW[115] = "Wrong publication type (n = 27)"
NEW[122] = "Wrong publication type (n = 27)"
ADD_AFTER = {103: "Wrong publication type (n = 1)", 107: "Wrong publication type (n = 1)"}

def set_text(p, text):
    ts = p.xpath(".//w:t", namespaces=ns)
    ts[0].text = text
    ts[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    for t in ts[1:]:
        t.text = ""

zin = zipfile.ZipFile(SRC)
root = etree.fromstring(zin.read("word/document.xml"))
ps = root.xpath("//w:p", namespaces=ns)
for i, p in enumerate(ps):
    if i in NEW:
        set_text(p, NEW[i])
for i, text in ADD_AFTER.items():
    p = ps[i]
    q = copy.deepcopy(p)
    set_text(q, text)
    p.addnext(q)
docx = os.path.join(WORK, "prisma_76.docx")
zout = zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == "word/document.xml":
        data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    zout.writestr(item, data)
zout.close()
print(docx)
