import re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
import assemble as AS
import content_a as A
import tables as T

D = AS.doc_blocks()
TOK = AS.TOKEN

def plain(t):
    return TOK.sub("", t).replace("  ", " ")

texts = []
for kind, payload in D:
    if kind == "authors":
        continue
    if kind in ("p", "h1", "h2", "h1b", "title", "keywords"):
        texts.append((kind, plain(payload)))
    elif kind == "abstract":
        for lab, tx in payload:
            texts.append(("abstract", lab + " " + tx))
for key, t in T.all_tables().items():
    for row in t["rows"]:
        if row[0] == "__GROUP__":
            continue
        for c in row:
            texts.append(("cell", plain(c)))
    texts.append(("note", t["note"]))

BAD_CHARS = {"em dash": "\u2014", "en dash": "\u2013", "double hyphen": "--", "semicolon": ";", "colon": ":"}
issues = []
for kind, tx in texts:
    for name, ch in BAD_CHARS.items():
        if ch in tx:
            if name == "colon" and kind in ("title", "abstract") and False:
                continue
            issues.append((name, kind, tx[:90]))
print("char issues", len(issues))
for i in issues[:60]:
    print(i)

WORDS = ["delve", "underscore", "intricate", "tapestry", "testament", "landscape", "pivotal", "showcase", "foster", "leverage", "realm", "seamless", "novel", "groundbreaking", "paramount", "crucial", "comprehensive", "robust", "notably", "importantly", "moreover", "furthermore", "additionally", "it is worth noting", "in order to", "plays a", "sheds light", "paves the way", "highlighting", "multifaceted", "holistic", "cutting-edge", "vital", "key role", "myriad", "ever-evolving", "navigate"]
body = " ".join(tx for k, tx in texts if k not in ("cell", "note")).lower()
for w in WORDS:
    c = body.count(w)
    if c:
        print("word", w, c)

abs_words = sum(len(tx.split()) for k, tx in texts if k == "abstract")
print("abstract words", abs_words)
main_words = sum(len(tx.split()) for k, tx in texts if k in ("p", "h1", "h2"))
print("main text words", main_words)

long = []
for kind, tx in texts:
    if kind == "p":
        for s in re.split(r"(?<=[.?!])\s+(?=[A-Z])", tx):
            n = len(s.split())
            if n > 38:
                long.append((n, s[:120]))
print("long sentences (>38 words)", len(long))
for n, s in sorted(long, reverse=True)[:25]:
    print(n, s)

starts = {}
for kind, tx in texts:
    if kind == "p":
        for s in re.split(r"(?<=[.?!])\s+(?=[A-Z])", tx):
            w = s.split()[:2]
            if len(w) == 2:
                starts[" ".join(w)] = starts.get(" ".join(w), 0) + 1
rep = sorted(((v, k) for k, v in starts.items() if v >= 5), reverse=True)
print("repeated openers", rep[:15])
