#!/usr/bin/env python3
"""D3 finite-grid decisions from explicit widths and byte-bound observations.

This is a decision calculator, not a simulation launcher, registration authority,
statistical uncertainty estimator, or physical eligibility/receipt validator.
See docs/reviews/mixer_d3_candidate_reader_contract_20261024.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from decimal import Decimal, InvalidOperation, localcontext

MAX_JSON_BYTES = 16 * 1024 * 1024
MAX_ARTIFACT_BYTES = 64 * 1024 * 1024
MAX_TOTAL_ARTIFACT_BYTES = 256 * 1024 * 1024
MAX_OUTPUT_BYTES = 64 * 1024 * 1024
MAX_GRID = 10000
MAX_VALIDATION = 64
MAX_DECISION_CELLS = 20000
RESERVED_CONFIRMATION_SEEDS = frozenset((15485863, 86028121, 104395301))
ROLES = ("C0", "C1", "C2")
HEX64 = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
ID = re.compile(r"[A-Za-z][A-Za-z0-9_.-]{0,95}\Z", re.ASCII)
FAILURE_STATES = frozenset(("technical-failure", "observable-undefined", "unsupported-contract", "missing"))


class ContractError(ValueError):
    """Malformed, ambiguous, unsupported, or unbound input; no decision issued."""


def _fail(where, message):
    raise ContractError(f"{where}: {message}")


def _obj(value, where, allowed, required=()):
    if not isinstance(value, dict):
        _fail(where, "expected object")
    extra, missing = set(value) - set(allowed), set(required) - set(value)
    if extra or missing:
        _fail(where, f"unknown fields {sorted(extra)}, missing fields {sorted(missing)}")
    return value


def _string(value, where, *, identifier=False):
    if not isinstance(value, str) or not value.strip() or len(value) > 512 or any(ord(c) < 32 for c in value):
        _fail(where, "expected nonempty text without control characters (maximum 512 characters)")
    if identifier and ID.fullmatch(value) is None:
        _fail(where, "expected ASCII identifier")
    return value


def _hash(value, where):
    if not isinstance(value, str) or HEX64.fullmatch(value) is None:
        _fail(where, "expected lowercase full SHA-256")
    return value


def _number(value, where, *, minimum=None, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        _fail(where, "expected finite JSON number, not boolean or string")
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        _fail(where, "invalid decimal")
    if not number.is_finite() or len(number.as_tuple().digits) > 64 or (number and abs(number.adjusted()) > 300):
        _fail(where, "number must be finite, at most 64 significant digits and decimal magnitude 1e-300..1e300")
    if (positive and number <= 0) or (minimum is not None and number < minimum):
        _fail(where, "number outside allowed domain")
    return number


def _integer(value, where, *, minimum=1):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum or value > 2**53 - 1:
        _fail(where, "expected bounded integer")
    return value


def _unique_strings(values, where, *, allow_empty=False, identifiers=True):
    if not isinstance(values, list) or (not values and not allow_empty) or len(values) > MAX_GRID:
        _fail(where, "expected bounded nonempty list" if not allow_empty else "expected bounded list")
    checked = [_string(v, where, identifier=identifiers) for v in values]
    if len(set(checked)) != len(checked):
        _fail(where, "duplicate list value")
    return checked


def _pairs_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("JSON", f"duplicate key {key!r}")
        result[key] = value
    return result


def loads_strict(text):
    """Reject duplicate keys and the non-JSON NaN/Infinity Python extension."""
    try:
        if len(text.encode("utf-8")) > MAX_JSON_BYTES:
            _fail("JSON", "input exceeds byte limit")
        return json.loads(text, object_pairs_hook=_pairs_no_duplicates, parse_float=Decimal,
                          parse_constant=lambda token: _fail("JSON", f"nonfinite token {token}"))
    except (json.JSONDecodeError, UnicodeError, RecursionError, ValueError) as exc:
        if isinstance(exc, ContractError):
            raise
        raise ContractError(f"JSON: {exc}") from exc


def _rules(contract):
    _obj(contract, "contract", {"schema", "analysis_id", "condition_sha256", "grid", "calibration", "validation", "seed_policy"},
         {"schema", "analysis_id", "condition_sha256", "grid", "calibration", "validation"})
    if contract["schema"] != "mixer_d3_decision_contract/1":
        _fail("contract.schema", "unsupported schema")
    _string(contract["analysis_id"], "analysis_id", identifier=True)
    _hash(contract["condition_sha256"], "condition_sha256")
    grid = contract["grid"]
    if not isinstance(grid, list) or not grid or len(grid) > MAX_GRID:
        _fail("grid", "expected 1..10000 ordered points")
    ids, bos = [], []
    for point in grid:
        _obj(point, "grid.point", {"id", "bo"}, {"id", "bo"})
        ids.append(_string(point["id"], "grid.id", identifier=True))
        bos.append(_number(point["bo"], "grid.bo", positive=True))
    if len(set(ids)) != len(ids) or any(a >= b for a, b in zip(bos, bos[1:])):
        _fail("grid", "IDs must be unique and Bo strictly increasing in registered order")
    _obj(contract["calibration"], "calibration rules", {"T1", "T2"}, {"T1", "T2"})
    validation = contract["validation"]
    if not isinstance(validation, dict) or not 1 <= len(validation) <= MAX_VALIDATION:
        _fail("validation rules", "expected 1..64 mandatory validation items")
    if len(ids) * (2 + len(validation)) > MAX_DECISION_CELLS:
        _fail("contract", "grid times test count exceeds supported decision-cell limit")
    rules = {}
    for group in ("calibration", "validation"):
        rules[group] = {}
        for tid, rule in contract[group].items():
            _string(tid, "test id", identifier=True)
            kind = "scalar" if group == "calibration" else rule.get("kind") if isinstance(rule, dict) else None
            if kind not in ("scalar", "categorical"):
                _fail(tid, "unsupported comparison kind")
            allowed = {"unit", "boundary", "widths"} if kind == "scalar" else {"unit", "rule", "labels"}
            if group == "validation":
                allowed.add("kind")
            _obj(rule, tid, allowed, allowed)
            _string(rule["unit"], tid + ".unit")
            entry = {"kind": kind, "unit": rule["unit"]}
            if kind == "scalar":
                if rule["boundary"] != "inclusive":
                    _fail(tid, "only explicit inclusive boundary is supported")
                _obj(rule["widths"], tid + ".widths", ids, ids)
                entry["widths"] = {bid: _number(rule["widths"][bid], tid + ".width", minimum=0) for bid in ids}
            else:
                if rule["rule"] != "exact-match":
                    _fail(tid, "categorical comparisons require explicit exact-match rule")
                entry["labels"] = _unique_strings(rule["labels"], tid + ".labels", identifiers=False)
            rules[group][tid] = entry
    return ids, bos, rules


def _artifacts(contract, observations, artifact_loader):
    entries = observations["artifacts"]
    if not isinstance(entries, list) or not 1 <= len(entries) <= MAX_GRID:
        _fail("artifacts", "expected bounded nonempty manifest")
    found, paths, total = {}, set(), 0
    for entry in entries:
        _obj(entry, "artifact", {"id", "path", "sha256"}, {"id", "path", "sha256"})
        aid = _string(entry["id"], "artifact.id", identifier=True)
        path = _string(entry["path"], "artifact.path")
        # A portable artifact path is relative, slash separated and traversal-free.
        p = PurePosixPath(path)
        if p.is_absolute() or "\\" in path or ":" in path or any(part in ("", ".", "..") for part in path.split("/")):
            _fail("artifact.path", "expected relative traversal-free path")
        expected = _hash(entry["sha256"], "artifact.sha256")
        if aid in found or path in paths:
            _fail("artifacts", "duplicate id or path")
        try:
            content = artifact_loader(path)
        except (OSError, KeyError, ValueError) as exc:
            raise ContractError(f"artifact {aid}: unreadable: {exc}") from exc
        if not isinstance(content, bytes) or len(content) > MAX_ARTIFACT_BYTES:
            _fail(aid, "artifact must be bounded bytes")
        total += len(content)
        if total > MAX_TOTAL_ARTIFACT_BYTES:
            _fail("artifacts", "combined artifact byte limit exceeded")
        actual = hashlib.sha256(content).hexdigest()
        if actual != expected:
            _fail(aid, "artifact SHA-256 mismatch")
        found[aid] = actual
        paths.add(path)
    condition = observations["condition_artifact"]
    if not isinstance(condition, str) or condition not in found or found[condition] != contract["condition_sha256"]:
        _fail("condition_artifact", "condition bytes do not match contract")
    return found


def _point(point, rule, artifacts, where):
    if point is None:
        return {"eligible": False, "reason": "missing observation"}
    _obj(point, where, {"state", "reason", "value", "unit", "source_ids", "uncertainty", "flags"}, {"state"})
    state = point["state"]
    if not isinstance(state, str) or state not in FAILURE_STATES | {"eligible"}:
        _fail(where, "unsupported state")
    flags = _unique_strings(point.get("flags", []), where + ".flags", allow_empty=True)
    if state != "eligible":
        _obj(point, where, {"state", "reason", "source_ids", "flags"}, {"state", "reason"})
        reason = _string(point["reason"], where + ".reason")
        if "source_ids" in point:
            sources = _unique_strings(point["source_ids"], where + ".source_ids")
            if set(sources) - set(artifacts):
                _fail(where, "unknown artifact source")
        return {"eligible": False, "reason": state + ": " + reason, "flags": flags}
    required = {"value", "unit", "source_ids"}
    if rule["kind"] == "scalar":
        required.add("uncertainty")
    missing = sorted(key for key in required if key not in point or point[key] is None)
    # Present malformed fields must never hide behind another missing field.
    if "unit" in point and point["unit"] is not None and point["unit"] != rule["unit"]:
        _fail(where, "unit mismatch")
    sources = []
    if point.get("source_ids") is not None:
        sources = _unique_strings(point["source_ids"], where + ".source_ids")
        if set(sources) - set(artifacts):
            _fail(where, "unknown artifact source")
    result = {"eligible": not missing, "reason": "missing " + ",".join(missing) if missing else "eligible declaration with verified source bytes",
              "flags": flags, "source_ids": sources, "unit": rule["unit"]}
    if point.get("value") is not None:
        if rule["kind"] == "scalar":
            result["value"] = _number(point["value"], where + ".value")
        elif not isinstance(point["value"], str) or point["value"] not in rule["labels"]:
            _fail(where, "unregistered categorical label")
        else:
            result["value"] = point["value"]
    if "uncertainty" in point and point["uncertainty"] is not None:
        if rule["kind"] != "scalar":
            _fail(where, "categorical rule does not use scalar uncertainty")
        uncertainty = point["uncertainty"]
        _obj(uncertainty, where + ".uncertainty", {"value", "unit", "n", "df", "method"}, {"value", "unit", "n", "df", "method"})
        if uncertainty["unit"] != rule["unit"]:
            _fail(where, "uncertainty unit mismatch")
        result["uncertainty"] = {"value": _number(uncertainty["value"], where + ".uncertainty.value", minimum=0),
                                 "unit": uncertainty["unit"], "n": _integer(uncertainty["n"], where + ".n"),
                                 "df": _number(uncertainty["df"], where + ".df", positive=True),
                                 "method": _string(uncertainty["method"], where + ".method")}
    return result


def _observed_groups(observations, rules, ids, artifacts):
    result = {}
    for group in ("calibration", "validation"):
        raw = observations.get(group, {})
        _obj(raw, group, rules[group])
        result[group] = {}
        for tid, rule in rules[group].items():
            test = raw.get(tid, {})
            _obj(test, group + "." + tid, {"experiment", "predictions"})
            predictions = test.get("predictions", {})
            _obj(predictions, tid + ".predictions", ids)
            # Validate all supplied points, including candidates later excluded by calibration.
            result[group][tid] = {
                "experiment": _point(test.get("experiment"), rule, artifacts, tid + ".experiment"),
                "predictions": {bid: _point(predictions.get(bid), rule, artifacts, tid + "." + bid) for bid in ids}}
    return result


def _comparison(test, rule, bid, *, upper):
    prediction, experiment = test["predictions"][bid], test["experiment"]
    row = {"id": bid, "prediction": prediction, "experiment": experiment}
    if not prediction["eligible"] or not experiment["eligible"] or "INSENSITIVE" in prediction.get("flags", []):
        row.update(status="UNASSESSED" if upper else "unassessed",
                   reason="prediction: " + prediction["reason"] + "; experiment: " + experiment["reason"])
        return row
    if rule["kind"] == "scalar":
        # The numeric bounds above make 700 digits sufficient for exact subtraction.
        with localcontext() as ctx:
            ctx.prec = 700
            difference = abs(prediction["value"] - experiment["value"])
        width = rule["widths"][bid]
        compatible = difference <= width
        row.update(absolute_difference=difference, width=width, boundary="inclusive")
    else:
        compatible = prediction["value"] == experiment["value"]
        row["rule"] = "exact-match"
    status = "compatible" if compatible else "incompatible"
    row.update(status=status.upper() if upper else status, reason="explicit contract comparison")
    return row


def _seed_check(contract, observations):
    policy = contract.get("seed_policy")
    allowed = set()
    if policy is not None:
        _obj(policy, "seed_policy", {"allowed_role_overlap"}, {"allowed_role_overlap"})
        pairs = policy["allowed_role_overlap"]
        if not isinstance(pairs, list) or len(pairs) > 3:
            _fail("seed_policy", "expected list of at most three role pairs")
        for pair in pairs:
            if not isinstance(pair, list) or len(pair) != 2 or any(x not in ROLES for x in pair) or pair[0] == pair[1]:
                _fail("seed_policy", "invalid role pair")
            key = tuple(sorted(pair))
            if key in allowed:
                _fail("seed_policy", "duplicate role pair")
            allowed.add(key)
    if "seed_manifest" not in observations:
        return {"status": "NOT_PROVIDED", "historical_nonuse_verified": False}
    if policy is None:
        _fail("seed_manifest", "explicit role-overlap policy required")
    manifest = observations["seed_manifest"]
    _obj(manifest, "seed_manifest", ROLES, ROLES)
    sets = {}
    for role in ROLES:
        values = manifest[role]
        if not isinstance(values, list) or len(values) > MAX_GRID:
            _fail(role, "expected bounded seed list")
        seeds = [_integer(seed, role + ".seed") for seed in values]
        if len(set(seeds)) != len(seeds) or set(seeds) & RESERVED_CONFIRMATION_SEEDS:
            _fail(role, "duplicate or reserved confirmation seed")
        sets[role] = set(seeds)
    overlaps = []
    for left, right in (("C0", "C1"), ("C0", "C2"), ("C1", "C2")):
        shared = sorted(sets[left] & sets[right])
        if shared and (left, right) not in allowed:
            _fail("seed_manifest", f"undeclared overlap {left}/{right}")
        if shared:
            overlaps.append({"roles": [left, right], "seeds": shared})
    return {"status": "CHECKED_SUPPLIED_MANIFEST", "roles": {r: sorted(sets[r]) for r in ROLES},
            "reserved_confirmation_seeds": sorted(RESERVED_CONFIRMATION_SEEDS), "overlaps": overlaps,
            "historical_nonuse_verified": False, "independent_samples_certified": False}


def _json_numbers(value):
    """Output decimal text preserves comparisons without a binary-float roundtrip."""
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_numbers(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_numbers(item) for item in value]
    return value


def evaluate(contract, observations, *, contract_sha256, artifact_loader):
    """Compute input-conditioned decisions; loader must return the actual bytes.

    The API caller supplies contract_sha256; only the CLI computes it directly
    from the bytes parsed into contract. API results label that distinction.
    """
    ids, bos, rules = _rules(contract)
    _obj(observations, "observations", {"schema", "contract_sha256", "condition_artifact", "artifacts", "calibration", "validation", "seed_manifest"},
         {"schema", "contract_sha256", "condition_artifact", "artifacts"})
    if observations["schema"] != "mixer_d3_observations/1":
        _fail("observations.schema", "unsupported schema")
    if _hash(observations["contract_sha256"], "observations.contract_sha256") != _hash(contract_sha256, "supplied contract SHA"):
        _fail("contract_sha256", "contract digest does not match observation binding")
    artifacts = _artifacts(contract, observations, artifact_loader)
    seed_check = _seed_check(contract, observations)
    groups = _observed_groups(observations, rules, ids, artifacts)
    calibration = {tid: [_comparison(groups["calibration"][tid], rules["calibration"][tid], bid, upper=True) for bid in ids]
                   for tid in ("T1", "T2")}
    accepted = {tid: [row["id"] for row in rows if row["status"] == "COMPATIBLE"] for tid, rows in calibration.items()}
    accepted_sets = {tid: set(values) for tid, values in accepted.items()}
    S = [bid for bid in ids if bid in accepted_sets["T1"] and bid in accepted_sets["T2"]]
    candidate_ids = set(S)
    empty_case = ("not-empty" if S else "both-tests-empty" if not accepted["T1"] and not accepted["T2"] else
                  "T1-empty" if not accepted["T1"] else "T2-empty" if not accepted["T2"] else "disjoint")
    neighbor_groups = []
    previous_selected = False
    for bid in ids:
        if bid in candidate_ids:
            if not previous_selected:
                neighbor_groups.append([])
            neighbor_groups[-1].append(bid)
        previous_selected = bid in candidate_ids
    boundary = {"lower_candidate": ids[0] in candidate_ids, "upper_candidate": ids[-1] in candidate_ids,
                "lower_unassessed": any(calibration[t][0]["status"] == "UNASSESSED" for t in calibration),
                "upper_unassessed": any(calibration[t][-1]["status"] == "UNASSESSED" for t in calibration)}
    candidates = []
    counts = {"compatible": 0, "incompatible": 0, "unassessed": 0}
    for bid in S:
        items = {tid: _comparison(groups["validation"][tid], rule, bid, upper=False) for tid, rule in rules["validation"].items()}
        statuses = [row["status"] for row in items.values()]
        status = "unassessed" if "unassessed" in statuses else "incompatible" if "incompatible" in statuses else "compatible"
        candidates.append({"id": bid, "status": status, "items": items})
        counts[status] += 1
    aggregate = ("not-applicable" if not S else "incomplete" if counts["unassessed"] else
                 "all-compatible" if counts["compatible"] == len(S) else
                 "none-compatible" if counts["incompatible"] == len(S) else "mixed")
    with localcontext() as ctx:
        ctx.prec = 50
        output_grid = [{"id": bid, "bo_code": bo, "bo_po_approx": bo / Decimal("6.75")} for bid, bo in zip(ids, bos)]
    result = {
        "schema": "mixer_d3_decision_result/1", "analysis_id": contract["analysis_id"],
        "numeric_encoding": "decimal-text", "contract_sha256": contract_sha256,
        "contract_binding": "caller-supplied-digest-compared",
        "verified_artifact_sha256": artifacts, "condition_sha256": contract["condition_sha256"],
        "grid": output_grid, "bo_po_definition": "Bo_code / 6.75; 50 significant decimal digits",
        "calibration": calibration, "S_T1": accepted["T1"], "S_T2": accepted["T2"], "S": S,
        "calibration_complete": all(row["status"] != "UNASSESSED" for rows in calibration.values() for row in rows),
        "empty_case": empty_case, "neighbor_groups": neighbor_groups,
        "boundary": boundary, "range_limited": any(boundary.values()),
        "validation": {"aggregate": aggregate, "counts": counts, "candidates": candidates},
        "seed_check": seed_check, "execution_ready": False,
        "limitations": ["finite-grid-only", "no-continuous-interval-or-center", "no-identifiability-claim",
                        "input-eligibility-and-uncertainty-declarations-not-physically-validated",
                        "artifact-hashes-do-not-prove-preregistration-or-blinding",
                        "validation-does-not-redefine-calibration-S", "not-an-execution-approval"],
    }
    return _json_numbers(result)


def _read_regular(path, limit):
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            _fail(str(path), "expected bounded regular file")
        data = stream.read(limit + 1)
        if len(data) > limit:
            _fail(str(path), "byte limit exceeded")
        return data


def _artifact_loader(root):
    root = root.resolve(strict=True)
    def load(relative):
        current = root
        for part in PurePosixPath(relative).parts:
            current = current / part
            if current.is_symlink():
                _fail(relative, "artifact symlinks are not supported")
        resolved = current.resolve(strict=True)
        if not resolved.is_relative_to(root):
            _fail(relative, "artifact escapes observations directory")
        return _read_regular(resolved, MAX_ARTIFACT_BYTES)
    return load


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--observations", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path, help="new JSON file; never overwrites an existing path")
    args = parser.parse_args(argv)
    try:
        contract_bytes = _read_regular(args.contract, MAX_JSON_BYTES)
        observation_bytes = _read_regular(args.observations, MAX_JSON_BYTES)
        contract = loads_strict(contract_bytes.decode("utf-8"))
        observations = loads_strict(observation_bytes.decode("utf-8"))
        contract_sha = hashlib.sha256(contract_bytes).hexdigest()
        result = evaluate(contract, observations, contract_sha256=contract_sha,
                          artifact_loader=_artifact_loader(args.observations.parent))
        result["input_sha256"] = {"contract": contract_sha, "observations": hashlib.sha256(observation_bytes).hexdigest()}
        result["contract_binding"] = "actual-input-bytes-verified"
        result["reader_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        encoded = (json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
        if len(encoded) > MAX_OUTPUT_BYTES:
            _fail("output", "result exceeds byte limit")
        fd = os.open(args.out, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(encoded)
        print(json.dumps({"output": str(args.out), "candidate_count": len(result["S"]),
                          "validation": result["validation"]["aggregate"], "execution_ready": False}))
        return 0
    except (ContractError, OSError, UnicodeError, RecursionError) as exc:
        print(f"D3_CONTRACT_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
