"""Re-use the frozen N0/B1 observer, frame window and E0 reference on the B2-U return."""
import argparse
import gzip
import importlib.util
import json
import math
from pathlib import Path
import runpy
import subprocess
import sys
import tarfile
import tempfile


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("frozen", type=Path)
    p.add_argument("b1_observation", type=Path)
    p.add_argument("b2_return", type=Path)
    p.add_argument("out", type=Path)
    args = p.parse_args()
    case, job = "PRECAL_R1_B2_U", "368758"
    reader = runpy.run_path(str(Path(__file__).with_name("read_b2_u.py")))
    spec = importlib.util.spec_from_file_location("b1_library", args.frozen / "readback.py")
    b1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b1)
    b1.verify_packet(args.frozen)
    b1.CASE = case
    ret = json.loads((args.b2_return / "return.json").read_bytes())
    runtime = reader["inspect_report"](args.b2_return / "b2_report.tar.gz", ret)
    hashes = reader["EXPECTED"]
    b1.require(ret["archive_hashes"] == hashes, "archive identities")
    args.out.mkdir(exist_ok=False)
    b1raw = json.loads(args.b1_observation.read_bytes())
    b1.require(b1raw["case"] == "PRECAL_R1_B1_U" and b1raw["job_id"] == "368139", "B1-U identity")
    f8_hashes = {f.name: reader["sha"](f.read_bytes()) for f in (args.frozen / "scripts").glob("*.py")}
    b1.require(b1raw["source_sha256"] == f8_hashes and len(f8_hashes) == 9, "frozen sources")
    with tempfile.TemporaryDirectory(prefix="b2_frozen_readback_") as scratch:
        dest = Path(scratch) / case
        dest.mkdir()
        for name, digest in hashes.items():
            with (args.b2_return / name).open("rb") as f:
                b1.require(b1.hash_file(f) == digest, "archive checksum differs")
                if name == "b2_full_result.tar.gz":
                    f.seek(0)
                    with gzip.GzipFile(fileobj=f) as dec, tarfile.open(fileobj=dec, mode="r|", bufsize=1024**2) as tar:
                        b1.require(b1.stage(tar, dest) == 234, "dump listing")
        b1.require(reader["sha"]((dest / "in.mixer").read_bytes()) == reader["DECK_SHA"]
                   and reader["sha"]((dest / "deck_meta.json").read_bytes()) == reader["META_SHA"], "B2-U input")
        end = json.loads((dest / "job_end.json").read_bytes())
        b1.require(end["job_id"] == job and end["returncode"] == 0, "embedded job")
        proc = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(args.frozen / "scripts/mixer_precal_observe.py"),
                               "--case", case, "--run", str(dest), "--reference", str(args.frozen / "E0")], capture_output=True)
        result = json.loads(proc.stdout)
        if proc.returncode or result["status"] != "OK":
            (args.out / "reported_failure.json").write_text(json.dumps({"status": result["status"],
                      "rc": proc.returncode, "reasons": result.get("reasons")}, indent=2))
            raise SystemExit("Frozen observer reported incomplete")
        prov = result["provenance"]
        frames = [{k: v[k] for k in ("step", "sha256")} for v in prov["frames"]]
        b1.require(len(frames) == 101 and [v["step"] for v in frames] == [v["step"] for v in b1raw["frames"]]
                   and {f"post/mix_{v['step']}.liggghts" for v in frames} == b1.SELECTED, "B1 window identity")
        b1.require(len(prov["reference_frames"]) == 1 and
                   {k: prov["reference_frames"][0][k] for k in ("step", "sha256")} == b1raw["e0_frame"],
                   "E0 reference differs")
        b1.require({Path(v["path"]).name: v["sha256"] for v in prov["module_sha256"].values()} == f8_hashes,
                   "B2 observer bytes differ")
        grids = []
        for g1, g2 in zip(b1raw["mixing"]["grids"], result["mixing"]["grids"], strict=True):
            b1.require(g1["grid"] == g2["grid"] and math.isclose(g1["SR"], g2["SR"], rel_tol=1e-12, abs_tol=1e-14),
                       "Grid or E0 variance differs")
            grids.append({"grid": g1["grid"], "E0_SR": g1["SR"],
                          "B1_U_M_mean": g1["M_mean"], "B1_U_frame_SD": g1["M_sd"],
                          "B2_U_M_mean": g2["M_mean"], "B2_U_frame_SD": g2["M_sd"],
                          "B2_minus_B1_M": g2["M_mean"] - g1["M_mean"],
                          "B1_U_S0": g1["S0"], "B2_U_S0": g2["S0"]})
        obs = {k: result[k] for k in ("contact", "mixing", "counts", "reference_counts")}
        obs.update(case=case, job=job, frames=frames, source_sha256=f8_hashes, e0_frame=b1raw["e0_frame"])
        observ = args.out / "b2_u_observer.json"
        observ.write_text(json.dumps(obs, indent=2, allow_nan=False, ensure_ascii=False) + "\n", encoding="utf8")
        compact = dict(label="DEVELOPMENT_DATA_ONLY", jobs=["368139",job], method="M=(S0-S)/(S0-SR)",
                       window_indices=list(range(134,234)), t0_index=34, grids=grids,
                       frame_sd_scope="within-run variation, one seed per case", w9=runtime["w9"],
                       source_sha256=f8_hashes, archives=hashes,
                       b1_u_observer_sha256=reader["sha"](args.b1_observation.read_bytes()),
                       b2_u_observer_sha256=reader["sha"](observ.read_bytes()), e0_frame=b1raw["e0_frame"])
        (args.out / "comparison.json").write_text(json.dumps(compact, indent=2, allow_nan=False) + "\n", encoding="utf8")
        print(json.dumps(grids))


if __name__ == "__main__":
    main()
