import json, collections, statistics, sys
sys.path.insert(0, ".")
from data_core import *

cr = json.load(open("cr_all.json", encoding="utf-8"))

def year_of(no):
    m = cr.get("core%d" % no, {})
    if "special" in m:
        return {12: 2004, 13: 2006, 60: 2025}[no]
    for k in ("published-print", "published-online", "issued"):
        v = m.get(k, {}).get("date-parts")
        if v and v[0] and v[0][0]:
            y = v[0][0]
            break
    return y

YEAR = {no: year_of(no) for no in R}

YEAR.update({2: 2023, 6: 2022, 35: 2022, 37: 2020, 43: 2018, 44: 2023, 59: 2021, 65: 2025, 69: 2022, 54: 2011, 55: 2016})
MAINC = {no: R[no][1].split(",")[0] for no in R}

def tally(keyfn):
    c = collections.Counter(keyfn(no) for no in R)
    return dict(c.most_common())

S = {}
S["n_total"] = len(R)
S["design"] = tally(lambda n: R[n][2])
S["tumor"] = tally(lambda n: R[n][3])
S["stream"] = tally(lambda n: R[n][4])
S["country"] = tally(lambda n: MAINC[n])
S["n_countries"] = len(S["country"])
S["level"] = tally(lambda n: level(n))
S["year_min"], S["year_max"] = min(YEAR.values()), max(YEAR.values())
S["year_2018plus"] = sum(1 for n in R if YEAR[n] >= 2018)
S["year_2020plus"] = sum(1 for n in R if YEAR[n] >= 2020)
S["year_pre2005"] = sum(1 for n in R if YEAR[n] < 2005)
ns = [R[n][5] for n in R if R[n][5] is not None]
S["n_with_size"] = len(ns)
S["n_median"] = statistics.median(ns)
q = statistics.quantiles(ns, n=4)
S["n_q1"], S["n_q3"] = q[0], q[2]
S["n_min"], S["n_max"] = min(ns), max(ns)
flags = collections.Counter(f for n in R for f in R[n][9])
S["flags"] = dict(flags)
S["flag_members"] = {f: [n for n in R if f in R[n][9]] for f in "FCNIBMDHT"}
S["cog_class"] = {k: len(v) for k, v in COG_CLASS.items()}
S["cog_total"] = sum(S["cog_class"].values())
S["cog_dir"] = {k: len(v) for k, v in COG_DIR.items()}
S["tumor_members"] = {t: [n for n in R if R[n][3] == t] for t in ("Glioma", "Meningioma", "Mixed", "Metastasis")}
S["rct"] = [n for n in R if R[n][2] == "RCT"]
S["protocol"] = [n for n in R if R[n][2] == "Trial protocol"]
S["dwi"] = {n: "%d of %d (%.1f%%)" % (a, b, 100 * a / b) for n, (a, b) in DWI.items()}
json.dump({"S": S, "YEAR": YEAR}, open("stats.json", "w"), indent=1, default=str)
if __name__ == "__main__":
    for k, v in S.items():
        print(k, v)
    print("year by study", YEAR)

    assert sum(S["design"].values()) == 70 and sum(S["tumor"].values()) == 70 and sum(S["stream"].values()) == 70
    allcog = sorted(x for v in COG_CLASS.values() for x in v)
    assert allcog == sorted(S["flag_members"]["C"]), (allcog, sorted(S["flag_members"]["C"]))
    dirs = sorted(x for v in COG_DIR.values() for x in v)
    assert len(dirs) == len(set(dirs)) == 18, len(dirs)
    for t, ids in S["tumor_members"].items():
        print(t, len(ids))
    print("OK")
