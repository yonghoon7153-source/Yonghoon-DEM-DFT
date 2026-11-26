"""Reduce a verified ladder arm with the registered observer, retaining native frame hashes."""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import runpy
import tarfile


def check(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(args):
    receipt_raw = args.receipt.read_bytes()
    check(digest(receipt_raw) == args.receipt_sha, "verified receipt identity")
    receipt = json.loads(receipt_raw)
    arm = receipt["role"]
    check(receipt["w9"] == "LIVE_TERMINAL_MATCH" and receipt["runner_rc"] == 0 and
          receipt["stable_id_types_frames"] == 101 and receipt["native_frames_verified"] == 234, "native receipt")
    with args.packet.open("rb") as stream:
        check(hashlib.file_digest(stream,"sha256").hexdigest() == receipt["source_packet_sha256"], "source packet")
    with tarfile.open(args.packet) as packet:
        deck, meta = [packet.extractfile(f"assets/{arm}/{n}").read() for n in ("in.mixer","deck_meta.json")]
    adapter = runpy.run_path(str(args.adapter.resolve()))
    obs = adapter["verified_observer"](args.frozen.resolve())
    check(obs["_BOOT_ERROR"] is None, "observer dependencies")
    geom = adapter["binding"](obs, args.frozen.resolve(), arm, deck, meta)
    check(geom["seed"] == receipt["seed"], "seed differs")
    manifest = {r["step"]:r for r in receipt["full_frame_manifest"]}
    listing = [(s,Path(f"mix_{s}.liggghts")) for s in sorted(manifest)]
    plan = obs["_frozen_plan"](deck, geom, listing)
    base, steps = plan["t0_step"], plan["bin_steps"]
    check(base == 32976*34 and steps == [32976*i for i in range(134,234)], "frame selection")
    keep = set(steps) | {base}
    stem = receipt["case"] + "/"
    rows = {}
    fingerprints = {}
    seen = set()
    required = {"log.liggghts","in.mixer","deck_meta.json"}
    with args.archive.open("rb") as fp:
        check(hashlib.file_digest(fp,"sha256").hexdigest() == receipt["archives_sha256"][args.archive.name], "archive identity")
        fp.seek(0)
        with gzip.GzipFile(fileobj=fp) as gz, tarfile.open(fileobj=gz, mode="r|", bufsize=1024*1024) as tar:
            for m in tar:
                check(m.name.startswith(stem) and m.isfile() and m.name not in seen, "archive name")
                seen.add(m.name)
                name = m.name[len(stem):]
                if name in required:
                    raw = tar.extractfile(m).read()
                    if name == "log.liggghts":
                        obs["_log_contract"](raw, plan["runs"], obs["_deck_log_facts"](deck))
                    else:
                        check(raw == (deck if name == "in.mixer" else meta), "deck does not match packet")
                    required.remove(name)
                if not name.startswith("post/mix_") or not name.endswith(".liggghts"):
                    continue
                step = int(Path(name).stem.removeprefix("mix_"))
                if step not in keep:
                    continue
                raw = tar.extractfile(m).read()
                check(digest(raw) == manifest[step]["sha256"], "frame hash")
                arr = obs["_parse_dump"](raw,step)
                obs["qualify_arrays"]([arr],geom)
                # Canonical ordering permits exact cross-frame ID/type/radius comparison
                # even when the baseline file is stored after some observed frames.
                order = arr["id"].argsort(kind="stable")
                fingerprints[step] = tuple(digest(arr[k][order].tobytes()) for k in ("id","type","radius"))
                if step != base:
                    rows[step] = obs["contact"].frame_quantities(arr,geom["frame_pm"])
    check(not required and set(fingerprints) == keep and len(set(fingerprints.values())) == 1, "frame or ID/type/radius evidence")
    check(set(rows) == set(steps), "window incomplete")
    summary = obs["contact"].bin_summary([rows[s] for s in steps], steps)
    check(summary["status"] == "OK" and summary["n"] == 100, "incomplete readback")
    keys = {"se_frac_in_clusters":"s1_se_clusters","se_attached_any_frac":"s2_am_se_attach"}
    return dict(scope="SINGLE_ARM_DEVELOPMENT_ONLY",role=arm,job=receipt["job_id"],seed=geom["seed"],
        verified_receipt_sha256=args.receipt_sha,source_packet_sha256=receipt["source_packet_sha256"],
        archive_sha256=receipt["archives_sha256"][args.archive.name],observer_manifest_sha256=adapter["MANIFEST"],
        baseline_step=base,frames=[dict(step=s,ordinal=s//32976,sha256=manifest[s]["sha256"],
                                        **{k:float(rows[s][g][k]) for k,g in keys.items()},
                                        resolution={side:{k:float(rows[s]["resolution"][side][k]) for k in keys} for side in ("lo","hi")})
                                    for s in steps],
        mean_fraction={k:summary["mean"][k] for k in keys},
        mean_coordinate_precision={side:{k:summary["mean"][side+"."+k] for k in keys} for side in ("lo","hi")},
        paired_contrast=None)


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for key in ("archive","receipt","packet","adapter","frozen","output"):
        p.add_argument(key,type=Path)
    p.add_argument("receipt_sha")
    args=p.parse_args()
    result=read(args)
    with args.output.open("x",encoding="utf8") as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write("\n")
    print(result["role"],len(result["frames"]),result["mean_fraction"])
