"""Read an author's returned WSL30 ZIP against its screen SHA and the fixed earlier metadata."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import sys
import zipfile

D = runpy.run_path(str(Path(__file__).with_name("check_live_metadata.py")))
check = D["check"]
PRIOR_SHA = "590db9cc8dcaf0802f48a720159435d0631a6e11ac005152f0137b756cb35158"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compare(archive, expected_hash, prior):
    check(archive.is_file() and archive.stat().st_size <= 1024 * 1024)
    with archive.open("rb") as handle:
        check(sha(handle.read()) == expected_hash)
        handle.seek(0)
        with zipfile.ZipFile(handle) as z:
            names = z.namelist()
            check(len(names) == len(set(names)) and
                  set(names) in ({"receipt.json", "SHA256SUMS"},
                                 {"receipt.json", "inventory.json", "SHA256SUMS"}))
            check(all(info.file_size <= 65536 for info in z.infolist()))
            files = {n: z.read(n) for n in names}
    sums = files.pop("SHA256SUMS").decode("ascii").splitlines()
    check(sorted(sums) == sorted(sha(data) + "  " + n for n, data in files.items()))
    receipt = json.loads(files["receipt.json"], object_pairs_hook=D["strict_object"])
    check(receipt["scope"] == "WSL30" and receipt["sealed_scanner_sha256"] == D["SCANNER_SHA"])
    check(receipt["execution_identity"] == "NOT_ESTABLISHED" and receipt["canonical_run_segment"] == "UNSELECTED")
    check(receipt["value_access"] == "NOT_GRANTED" and receipt["section5"] == "UNRESOLVED" and
          receipt["tau"] == "NOT_EVALUATED" and receipt["v13_release"] == "NOT_AUTHORIZED")
    if receipt["status"] == "INCOMPLETE":
        check("inventory.json" not in files and receipt["command_rc"] == 2)
        return {"status": "INCOMPLETE", "accepted_cases": 0}
    check(receipt["status"] == "INVENTORY_COMPLETE" and receipt["command_rc"] == 0)
    data = files["inventory.json"]
    check(receipt["inventory_sha256"] == sha(data))
    current = D["validate"](data, receipt["scanner_process_rc"])
    summary = D["observation"](current)
    check(receipt["observation"] == summary)
    historical = prior.read_bytes()
    check(sha(historical) == PRIOR_SHA)
    earlier = {r["case"]: r for r in D["validate"](historical, 0)["cases"]}
    changed = [r["case"] for r in current["cases"] if r != earlier[r["case"]]]
    return {"status": "METADATA_READBACK_OK", "observation": summary,
            "changed_metadata_cases_since_2026_11_08": sorted(changed),
            "execution_identity": "NOT_ESTABLISHED", "section5": "UNRESOLVED", "release_v13": "NOT_AUTHORIZED"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("screen_sha256")
    parser.add_argument("prior", type=Path)
    args = parser.parse_args()
    try:
        verdict = compare(args.archive, args.screen_sha256, args.prior)
    except (KeyError, TypeError, ValueError, OSError, zipfile.BadZipFile):
        print("HOLD: return integrity or metadata contract", file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps(verdict, sort_keys=True))
    raise SystemExit(0 if verdict["status"] == "METADATA_READBACK_OK" else 2)
