#!/usr/bin/env python3
"""Synthetic decision-contract regressions; no experimental/DEM observations."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).with_name("mixer_d3_candidates.py")
spec = importlib.util.spec_from_file_location("mixer_d3_candidates", MODULE_PATH)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fixture():
    """All values/labels/seeds below are synthetic software-test inputs."""
    artifacts = {"conditions.txt": b"SYNTHETIC condition definition\n",
                 "observations.txt": b"SYNTHETIC source observations\n"}
    contract = {
        "schema": "mixer_d3_decision_contract/1",
        "analysis_id": "synthetic-test",
        "condition_sha256": sha(artifacts["conditions.txt"]),
        "grid": [{"id": "b1", "bo": 1}, {"id": "b2", "bo": 2}],
        "calibration": {t: {"unit": "synthetic-unit", "boundary": "inclusive",
                             "widths": {"b1": 0.5, "b2": 0.5}}
                        for t in ("T1", "T2")},
        "validation": {
            "v1": {"kind": "scalar", "unit": "synthetic-unit",
                   "boundary": "inclusive", "widths": {"b1": 0.5, "b2": 0.5}},
            "v2": {"kind": "categorical", "unit": "synthetic-state",
                   "rule": "exact-match", "labels": ["flow", "stopped"]}},
        "seed_policy": {"allowed_role_overlap": []},
    }
    def point(value, unit="synthetic-unit", categorical=False):
        result = {"state": "eligible", "value": value, "unit": unit,
                  "source_ids": ["raw"]}
        if not categorical:
            result["uncertainty"] = {"value": 0.1, "unit": unit, "n": 2,
                                     "df": 1, "method": "synthetic supplied uncertainty"}
        return result
    observations = {
        "schema": "mixer_d3_observations/1",
        "contract_sha256": "a" * 64,
        "condition_artifact": "conditions",
        "artifacts": [
            {"id": "conditions", "path": "conditions.txt", "sha256": sha(artifacts["conditions.txt"])},
            {"id": "raw", "path": "observations.txt", "sha256": sha(artifacts["observations.txt"])}],
        "calibration": {t: {"experiment": point(10),
                             "predictions": {"b1": point(10), "b2": point(10)}}
                        for t in ("T1", "T2")},
        "validation": {
            "v1": {"experiment": point(10), "predictions": {"b1": point(10), "b2": point(10)}},
            "v2": {"experiment": point("flow", "synthetic-state", True),
                   "predictions": {b: point("flow", "synthetic-state", True) for b in ("b1", "b2")}}},
        "seed_manifest": {"C0": [101], "C1": [103], "C2": [107]},
    }
    return contract, observations, artifacts


class DecisionTests(unittest.TestCase):
    def run_case(self, contract=None, observations=None, artifacts=None):
        c, o, a = fixture()
        return reader.evaluate(contract if contract is not None else c,
                               observations if observations is not None else o,
                               contract_sha256="a" * 64,
                               artifact_loader=(artifacts if artifacts is not None else a).__getitem__)

    def test_all_compatible(self):
        out = self.run_case()
        self.assertEqual(out["S"], ["b1", "b2"])
        self.assertEqual(out["S_T1"], out["S_T2"])
        self.assertEqual(out["validation"]["aggregate"], "all-compatible")
        self.assertTrue(out["calibration_complete"])
        self.assertFalse(out["execution_ready"])
        self.assertEqual(out["seed_check"]["status"], "CHECKED_SUPPLIED_MANIFEST")

    def test_calibration_states_exhaustive_81(self):
        states = ("compatible", "incompatible", "unassessed")
        for combination in itertools.product(states, repeat=4):
            c, o, _ = fixture()
            accepted = {"T1": [], "T2": []}
            for (test, bid), state in zip(itertools.product(("T1", "T2"), ("b1", "b2")), combination):
                row = o["calibration"][test]["predictions"][bid]
                if state == "compatible":
                    accepted[test].append(bid)
                elif state == "incompatible":
                    row["value"] = 20
                else:
                    del o["calibration"][test]["predictions"][bid]
            with self.subTest(combination=combination):
                out = self.run_case(c, o)
                self.assertEqual(out["S_T1"], accepted["T1"])
                self.assertEqual(out["S_T2"], accepted["T2"])
                self.assertEqual(out["S"], [b for b in ("b1", "b2") if b in accepted["T1"] and b in accepted["T2"]])
                self.assertEqual(out["calibration_complete"], "unassessed" not in combination)

    def test_validation_states_exhaustive_81_preserves_S(self):
        states = ("compatible", "incompatible", "unassessed")
        totals = {}
        for combination in itertools.product(states, repeat=4):
            c, o, _ = fixture()
            for (bid, test), state in zip(itertools.product(("b1", "b2"), ("v1", "v2")), combination):
                row = o["validation"][test]["predictions"][bid]
                if state == "incompatible":
                    row["value"] = 20 if test == "v1" else "stopped"
                elif state == "unassessed":
                    del o["validation"][test]["predictions"][bid]
            out = self.run_case(c, o)
            expected_candidates = []
            for pair in (combination[:2], combination[2:]):
                expected_candidates.append("unassessed" if "unassessed" in pair else
                                           "incompatible" if "incompatible" in pair else "compatible")
            expected = ("incomplete" if "unassessed" in expected_candidates else
                        "all-compatible" if all(x == "compatible" for x in expected_candidates) else
                        "none-compatible" if all(x == "incompatible" for x in expected_candidates) else "mixed")
            with self.subTest(combination=combination):
                self.assertEqual(out["S"], ["b1", "b2"])
                self.assertEqual(out["validation"]["aggregate"], expected)
                self.assertEqual([x["status"] for x in out["validation"]["candidates"]], expected_candidates)
            totals[expected] = totals.get(expected, 0) + 1
        self.assertEqual(totals, {"all-compatible": 1, "mixed": 6, "incomplete": 65, "none-compatible": 9})

    def test_known_incompatibility_not_erased_by_unassessed_summary(self):
        c, o, _ = fixture()
        o["validation"]["v1"]["predictions"]["b1"]["value"] = 20
        del o["validation"]["v2"]["predictions"]["b1"]
        out = self.run_case(c, o)
        b = out["validation"]["candidates"][0]
        self.assertEqual(b["status"], "unassessed")
        self.assertEqual(b["items"]["v1"]["status"], "incompatible")

    def test_empty_grid_result_not_validation_success(self):
        for test in ("T1", "T2"):
            c, o, _ = fixture()
            for row in o["calibration"][test]["predictions"].values():
                row["value"] = 20
            out = self.run_case(c, o)
            self.assertEqual(out["S"], [])
            self.assertEqual(out["empty_case"], test + "-empty")
            self.assertEqual(out["validation"]["aggregate"], "not-applicable")

    def test_disjoint_individually_nonempty(self):
        c, o, _ = fixture()
        o["calibration"]["T1"]["predictions"]["b2"]["value"] = 20
        o["calibration"]["T2"]["predictions"]["b1"]["value"] = 20
        out = self.run_case(c, o)
        self.assertEqual(out["empty_case"], "disjoint")
        self.assertEqual(out["S"], [])
        self.assertIn("finite-grid-only", out["limitations"])

    def test_missing_experiment_and_uncertainty_are_unassessed(self):
        for change in ("experiment", "uncertainty", "value", "source_ids"):
            c, o, _ = fixture()
            if change == "experiment":
                del o["calibration"]["T1"][change]
            else:
                del o["calibration"]["T1"]["predictions"]["b1"][change]
            out = self.run_case(c, o)
            self.assertFalse(out["calibration_complete"])
            self.assertEqual(out["calibration"]["T1"][0]["status"], "UNASSESSED")

    def test_failure_reasons_preserved(self):
        for state in ("technical-failure", "observable-undefined", "unsupported-contract", "missing"):
            c, o, _ = fixture()
            o["calibration"]["T1"]["predictions"]["b1"] = {"state": state, "reason": "synthetic cause"}
            row = self.run_case(c, o)["calibration"]["T1"][0]
            self.assertEqual(row["status"], "UNASSESSED")
            self.assertIn(state, row["reason"])

    def test_flat_valid_response_keeps_candidates_without_identifiability_claim(self):
        c, o, _ = fixture()
        for row in o["calibration"]["T1"]["predictions"].values():
            row["flags"] = ["INSENSITIVE"]
        out = self.run_case(c, o)
        self.assertEqual(out["S"], ["b1", "b2"])
        self.assertEqual(out["calibration"]["T1"][0]["prediction"]["flags"], ["INSENSITIVE"])
        self.assertIn("no-identifiability-claim", out["limitations"])

    def test_boundary_is_exact_inclusive_decimal(self):
        c, o, _ = fixture()
        c["calibration"]["T1"]["widths"]["b1"] = 0.1
        o["calibration"]["T1"]["experiment"]["value"] = 0.4
        o["calibration"]["T1"]["predictions"]["b1"]["value"] = 0.3
        self.assertEqual(self.run_case(c, o)["calibration"]["T1"][0]["status"], "COMPATIBLE")

    def test_groups_respect_registered_topology_and_unknown_gap(self):
        c, o, _ = fixture()
        c["grid"].insert(1, {"id": "gap", "bo": 1.5})
        for rules in (c["calibration"], c["validation"]):
            for rule in rules.values():
                if "widths" in rule:
                    rule["widths"]["gap"] = 0.5
        out = self.run_case(c, o)
        self.assertEqual(out["neighbor_groups"], [["b1"], ["b2"]])
        self.assertTrue(out["range_limited"])
        self.assertNotIn("center", out)

    def test_no_input_mutation(self):
        c, o, _ = fixture()
        before = copy.deepcopy((c, o))
        self.run_case(c, o)
        self.assertEqual((c, o), before)

    def test_bounded_decision_cells(self):
        c, o, _ = fixture()
        c["grid"] = [{"id": "b" + str(n), "bo": n} for n in range(1, 1001)]
        c["validation"] = {"v" + str(n): copy.deepcopy(c["validation"]["v1"]) for n in range(64)}
        with self.assertRaisesRegex(reader.ContractError, "decision-cell limit"):
            self.run_case(c, o)

    def test_numeric_rejections(self):
        for value in (True, False, "1", "١", float("nan"), float("inf"), float("-inf")):
            for location in ("bo", "width", "value", "uncertainty"):
                c, o, _ = fixture()
                if location == "bo": c["grid"][0]["bo"] = value
                elif location == "width": c["calibration"]["T1"]["widths"]["b1"] = value
                elif location == "value": o["calibration"]["T1"]["experiment"]["value"] = value
                else: o["calibration"]["T1"]["experiment"]["uncertainty"]["value"] = value
                with self.subTest(value=value, location=location), self.assertRaises(reader.ContractError):
                    self.run_case(c, o)

    def test_invalid_grid_and_rules(self):
        changes = [lambda c: c.update(grid=[]),
                   lambda c: c["grid"].reverse(),
                   lambda c: c["grid"][1].update(id="b1"),
                   lambda c: c["grid"][1].update(bo=1),
                   lambda c: c["grid"][0].update(bo=0),
                   lambda c: c.update(validation={}),
                   lambda c: c["calibration"]["T1"]["widths"].pop("b1"),
                   lambda c: c["calibration"]["T1"].update(boundary="result-selected"),
                   lambda c: c["validation"]["v2"].update(labels=["flow", "flow"])]
        for change in changes:
            c, o, _ = fixture(); change(c)
            with self.assertRaises(reader.ContractError): self.run_case(c, o)

    def test_unknown_fields_ids_units_rejected_even_excluded_candidate(self):
        for change in (lambda o: o.update(extra=True),
                       lambda o: o["calibration"]["T1"]["predictions"].update(unknown={}),
                       lambda o: o["validation"].update(unknown={}),
                       lambda o: o["calibration"]["T1"]["predictions"]["b1"].update(unit="wrong"),
                       lambda o: o["validation"]["v1"]["predictions"]["b2"].update(unit="wrong"),
                       lambda o: o["validation"]["v2"]["predictions"]["b2"].update(value="invented")):
            c, o, _ = fixture()
            o["calibration"]["T1"]["predictions"]["b2"]["value"] = 20
            change(o)
            with self.assertRaises(reader.ContractError): self.run_case(c, o)

    def test_artifact_and_contract_binding(self):
        for change in ("contract", "condition", "source", "bytes", "duplicate", "missing"):
            c, o, a = fixture()
            if change == "contract": o["contract_sha256"] = "b" * 64
            if change == "condition": c["condition_sha256"] = "b" * 64
            if change == "source": o["calibration"]["T1"]["experiment"]["source_ids"] = ["unknown"]
            if change == "bytes": a["observations.txt"] += b"mutated"
            if change == "duplicate": o["artifacts"].append(copy.deepcopy(o["artifacts"][0]))
            if change == "missing": del a["observations.txt"]
            with self.subTest(change=change), self.assertRaises(reader.ContractError): self.run_case(c, o, a)

    def test_seed_reserved_duplicates_and_overlap(self):
        for reserved in (15485863, 86028121, 104395301):
            for role in ("C0", "C1", "C2"):
                c, o, _ = fixture(); o["seed_manifest"][role] = [reserved]
                with self.assertRaises(reader.ContractError): self.run_case(c, o)
        for change in (lambda o: o["seed_manifest"].update(C0=[101, 101]),
                       lambda o: o["seed_manifest"].update(C1=[101]),
                       lambda o: o["seed_manifest"].update(C0=[True]),
                       lambda o: o["seed_manifest"].update(C0=["101"]),
                       lambda o: o["seed_manifest"].update(C3=[109])):
            c, o, _ = fixture(); change(o)
            with self.assertRaises(reader.ContractError): self.run_case(c, o)

    def test_explicit_paired_seed_role_and_missing_manifest(self):
        c, o, _ = fixture()
        c["seed_policy"]["allowed_role_overlap"] = [["C0", "C1"]]
        o["seed_manifest"]["C1"] = [101]
        out = self.run_case(c, o)
        self.assertEqual(out["seed_check"]["overlaps"], [{"roles": ["C0", "C1"], "seeds": [101]}])
        del o["seed_manifest"]
        self.assertEqual(self.run_case(c, o)["seed_check"]["status"], "NOT_PROVIDED")

    def test_json_duplicate_keys_unicode_nonfinite_and_depth_rejected(self):
        for text in ('{"a":1,"a":2}', '{"n":NaN}', '{"n":Infinity}', '{"n":١}', '[' * 10000 + '0' + ']' * 10000):
            with self.assertRaises(reader.ContractError): reader.loads_strict(text)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="d3-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        c, o, artifacts = fixture()
        self.contract = self.root / "contract.json"
        self.contract.write_text(json.dumps(c), encoding="utf-8")
        o["contract_sha256"] = sha(self.contract.read_bytes())
        self.observations = self.root / "observations.json"
        self.observations.write_text(json.dumps(o), encoding="utf-8")
        for path, content in artifacts.items(): (self.root / path).write_bytes(content)

    def run_cli(self, output="result.json"):
        return subprocess.run([sys.executable, "-I", str(MODULE_PATH), "--contract", str(self.contract),
                               "--observations", str(self.observations), "--out", str(self.root / output)],
                              text=True, capture_output=True, check=False)

    def test_actual_cli_and_existing_output_refusal(self):
        result = self.run_cli(); self.assertEqual(result.returncode, 0, result.stderr)
        output = (self.root / "result.json").read_bytes()
        payload = json.loads(output)
        self.assertEqual(payload["validation"]["aggregate"], "all-compatible")
        self.assertEqual(payload["input_sha256"]["contract"], sha(self.contract.read_bytes()))
        self.assertEqual(payload["input_sha256"]["observations"], sha(self.observations.read_bytes()))
        self.assertEqual(payload["contract_binding"], "actual-input-bytes-verified")
        repeat = self.run_cli(); self.assertNotEqual(repeat.returncode, 0)
        self.assertEqual((self.root / "result.json").read_bytes(), output)

    def test_bad_hash_no_output(self):
        (self.root / "observations.txt").write_text("corrupted", encoding="utf-8")
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "result.json").exists())

    def test_artifact_path_escape_and_symlink_refused(self):
        for path in ("../outside.txt", "/etc/passwd", "linked.txt"):
            o = json.loads(self.observations.read_text())
            o["artifacts"][1]["path"] = path
            self.observations.write_text(json.dumps(o))
            if path == "linked.txt": (self.root / path).symlink_to(self.root / "observations.txt")
            result = self.run_cli()
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((self.root / "result.json").exists())

    def test_json_parser_duplicate_no_output(self):
        self.observations.write_text('{"schema":"x", "schema":"y"}')
        self.assertNotEqual(self.run_cli().returncode, 0)
        self.assertFalse((self.root / "result.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
