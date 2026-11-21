"""Apply the U6(c) doubled-resolution force rule to fixed development evidence."""
import argparse
from bisect import bisect_right
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import tarfile


HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / "suyoung_u6c_doubling_readback_20261122" / "doubling.py"
PREVIOUS_SHA256 = "9d664ed38a70295b9bd04ecbf5dae4ffda663c5efbc348c30a77bf6b99fa1bda"
SUMMARY_SHA256 = "bb893705987c692699741fe82ed544c1104f482e3dd2e30d6157a6da08ff6ada"
RULE_SHA256 = "1736322b4b2f4cef384becd97099998668137c19272e504edd951b698502a8f4"
PAIRS = ("F8_F16", "F12_F24")


def digest(data):
    return hashlib.sha256(data).hexdigest()


if digest(PREVIOUS.read_bytes()) != PREVIOUS_SHA256:
    raise ValueError("source mismatch for fixed trace reader")
_spec = importlib.util.spec_from_file_location("u6c_previous_curves", PREVIOUS)
curves = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(curves)


def exceeds(error, denominator):
    # Compare the two unrounded binary64 results to the exact fraction 1/20.
    # This also avoids overflow when the reference or error is very large.
    en, ed = error.as_integer_ratio()
    dn, dd = denominator.as_integer_ratio()
    return 20 * en * dd > dn * ed


def held(reason):
    return {"comparison": "HOLD", "reason": reason, "ratio": None, "exceeding_knots": None}


def compare(coarse, fine):
    """Evaluate a pair of nonnegative compression curves in the same units."""
    try:
        curves.validate(coarse)
        curves.validate(fine)
        a = [u for u, _ in coarse]
        b = [u for u, _ in fine]
        end = min(a[-1], b[-1])
        ac, bc = bisect_right(a, end), bisect_right(b, end)
        knots = sorted(set(a[:ac]).union(b[:bc]))
        refs = [curves.interpolate(u, b, fine) for u in knots]
        differences = [curves.interpolate(u, a, coarse) - reference
                       for u, reference in zip(knots, refs)]
        if not all(map(math.isfinite, refs)) or not all(map(math.isfinite, differences)):
            return held("NONFINITE_INTERPOLATION")
    except (ArithmeticError, TypeError, ValueError, IndexError):
        return held("INVALID_CURVE")

    peak_index = max(range(len(knots)), key=lambda i: abs(refs[i]))
    error_index = max(range(len(knots)), key=lambda i: abs(differences[i]))
    denominator = abs(refs[peak_index])
    error = abs(differences[error_index])
    result = {
        "common_start_u": 0., "common_end_u": end, "coarse_end_u": a[-1], "fine_end_u": b[-1],
        "coarse_samples": len(a), "fine_samples": len(b),
        "coarse_samples_in_common": ac, "fine_samples_in_common": bc, "union_knots": len(knots),
        "fine_peak_MPa": denominator, "u_at_first_fine_peak": knots[peak_index],
        "max_abs_difference_MPa": error, "coarse_minus_fine_at_first_max_MPa": differences[error_index],
        "u_at_first_max_abs": knots[error_index],
    }
    if denominator == 0.:
        return dict(result, **held("ZERO_REFERENCE"))
    above = [u for u, d in zip(knots, differences) if exceeds(abs(d), denominator)]
    ratio = error / denominator
    result.update(comparison="EXCEEDS" if above else "WITHIN", exceeding_knots=len(above),
                  first_exceedance_u=above[0] if above else None,
                  ratio=ratio if math.isfinite(ratio) else None)
    return result


def aggregate(pairs):
    """A demonstrated exceedance survives a separate pair's missing data."""
    states = [pairs.get(p, {}).get("comparison", "HOLD") for p in PAIRS]
    if "EXCEEDS" in states:
        return "EXCEEDS"
    return "WITHIN" if all(s == "WITHIN" for s in states) else "HOLD"


def replay(path):
    report = {
        "scope": "RETROSPECTIVE_DEVELOPMENT_REPLAY", "qualification_tested": False,
        "qualification": "HOLD", "stage3_go": False,
        "expected_rule_sha256": RULE_SHA256,
        "trace_reader_sha256": PREVIOUS_SHA256, "expected_archive_sha256": curves.ARCHIVE_DIGEST,
        "required_pairs": list(PAIRS), "historical_comparison": "HOLD", "pairs": {},
    }
    try:
        report["rule_sha256"] = digest((HERE / "rule.json").read_bytes())
    except OSError:
        report["reason"] = "FROZEN_RULE_UNAVAILABLE"
        return report
    if report["rule_sha256"] != RULE_SHA256:
        report["reason"] = "FROZEN_RULE_MISMATCH"
        return report
    try:
        with path.open("rb") as stream:
            observed = hashlib.file_digest(stream, "sha256").hexdigest()
            report["archive_sha256"] = observed
            if observed != curves.ARCHIVE_DIGEST:
                report["reason"] = "ARCHIVE_HASH_MISMATCH"
                return report
            stream.seek(0)
            with tarfile.open(fileobj=stream, mode="r:gz") as archive:
                names = archive.getnames()
                if len(set(names)) != len(names):
                    raise ValueError("duplicate archive name")
                raw = archive.extractfile("run/summary.json").read()
                origin = archive.extractfile("run/origin.txt").read().decode("ascii").splitlines()
                if digest(raw) != SUMMARY_SHA256 or "release="+curves.SOURCE not in origin:
                    raise ValueError("fixed release or summary mismatch")
                summary = json.loads(raw)
                report.update(source_release=curves.SOURCE, summary_sha256=SUMMARY_SHA256,
                              receipts={})
                for cells, pair in zip((8, 12), PAIRS):
                    try:
                        coarse, h_coarse, cref = curves.read_curve(archive, summary, cells)
                        fine, h_fine, fref = curves.read_curve(archive, summary, 2*cells)
                        report["receipts"]["F"+str(cells)] = cref
                        report["receipts"]["F"+str(2*cells)] = fref
                        if h_coarse != h_fine:
                            raise ValueError("initial height mismatch")
                        result = compare(coarse, fine)
                    except (ArithmeticError, KeyError, OSError, TypeError, ValueError):
                        result = held("CURVE_OR_RECEIPT_MISMATCH")
                    report["pairs"][pair] = result
                report["historical_comparison"] = aggregate(report["pairs"])
    except (OSError, tarfile.TarError, KeyError, ValueError, TypeError):
        report["reason"] = "ARCHIVE_UNAVAILABLE_OR_INVALID"
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path, help="new JSON report")
    args = parser.parse_args()
    report = replay(args.archive)
    with args.output.open("x", encoding="ascii", newline="\n") as output:
        json.dump(report, output, indent=2, sort_keys=True, allow_nan=False)
        output.write("\n")
    # Exceedance is a completed technical readback. Its decision is in the JSON.
    return 4 if (report["historical_comparison"] == "HOLD" or
                 any(p["comparison"] == "HOLD" for p in report["pairs"].values())) else 0


if __name__ == "__main__":
    sys.exit(main())
