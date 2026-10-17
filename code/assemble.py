import re, json, sys
sys.path.insert(0, ".")
import content_a as A
import content_b as B
import content_c as C
import tables as T

TOKEN = re.compile(r"\{c:([^}]+)\}")

def rk(k):
    k = k.strip()
    return "core" + k[1:] if re.fullmatch(r"s\d+", k) else k

def doc_blocks():
    D = []
    D.append(("title", A.TITLE))
    D.append(("authors", A.AUTHORS))
    D.append(("abstract", A.ABSTRACT))
    D.append(("keywords", A.KEYWORDS))
    D.append(("h1", "1. Introduction"))
    for p in A.INTRO:
        D.append(("p", p))
    D.append(("h1", "2. Materials and Methods"))
    M = A.METHODS
    for h, body in (("h_design", "design"), ("h_q", "q"), ("h_elig", "elig"), ("h_src", "src"), ("h_sel", "sel"), ("h_chart", "chart"), ("h_syn", "syn"), ("h_env", "env")):
        D.append(("h2", M[h]))
        for p in M[body]:
            D.append(("p", p))
    D.extend(B.results())
    D.extend(C.DISCUSSION)
    D.extend(C.BACK)
    return D

def cite_order(D, tables):
    order = []
    seen = set()

    def scan(text):
        for m in TOKEN.finditer(text):
            for k in m.group(1).split(","):
                k = rk(k)
                if k not in seen:
                    seen.add(k)
                    order.append(k)

    for kind, payload in D:
        if kind in ("p", "h1", "h2"):
            scan(payload)
        elif kind == "table":
            t = tables[payload]
            for row in t["rows"]:
                if row[0] == "__GROUP__":
                    continue
                for cell in row:
                    scan(cell)
    return order

if __name__ == "__main__":
    D = doc_blocks()
    tables = T.all_tables()
    order = cite_order(D, tables)
    json.dump(order, open("cite_order.json", "w"), indent=1)
    refs = json.load(open("refs_master.json", encoding="utf-8"))
    miss = [k for k in order if k not in refs]
    print("cited", len(order), "missing", miss)
    unused = [k for k in refs if k not in order]
    print("unused", unused)
