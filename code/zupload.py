import os
import json, re, sys, uuid, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
BUILD = "."
KEY = os.environ["ZOTERO_API_KEY"]
UID = 14681764
refs = json.load(open(BUILD + "/refs_master.json", encoding="utf-8"))
order = json.load(open(BUILD + "/cite_order.json"))
COLL_NAME = "Scoping Review PBI 2026 - Tumor-Associated Brain Frailty"

def api(method, path, body=None, extra=None):
    h = {"Zotero-API-Key": KEY, "Content-Type": "application/json", "Zotero-API-Version": "3"}
    if extra:
        h.update(extra)
    req = urllib.request.Request("https://api.zotero.org/users/%d%s" % (UID, path), data=json.dumps(body).encode("utf-8") if body is not None else None, headers=h, method=method)
    return json.loads(urllib.request.urlopen(req, timeout=120).read().decode("utf-8"))

def lowercase_after_colon(t):
    return re.sub(r": ([A-Z])(?=[a-z ])", lambda m: ": " + m.group(1).lower(), t)

def item_json(k, coll):
    r = refs[k]
    cre = [{"creatorType": "author", "firstName": a["given"], "lastName": a["family"]} for a in r["authors"]]
    title = lowercase_after_colon(r["title"])
    extra = ("PMID: %s" % r["pmid"]) if r.get("pmid") else ""
    if k == "core60":
        return {"itemType": "preprint", "title": title, "creators": cre, "date": "2025", "repository": "arXiv", "archiveID": "arXiv:2507.23057", "DOI": r["doi"],
                "url": "https://arxiv.org/abs/2507.23057", "language": "en", "collections": [coll]}
    if k == "bangun2018":
        return {"itemType": "bookSection", "title": title, "creators": cre, "bookTitle": "Stem Cell Oncology", "publisher": "CRC Press", "place": "London", "date": "2018", "pages": "119-123",
                "DOI": r["doi"], "language": "en", "collections": [coll]}
    if k == "mckenzie2019":
        eds = [("Higgins", "Julian P T"), ("Thomas", "James"), ("Chandler", "Jacqueline"), ("Cumpston", "Miranda"), ("Li", "Tianjing"), ("Page", "Matthew J"), ("Welch", "Vivian A")]
        cre = cre + [{"creatorType": "editor", "firstName": g, "lastName": f} for f, g in eds]
        return {"itemType": "bookSection", "title": title, "creators": cre, "bookTitle": "Cochrane Handbook for Systematic Reviews of Interventions", "edition": "2nd ed", "publisher": "Wiley",
                "place": "Chichester", "date": "2019", "pages": "321-347", "DOI": r["doi"], "language": "en", "collections": [coll]}
    it = {"itemType": "journalArticle", "title": title, "creators": cre, "publicationTitle": r["journal"], "volume": r["volume"], "issue": r["issue"], "pages": r["pages"],
          "date": str(r["year"]), "journalAbbreviation": r["abbr"], "language": r.get("language", "en"), "DOI": r["doi"], "extra": extra, "collections": [coll]}
    return it

def main():
    coll = api("POST", "/collections", [{"name": COLL_NAME}], {"Zotero-Write-Token": uuid.uuid4().hex})
    ck = coll["successful"]["0"]["key"]
    print("collection", ck)
    keys = {}
    for i in range(0, len(order), 40):
        batch = order[i:i + 40]
        res = api("POST", "/items", [item_json(k, ck) for k in batch], {"Zotero-Write-Token": uuid.uuid4().hex})
        if res.get("failed"):
            print("FAILED", res["failed"])
        for idx, v in res["successful"].items():
            keys[batch[int(idx)]] = v["key"]
        print("batch", i, len(res["successful"]))
    json.dump({"collection": ck, "keys": keys}, open(BUILD + "/zkeys.json", "w"), indent=1)
    print("uploaded", len(keys), "of", len(order))

if __name__ == "__main__":
    if "--dry" in sys.argv:
        for k in order[:3] + ["core60", "bangun2018", "mckenzie2019"]:
            print(json.dumps(item_json(k, "XXXX"), ensure_ascii=False)[:400])
    else:
        main()
