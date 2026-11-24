"""Read the returned B2-U rotation on the author's computer. No scheduler or simulation calls."""
import argparse
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import runpy
import tarfile
import tempfile


HERE = Path(__file__).resolve().parent
CASE = "PRECAL_R1_B2_U"
JOB = "368758"
PIN = "f9c8ee5a2cc590ceb70766d144e82ad571942535"
DECK_SHA = "b37974e5c0674947912e932c55517e9e84243293f29257183f8f70cc032f2fd7"
META_SHA = "7e7b3f13354aaf312d780f8b96094a432cc64fadd20c335b815ab871ff2602ec"
B_MANIFEST = "088460cc6a71db4fcc0b6fd326fb89ae629767a2ded45846952640ca44ac0ee0"
EXPECTED = {
    "b2_report.tar.gz": "a4be97a2d67652a1915c7918252ad79c7ec39e3a881bfc161b45df8254868403",
    "b2_full_result.tar.gz": "84d3cf8a0bf3e561622c4b78014690b2a2553b70bd1262512239cf82ed756c8e",
}
STRIDE = 32976
EXPECTED_DUMPS = {f"{CASE}/post/mix_{i * STRIDE}.liggghts": i for i in range(1, 235)}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def member_ok(member, seen):
    name = member.name
    check((member.isfile() or member.isdir()) and "\\" not in name and ":" not in name
          and all(part not in {"", ".", ".."} for part in name.split("/"))
          and name not in seen, "Invalid or repeated TAR member")
    seen.add(name)


def inspect_report(path, receipt):
    with tarfile.open(path, "r:gz") as report:
        seen = set()
        for member in report:
            member_ok(member, seen)

        def raw(name):
            member = report.getmember(name)
            check(member.isfile() and member.size <= 16 * 1024**2, "Invalid report member: " + name)
            return report.extractfile(member).read()

        def doc(name):
            return json.loads(raw(name))

        collection_path = "evidence/" + receipt["directory"]
        embedded = doc(collection_path + ".json")
        check(embedded == {k: v for k, v in receipt.items() if k not in {"directory", "archive_hashes"}},
              "Report and return.json collection disagree")
        check(sha(raw("B_manifest.json")) == B_MANIFEST and doc("control/pair_pin.json")["commit"] == PIN,
              "Deployment or controller identity differs")
        authority = doc("control/pair_authority.json")
        arm = doc("evidence/author_arm.json")
        check(authority["release_pin"] == arm["pin"] == PIN and authority["allowed_to_submit"] == [CASE]
              and arm["case"] == CASE and arm["token"] == authority["author_action"] == "GO_B2_U_ONCE"
              and authority["asset_manifest"] == B_MANIFEST, "Archived job authority differs")
        submission = doc("admission/" + CASE + ".submission.json")
        check(submission["state"] == "SUBMITTED" and submission["case"] == CASE
              and str(submission["job_id"]) == JOB, "Archived submission differs")
        pre = doc("evidence/runtime_pre/runtime.json")
        post = doc(collection_path + "_post/runtime.json")
        check(pre["matches"] is True and post["matches"] is True and not pre["mismatches"]
              and not post["mismatches"] and all(pre[k] == post[k] and pre[k] for k in ("linked", "packages"))
              and receipt["post_runtime_error"] is None, "Runtime identity differs")
        times = [pre["collected_unix"], receipt["job_end_unix"], receipt["post_start_unix"],
                 post["collected_unix"], receipt["post_finished_unix"]]
        check(all(type(t) in (float, int) and math.isfinite(t) for t in times) and times == sorted(times),
              "Runtime verification is outside the recorded terminal window")
        return {"w9": receipt["w9"], "runner_rc": receipt["runner_rc"],
                "state": receipt["scheduler"]["state"], "exit_code": receipt["scheduler"]["exit_code"],
                "elapsed": receipt["scheduler"]["raw"][3],
                "end_to_post_start_s": times[2] - times[1], "end_to_post_finish_s": times[4] - times[1]}


def inspect_full(path, receipt, observe_frame):
    seen, metadata, records, bindings = set(), {}, {}, {}
    fields = {CASE + "/" + name: name for name in ("in.mixer", "deck_meta.json", "job_end.json")}
    with gzip.open(path, "rb") as uncompressed:
        with tarfile.open(fileobj=uncompressed, mode="r|", bufsize=1024**2) as archive:
            for member in archive:
                member_ok(member, seen)
                name = member.name
                check(name.startswith(CASE + "/"), "Foreign case member")
                if name.startswith(CASE + "/post/mix_"):
                    check(member.isfile() and name in EXPECTED_DUMPS, "Unexpected native dump")
                    index = EXPECTED_DUMPS[name]
                    if index >= 34:
                        check(0 < member.size <= 256 * 1024**2, "Native dump size exceeds the reader bound")
                        data = archive.extractfile(member).read()
                        step = index * STRIDE
                        records[index] = observe_frame(io.BytesIO(data), step)
                        bindings[index] = {"step": step, "sha256": sha(data)}
                elif name in fields:
                    check(member.isfile() and member.size <= 4 * 1024**2, "Invalid case metadata member")
                    metadata[fields[name]] = archive.extractfile(member).read()
    check(EXPECTED_DUMPS.keys() <= seen, "Missing native dump(s)")
    check(sha(metadata["in.mixer"]) == DECK_SHA and sha(metadata["deck_meta.json"]) == META_SHA,
          "Native deck or metadata differs")
    end = json.loads(metadata["job_end.json"])
    check(str(end["job_id"]) == JOB and type(end["returncode"]) is int and end["returncode"] == 0
          and end["end_unix"] == receipt["job_end_unix"], "Native job-end receipt differs")
    order = range(34, 235)
    return [records[i] for i in order], [bindings[i] for i in order]


def readback(folder, out):
    check(folder.is_dir() and not folder.is_symlink(), "Missing or linked return directory")
    check(not out.resolve().is_relative_to(folder.resolve()), "Place new output outside the original return")
    check(not out.exists() and not out.is_symlink() and out.parent.is_dir(), "Provide a new output directory")
    validator_path = HERE / "mixer_b2_u_completion.py"
    if not validator_path.is_file():
        validator_path = next(p / "scripts/mixer_b2_u_completion.py" for p in HERE.parents
                              if (p / "scripts/mixer_b2_u_completion.py").is_file())
    validator = runpy.run_path(str(validator_path))
    observer_path = HERE / "flow_observer.py"
    observer = runpy.run_path(str(observer_path))
    names = [*EXPECTED, "SHA256SUMS", "return.json"]

    def input_stamp():
        stamps = []
        for name in names:
            stat = validator["regular"](folder / name).stat()
            stamps.append((stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns))
        return stamps

    stamp = input_stamp()
    with tempfile.TemporaryDirectory(dir=out.parent) as scratch:
        tmp = Path(scratch)
        proof = tmp / "proof"
        digest = validator["verify_local"](folder, proof)
        receipt = json.loads(proof.read_bytes())
        check(receipt["archive_hashes"] == EXPECTED, "Different B2-U return archive identities")
        runtime = inspect_report(folder / "b2_report.tar.gz", receipt)
        records, bindings = inspect_full(folder / "b2_full_result.tar.gz", receipt, observer["observe_frame"])
        summary = observer["summarize"](records)
        check(input_stamp() == stamp, "Return files changed during readback")
        provenance = {"case": CASE, "job_id": JOB, "release": PIN, "label": "DEVELOPMENT_DATA_ONLY",
                      "archives": EXPECTED, "return_receipt_sha256": digest, "runtime": runtime,
                      "in_mixer_sha256": DECK_SHA, "deck_meta_sha256": META_SHA,
                      "archive_frame_names_verified": 234, "observed_steps_sha256": bindings,
                      "source_sha256": {p.name: sha(p.read_bytes()) for p in
                                        (Path(__file__), validator_path, observer_path)}}
        for name, obj in (("summary.json", summary), ("provenance.json", provenance)):
            (tmp / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                                    encoding="utf-8")
        with (tmp / "frames.jsonl").open("x", encoding="utf-8") as stream:
            for record in records:
                stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
        products = ("frames.jsonl", "provenance.json", "summary.json")
        (tmp / "SHA256SUMS").write_text("".join(sha((tmp / n).read_bytes()) + "  " + n + "\n" for n in products),
                                        encoding="ascii")
        out.mkdir()
        for name in (*products, "SHA256SUMS"):
            (tmp / name).rename(out / name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("return_dir", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    readback(args.return_dir, args.out)
    print("B2_U_LOCAL_READBACK_COMPLETE JOB=368758 NATIVE=234 OBSERVED=201 DEVELOPMENT_ONLY")
