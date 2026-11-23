"""Bind the author's verified B2-U archives to the original B2-U submission and return."""
import hashlib
import json
from pathlib import Path
import re
import sys

U_PIN = "f9c8ee5a2cc590ceb70766d144e82ad571942535"
U_JOB = "368758"
U_CASE = "PRECAL_R1_B2_U"
FIRST8 = "docs/reviews/mixer_first8_launch_preparation_20261106"
ARCHIVES = ("b2_report.tar.gz", "b2_full_result.tar.gz")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def regular(path):
    require(path.is_file() and not path.is_symlink(), "Missing or linked B2-U file: " + path.name)
    return path


def check_record(record):
    scheduler = record["scheduler"]
    require(record["case"] == U_CASE and record["role"] == "U"
            and record["release_pin"] == U_PIN and record["label"] == "DEVELOPMENT_DATA_ONLY"
            and U_JOB == record["job_id"] == record["job_end_id"] == scheduler["job_id"],
            "B2-U case, source or job identity")
    require(type(record["runner_rc"]) is int and record["runner_rc"] == 0
            and scheduler["state"] == "COMPLETED" and scheduler["exit_code"] == "0:0"
            and record["return_ready"] is True and record["exact_frame_names"] is True
            and type(record["frame_count"]) is int and record["frame_count"] == 234
            and record["post_runtime_matches"] is True and record["w9"] == "LIVE_TERMINAL_MATCH",
            "B2-U normal completion, 234 frames and live W9 required")
    require(re.fullmatch(r"collection_[0-9]+", record["directory"]), "Malformed B2-U collection name")
    hashes = record["archive_hashes"]
    require(set(hashes) == set(ARCHIVES)
            and all(re.fullmatch("[0-9a-f]{64}", h) for h in hashes.values()), "B2-U archive identities")
    return hashes


def check_manifest(folder, hashes):
    rows = regular(folder / "SHA256SUMS").read_text(encoding="ascii").splitlines()
    require(sorted(rows) == sorted(h+"  "+n for n, h in hashes.items()), "B2-U archive checksum list")


def verify_local(folder, output):
    receipt = regular(folder / "return.json").read_bytes()
    hashes = check_record(json.loads(receipt))
    check_manifest(folder, hashes)
    for name, expected in hashes.items():
        digest = hashlib.sha256()
        with regular(folder / name).open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        require(digest.hexdigest() == expected, "B2-U archive differs: " + name)
    with output.open("xb") as out:
        out.write(receipt)
    return hashlib.sha256(receipt).hexdigest()


def verify_original(root, proof):
    original = regular(root / "arms/U/return.json")
    receipt = original.read_bytes()
    require(receipt == regular(proof).read_bytes(), "Local and original B2-U receipts differ")
    record = json.loads(receipt)
    hashes = check_record(record)
    collection = original.parent / record["directory"]
    require(collection.is_dir() and not collection.is_symlink(), "B2-U collection directory")
    check_manifest(collection, hashes)
    submitted = json.loads(regular(root / "B" / FIRST8 / "cases" / U_CASE / "submission.receipt.json").read_bytes())
    require(submitted["case"] == U_CASE and submitted["state"] == "SUBMITTED"
            and str(submitted["job_id"]) == U_JOB, "Original B2-U submission receipt differs")
    return original


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: verified U return directory, new proof file")
    print(verify_local(Path(sys.argv[1]), Path(sys.argv[2])))
