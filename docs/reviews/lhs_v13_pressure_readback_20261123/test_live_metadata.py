import copy
import json
from pathlib import Path
import runpy
import unittest

from unittest.mock import patch


D = runpy.run_path(str(Path(__file__).with_name("check_live_metadata.py")))


def valid():
    row = {"root": "local", "status": "COUNTED", "logs_with_b7_matches": 2,
           "case_out": {"status": "ABSENT", "regular_files": 0},
           "root_out": {"status": "ABSENT", "regular_files": 0}}
    counts = dict.fromkeys(D["COUNTS"], 0)
    counts.update(status="COUNTED", b7_matches=3, bytes=85)
    row["logs"] = {key: dict(counts) for key in D["LOGS"]}
    rows = [dict(copy.deepcopy(row), case=n) for n in sorted(D["NAMES"])]
    return {"schema": "lhs_pressure_inventory/v1", "mode": "wsl", "rc": 0,
            "status": "INVENTORY_COMPLETE", "expected_cases": 30, "counted_cases": 30,
            "b7_source_sha256": D["B7"], "roots": {"local": "COUNTED"}, "cases": rows}


def validate(data, rc=0):
    return D["validate"](json.dumps(data).encode(), rc)


class Live(unittest.TestCase):
    def test_divergent_counts_preserved_without_qualification(self):
        data = valid()
        data["cases"][0]["logs"]["log.txt"]["b7_matches"] = 4
        data["cases"][1]["logs"]["log.txt"]["bytes"] = 125
        with patch("builtins.open", side_effect=AssertionError("study data")):
            derived = D["observation"](validate(data))
        self.assertEqual(derived, {"cases": 30, "logs": 60, "pairs_with_b7_in_both": 30,
                                   "pairs_with_equal_b7_row_counts": 29, "pairs_with_different_file_sizes": 1})

    def test_no_matches_is_valid_inventory(self):
        data = valid()
        for item in data["cases"][0]["logs"].values():
            item["b7_matches"] = 0
        data["cases"][0]["logs_with_b7_matches"] = 0
        self.assertEqual(D["observation"](validate(data))["pairs_with_b7_in_both"], 29)

    def test_reject_new_field_or_string_payload(self):
        for field, value in [("pressure_mpa", "VALUE_CANARY"), ("bytes", "VALUE_CANARY"),
                             ("b7_matches", True), ("pressure_prefix_malformed", -1)]:
            data = valid()
            data["cases"][0]["logs"]["log.txt"][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "^WSL30 structural contract$"):
                validate(data)

    def test_reject_extra_scope_absence_and_partial_even_if_rc_zero(self):
        for change in ["foreign", "missing", "duplicate", "symlink", "outside", "mismatch"]:
            data = valid()
            if change == "foreign":
                data["mode"] = "ibb"
            elif change == "missing":
                data["cases"].pop()
            elif change == "duplicate":
                data["cases"][1]["case"] = "lhs00_100"
            elif change == "symlink":
                data["cases"][0]["logs"]["log.txt"] = {"status": "SYMLINK"}
            elif change == "outside":
                data["cases"][0]["case"] = "lhs00_030"
            else:
                data["cases"][0]["logs_with_b7_matches"] = 1
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate(data)

    def test_scanner_rc_and_json_frame(self):
        data = valid()
        with self.assertRaises(ValueError):
            validate(data, 2)
        for raw in [b'{"mode":"wsl","mode":"ibb"}', b'{}\n{}', b'\xff', b' ' * 65537]:
            with self.assertRaises(ValueError):
                D["validate"](raw, 0)


if __name__ == "__main__":
    unittest.main()
