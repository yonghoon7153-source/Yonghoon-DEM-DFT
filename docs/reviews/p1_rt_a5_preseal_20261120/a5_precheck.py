"""Re-evaluate the fixed A3 prerequisite at its original site. No engine or writes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import types

LMP = "ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f"
READBACK_PIN = "851bfd571d4da9f0848e3f7040a1f05c59e4ef0c"
ANCHORS = {
    "a3_inputs.json": "ef1f8668c4006e813bb4c39788e241cad250dc6583f1afb4ba8835b0531d9211",
    "a3_return.json": "cd0cd6312bb7ee7fe792551206afdadbcdd5b3abb93b96d3028746dc815b3b74",
    "a3_readback.py": "705738f8134ecc2a299b774c7dd8cc5986a07eb9d8c78ccc2c2c13f3cad34e97",
    "a3_corrected_reader.py": "71f0322285ac515919b71d9a9eb0ad0cc962f60381db3bacecc904ac10e91bea",
    "a4_continuity.json": "c4910d33898851665436a869609573fbe21ab8362d109574a75b093a29e53ff3",
    "a4_receipt.json": "8ccafc8f6c9bddf4c94b4d3c6e555299d5641099f0be20e380434beffed4f17f",
}

def require(value, reason):
    if not value:
        raise ValueError(reason)

def fixed_files(kit):
    blobs = {}
    for name, expected in ANCHORS.items():
        raw = (kit / name).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, "changed candidate input: " + name)
        blobs[name] = raw
    module = types.ModuleType("readback_pinned")
    exec(compile(blobs["a3_readback.py"], "<fixed-original-path-readback>", "exec"), module.__dict__)
    return {"evidence":json.loads(blobs["a3_inputs.json"]), "receipt":json.loads(blobs["a3_return.json"]),
            "reader":blobs["a3_corrected_reader.py"], "readback":module,
            "a4":json.loads(blobs["a4_continuity.json"]), "a4_receipt":json.loads(blobs["a4_receipt.json"])}

def check_writer_inputs(folder, receipt):
    names = {"reference.dump":"contact_3200000.liggghts", "writer.log":"output_ps_7_3_r45_r8_220537.out",
             "writer.deck":"input_ps_7_3_r45_r8.liggghts"}
    expected = receipt["original_inputs_sha256_matched_to_historical_pins"]
    for key, name in names.items():
        h = hashlib.sha256()
        with (folder/name).open("rb") as stream:
            for chunk in iter(lambda:stream.read(1024**2), b""):
                h.update(chunk)
        require(h.hexdigest() == expected[key],"current 7:3 input differs from A4: "+key)

def checked_manifest(site, expected, binary):
    work = site / "work"
    raw = (work / "fixture/run_manifest.txt").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == expected["files"]["fixture/run_manifest.txt"],
            "fixture manifest differs from 367546")
    fields = {}
    for line in raw.decode("utf-8").splitlines():
        key, sep, value = line.partition("=")
        if key in ("np","job_id","mode","end","job_dir","kit","sums_sha256","lmp_sha256"):
            require(sep and key not in fields and value, "ambiguous or empty fixture manifest field: " + key)
            fields[key] = value
    for key, value in {"np":"6","job_id":expected["job"],"mode":"rt_grammar","lmp_sha256":binary,
                       "sums_sha256":expected["files"]["kit/RT_CANDIDATE_SHA256SUMS"]}.items():
        require(fields.get(key) == value, "historical manifest mismatch: " + key)
    require(fields.get("end"), "missing fixture end")
    for name, folder in (("job_dir","fixture"),("kit","kit")):
        recorded = Path(fields.get(name,""))
        require(recorded.is_absolute() and recorded.resolve(strict=True) == work/folder,
                "fixture must remain at its recorded " + name)

def check_site(site, binary, fixed):
    require(binary == LMP, "current binary differs from recorded fixture binary")
    site = Path(site).resolve(strict=True)
    expected = fixed["evidence"]
    checked_manifest(site, expected, binary)
    fresh = fixed["readback"].inspect(site, expected, fixed["reader"], READBACK_PIN)
    require(fresh == fixed["receipt"], "current original-path reread does not match the accepted receipt")
    require(fresh["status"] == "PASS" and fresh["reader_rc"] == 0 and
            fresh["numeric_status"] == fresh["binding_status"] == "PASS" and
            len(fresh["checks"]) == 20 and all(v is True for v in fresh["checks"].values()),
            "fixture checks incomplete")
    a4 = fixed["a4"]
    require(a4["result"]["status"] == "PASS" and a4["historical_job"] == "323957",
            "historical 7:3 A4 record")
    return {"ok":True,"scope":"ps_7_3_r45 RJ preflight only","operational_go":False,
            "job":expected["job"],"raw_files_verified_before_after":fresh["inputs_verified_before_after"],
            "checks_passed":len(fresh["checks"]),"archived_job_result":"FAILED 2:0",
            "reader_sha256":fresh["reader_sha256"],"receipt_sha256":ANCHORS["a3_return.json"],
            "historical_7_3_r_sha256":ANCHORS["a4_continuity.json"]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original_site",type=Path)
    parser.add_argument("--lmp-sha",required=True)
    parser.add_argument("--bed-input",type=Path,required=True)
    args = parser.parse_args()
    try:
        fixed = fixed_files(Path(__file__).resolve().parent)
        result = check_site(args.original_site, args.lmp_sha, fixed)
        check_writer_inputs(args.bed_input, fixed["a4_receipt"])
        result["current_writer_inputs_verified"] = 3
    except (OSError,ValueError,KeyError,TypeError,RuntimeError) as error:
        # The operator gets the failing condition; the kit never publishes a verdict.
        print(json.dumps({"ok":False,"operational_go":False,"error":str(error)},ensure_ascii=True))
        return 2
    print(json.dumps(result,allow_nan=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
