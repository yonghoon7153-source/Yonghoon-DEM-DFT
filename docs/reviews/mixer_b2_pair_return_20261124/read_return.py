"""Verify B2 deployment identity and run the frozen observer on the accepted local C return."""
import argparse
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import runpy
import subprocess
import sys
import tarfile
import tempfile


def check(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_arm(folder, role, rules):
    is_c = role == "C"
    case = "PRECAL_R1_B2_" + role
    job = "369734" if is_c else "368758"
    pin = rules["C_PIN"] if is_c else "f9c8ee5a2cc590ceb70766d144e82ad571942535"
    r = json.loads((folder/"return.json").read_bytes())
    if is_c:
        rules["receipt_fields"](r)
    check(r["case"] == case and r["job_id"] == r["job_end_id"] == r["scheduler"]["job_id"] == job
          and r["role"] == role and r["release_pin"] == pin, "arm or job identity")
    check(r["scheduler"]["state"] == "COMPLETED" and r["scheduler"]["exit_code"] == "0:0"
          and type(r["runner_rc"]) is int and r["runner_rc"] == 0 and r["w9"] == "LIVE_TERMINAL_MATCH"
          and r["return_ready"] is r["exact_frame_names"] is r["post_runtime_matches"] is True
          and r["post_runtime_error"] is None and r["frame_count"] == 234, "terminal return or W9")
    names = ["b2_full_result.tar.gz", "b2_report.tar.gz"]
    hashes = {n:digest(folder/n) for n in names}
    lines = (folder/"SHA256SUMS").read_text("ascii").splitlines()
    check(len(lines) == 2 and {f"{v}  {n}" for n,v in hashes.items()} == set(lines)
          and hashes == r["archive_hashes"], "return manifest")
    expected_full = ("9cb0f3986e2dad6be0a0ca328929bb7ae858a97037249fd0ac510c348c44e0ce" if is_c else
                     "84d3cf8a0bf3e561622c4b78014690b2a2553b70bd1262512239cf82ed756c8e")
    check(hashes[names[0]] == expected_full, "specific return bytes")
    with tarfile.open(folder/names[1], "r:gz") as tar:
        check(len(tar.getnames()) == len(set(tar.getnames())), "duplicate report member")
        def raw(name):
            m = tar.getmember(name)
            check(m.isfile() and m.size <= 16*1024**2, "report member")
            return tar.extractfile(m).read()
        def doc(name):
            return json.loads(raw(name))
        collect = "evidence/" + r["directory"]
        check(doc(collect+".json") == {k:v for k,v in r.items() if k not in {"directory","archive_hashes"}},
              "embedded and external receipts disagree")
        authority = doc("control/pair_authority.json")
        author = doc("evidence/author_arm.json")
        action = "GO_B2_C_PARALLEL_ONCE" if is_c else "GO_B2_U_ONCE"
        check(doc("control/pair_pin.json")["commit"] == authority["release_pin"] == author["pin"] == pin
              and authority["allowed_to_submit"] == [case] and author["case"] == case
              and author["token"] == authority["author_action"] == action, "launch identity")
        check(hashlib.sha256(raw("B_manifest.json")).hexdigest() == authority["asset_manifest"] ==
              "088460cc6a71db4fcc0b6fd326fb89ae629767a2ded45846952640ca44ac0ee0", "asset manifest")
        if is_c:
            check(hashlib.sha256(raw("control/b2_u_submission.json")).hexdigest() == authority["previous"]["sha256"]
                  and doc("control/b2_u_submission.json")["job_id"] == "368758", "C peer acknowledgement")
        s = doc("admission/"+case+".submission.json")
        check(s["case"] == case and s["state"] == "SUBMITTED" and str(s["job_id"]) == job, "submission")
        pre = doc("evidence/runtime_pre/runtime.json")
        post = doc(collect+"_post/runtime.json")
        check(pre["matches"] is post["matches"] is True and not (pre["mismatches"] or post["mismatches"])
              and all(pre[k] == post[k] and pre[k] for k in ("linked", "packages")), "W9 runtime binding")
        ts = [pre["collected_unix"], r["job_end_unix"], r["post_start_unix"], post["collected_unix"], r["post_finished_unix"]]
        check(all(math.isfinite(t) for t in ts) and ts == sorted(ts), "W9 event order")
    return r


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("frozen", "registered", "u_return", "u_observer", "c_return", "out"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    rules = runpy.run_path(str(args.registered))
    spec = importlib.util.spec_from_file_location("frozen_readback", args.frozen/"readback.py")
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    base.verify_packet(args.frozen)
    check(digest(args.u_observer) == rules["U_SHA"], "U observer")
    u = json.loads(args.u_observer.read_bytes())
    for arm,path in (("U",args.u_return),("C",args.c_return)):
        receipt = verify_arm(path, arm, rules)
        print(f"{arm}_ARCHIVES_AND_W9_OK", flush=True)
    modules = {p.name:digest(p) for p in (args.frozen/"scripts").glob("*.py")}
    check(len(modules) == 9 and modules == u["source_sha256"], "pre-observation source bytes")
    ref = u["e0_frame"]
    check(digest(args.frozen/"E0"/"post"/f"mix_{ref['step']}.liggghts") == ref["sha256"], "E0 native reference")
    case = base.CASE = rules["CASE"]
    args.out.mkdir(exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="b2_pair_") as scratch:
        staged = Path(scratch)/case
        staged.mkdir()
        full = args.c_return/"b2_full_result.tar.gz"
        stamp = full.stat()
        with gzip.open(full,"rb") as f, tarfile.open(fileobj=f, mode="r|",bufsize=1024**2) as tar:
            check(base.stage(tar, staged) == 234, "native listing")
        check((stamp.st_size,stamp.st_mtime_ns) == (full.stat().st_size,full.stat().st_mtime_ns), "archive changed")
        check(digest(staged/"in.mixer") == rules["C_DECK"] and digest(staged/"deck_meta.json") == rules["C_META"], "native C deck")
        end = json.loads((staged/"job_end.json").read_bytes())
        check(str(end["job_id"]) == receipt["job_id"] and type(end["returncode"]) is int and end["returncode"] == 0
              and end["end_unix"] == receipt["job_end_unix"], "native C stop")
        print("C_NATIVE_234_DECK_AND_E0_OK", flush=True)
        output = args.out/"c_observer.json"
        with output.open("xb") as stream:
            subprocess.run([sys.executable,"-I","-X","utf8","-B",str(args.frozen/"scripts/mixer_precal_observe.py"),
                "--case",case,"--run",str(staged),"--reference",str(args.frozen/"E0")],stdout=stream,check=True)
        subprocess.run([sys.executable,"-I","-X","utf8","-B",str(args.registered),str(args.u_observer),
                        str(output),str(args.c_return/"return.json"),str(args.out/"paired_exact.json")],check=True)
    print("FIXED_WINDOW_PAIR_COMPLETE",flush=True)


if __name__ == "__main__":
    main()
