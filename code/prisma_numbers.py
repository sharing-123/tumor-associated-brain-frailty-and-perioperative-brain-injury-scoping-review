P = dict(
    pubmed=692, scopus=1436, proquest=102, cochrane=72, medrxiv=16,
    gscholar=117, citation=34, client=7,
    dups=987,

    r_outcome_db=48 + 8, r_pop_db=79 + 1, r_pub_db=27, r_design_db=31, r_int_db=21,
    nr_db=17,

    r_outcome_ot=28 + 1, r_pop_ot=57, r_design_ot=19, r_pub_ot=1,
    nr_ot=13,
)
P["db_only"] = P["pubmed"] + P["scopus"] + P["proquest"] + P["cochrane"]
P["db_total"] = P["db_only"] + P["medrxiv"]
P["screened"] = P["db_total"] - P["dups"]
P["ta_excl"] = 1062
P["sought_db"] = P["screened"] - P["ta_excl"]
P["assessed_db"] = P["sought_db"] - P["nr_db"]
P["excl_db"] = P["r_outcome_db"] + P["r_pop_db"] + P["r_pub_db"] + P["r_design_db"] + P["r_int_db"]
P["inc_db"] = P["assessed_db"] - P["excl_db"]
P["other_total"] = P["gscholar"] + P["citation"] + P["client"]
P["sought_ot"] = P["other_total"]
P["assessed_ot"] = P["sought_ot"] - P["nr_ot"]
P["excl_ot"] = P["r_outcome_ot"] + P["r_pop_ot"] + P["r_design_ot"] + P["r_pub_ot"]
P["inc_ot"] = P["assessed_ot"] - P["excl_ot"]
P["inc_total"] = P["inc_db"] + P["inc_ot"]
P["instr"] = 6
P["core"] = P["inc_total"] - P["instr"]
P["all_records"] = P["db_total"] + P["other_total"]
assert P["db_only"] == 2302 and P["db_total"] == 2318 and P["screened"] == 1331
assert P["sought_db"] == 269 and P["assessed_db"] == 252 and P["excl_db"] == 215 and P["inc_db"] == 37
assert P["other_total"] == 158 and P["assessed_ot"] == 145 and P["excl_ot"] == 106 and P["inc_ot"] == 39
assert P["inc_total"] == 76 and P["core"] == 70
if __name__ == "__main__":
    for k, v in P.items():
        print(k, v)
