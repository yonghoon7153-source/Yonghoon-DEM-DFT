"""Check the WSL operator's fixed scanner output. Only structural counts leave this reader."""
import json

B7 = "34eb74142884489505590501840ccc6423a014a508989c82f135020146283ad3"
LOGS = ("log.liggghts", "log.txt")
NAMES = {"lhs00_%03d" % n for n in range(100, 130)}
COUNTS = ("b7_matches", "pressure_prefix_malformed", "read_restart_echo_lines",
          "reading_restart_message_lines", "bytes")
SCANNER_SHA = "2305bd2194b29ac5439008906a17b1c673968a59fd52dcdde35b03ff4da20634"


def check(condition):
    if not condition:
        raise ValueError("WSL30 structural contract")


def strict_object(pairs):
    obj = dict(pairs)
    check(len(obj) == len(pairs))
    return obj


def natural(value):
    return type(value) is int and value >= 0


def validate(raw, rc):
    check(rc == 0 and len(raw) <= 65536)
    data = json.loads(raw, object_pairs_hook=strict_object)
    check(set(data) == {"schema", "mode", "rc", "status", "expected_cases", "counted_cases",
                        "b7_source_sha256", "roots", "cases"})
    check(data["schema"] == "lhs_pressure_inventory/v1" and data["mode"] == "wsl")
    check(type(data["rc"]) is int and data["rc"] == 0 and data["status"] == "INVENTORY_COMPLETE")
    check(data["roots"] == {"local": "COUNTED"} and data["b7_source_sha256"] == B7)
    rows = data["cases"]
    check(type(rows) is list and data["expected_cases"] == data["counted_cases"] == len(rows) == 30)
    check({r["case"] for r in rows} == NAMES)
    for row in rows:
        check(set(row) == {"case", "root", "status", "logs", "case_out", "root_out", "logs_with_b7_matches"})
        check(row["root"] == "local" and row["status"] == "COUNTED" and set(row["logs"]) == set(LOGS))
        for name in LOGS:
            rec = row["logs"][name]
            check(set(rec) == set(COUNTS) | {"status"} and rec["status"] == "COUNTED")
            check(all(natural(rec[key]) for key in COUNTS))
        for key in ("case_out", "root_out"):
            out = row[key]
            check(set(out) == {"status", "regular_files"} and out["status"] in ("COUNTED", "ABSENT"))
            check(natural(out["regular_files"]) and (out["status"] == "COUNTED" or out["regular_files"] == 0))
        check(natural(row["logs_with_b7_matches"]) and row["logs_with_b7_matches"] ==
              sum(row["logs"][name]["b7_matches"] > 0 for name in LOGS))
    return data


def observation(inventory):
    logs = [row["logs"] for row in inventory["cases"]]
    return {"cases": len(logs), "logs": len(logs) * len(LOGS),
            "pairs_with_b7_in_both": sum(min(pair[name]["b7_matches"] for name in LOGS) > 0 for pair in logs),
            "pairs_with_equal_b7_row_counts": sum(p[LOGS[0]]["b7_matches"] == p[LOGS[1]]["b7_matches"] for p in logs),
            "pairs_with_different_file_sizes": sum(p[LOGS[0]]["bytes"] != p[LOGS[1]]["bytes"] for p in logs)}
