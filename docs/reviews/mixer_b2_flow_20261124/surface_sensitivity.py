"""Whole second-turn post-hoc sensitivity, using the same frame 134 dense-edge rule."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import runpy
import tarfile
from math import atan, degrees
from pathlib import Path

import numpy as np


def stats(values):
    q=np.quantile(values,[0,.25,.5,.75,1])
    return dict(zip(("min","q25","median","q75","max"),map(float,q)))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("archive",type=Path); ap.add_argument("readback",type=Path); ap.add_argument("outdir",type=Path)
    args=ap.parse_args()
    if args.outdir.exists():
        raise ValueError("Use a fresh output folder")
    method=runpy.run_path(str(Path(__file__).with_name("plot_single_frame.py")))
    recs=[json.loads(s) for s in (args.readback/"frames.jsonl").read_text(encoding="utf-8").splitlines()]
    selected={r["step"]:r for r in recs if r["phase"]=="TURN_1_TO_2"}
    if set(selected)!={i*32976 for i in range(134,234)}:
        raise ValueError("Incomplete second-turn frame set")
    provenance=json.loads((args.readback/"provenance.json").read_text(encoding="utf-8"))
    hashes={b["step"]:b["sha256"] for b in provenance["observed_steps_sha256"]}
    rows={}
    with gzip.open(args.archive,"rb") as raw, tarfile.open(fileobj=raw,mode="r|",bufsize=1024**2) as archive:
        for member in archive:
            m=method["PATTERN"].fullmatch(member.name)
            if not m or int(m[1]) not in selected:
                continue
            step=int(m[1]); rec=selected[step]
            if step in rows or not member.isfile() or member.size>256*1024**2:
                raise ValueError("Invalid frame")
            data=archive.extractfile(member).read()
            if hashlib.sha256(data).hexdigest()!=hashes[step] or int(data.split(b"\n",2)[1])!=step:
                raise ValueError("Frame SHA/step mismatch")
            atoms=np.loadtxt(io.BytesIO(data),skiprows=9,comments=None)
            if len(atoms)!=rec["atom_count"]:
                raise ValueError("Wrong number of atoms")
            _,cols=method["lines"](atoms)
            m99,b99=method["fit"]([(c[0],c[2]) for c in cols])
            t99=degrees(atan(m99))
            if abs(t99-rec["theta_signed_deg"])>1e-9:
                raise ValueError("Primary fit changed")
            dense=[(c[0],c[4]) for c in cols if c[4] is not None]
            # Frame 134 fitted every available dense column. Preserve the identical rule.
            # Report the primary fit's stricter horizontal-coverage check separately.
            ok=len(dense)>=2
            wide=len(dense)>=10 and dense[0][0]<=-.35 and dense[-1][0]>=.35
            td=degrees(atan(method["fit"](dense)[0])) if ok else None
            rows[step]=dict(step=step,frame=rec["frame_index"],turns=rec["turns_since_rotation"],
                            primary_columns=len(cols),occupied_columns=len(dense),
                            occupied_min_y_R=dense[0][0] if dense else None,
                            occupied_max_y_R=dense[-1][0] if dense else None,
                            status="OK" if ok else "INSUFFICIENT_POINTS",
                            dense_support_matches_primary=wide,
                            primary_signed_deg=t99,dense_signed_deg=td,
                            abs_angle_difference_deg=abs(td)-abs(t99) if ok else None,
                            signed_angle_difference_deg=td-t99 if ok else None)
            if len(rows)==100:
                break
    if set(rows)!=set(selected):
        raise ValueError("Missing second-turn frames")
    ordered=[rows[k] for k in sorted(rows)]
    report=summary(ordered)
    serialized=json.dumps(report,indent=2,allow_nan=False)+"\n"
    args.outdir.mkdir(parents=True)
    with (args.outdir/"second_turn_surface_sensitivity.csv").open("w",newline="",encoding="utf-8") as fp:
        writer=csv.DictWriter(fp,fieldnames=ordered[0]); writer.writeheader();writer.writerows(ordered)
    (args.outdir/"second_turn_surface_sensitivity.json").write_text(serialized,encoding="utf-8")
    print(serialized)


def summary(ordered):
    valid=[r for r in ordered if r["status"]=="OK"]
    if not valid:
        raise ValueError("No valid occupied-bed fits")
    return dict(independent_seeds=1,frames=len(ordered),valid=len(valid),
                primary_abs_all=stats([abs(r["primary_signed_deg"]) for r in ordered]),
                primary_abs_paired=stats([abs(r["primary_signed_deg"]) for r in valid]),
                dense_abs_paired=stats([abs(r["dense_signed_deg"]) for r in valid]),
                paired_abs_dense_minus_abs_primary=stats([r["abs_angle_difference_deg"] for r in valid]),
                paired_signed_dense_minus_signed_primary=stats([r["signed_angle_difference_deg"] for r in valid]),
                dense_steeper_count=sum(r["abs_angle_difference_deg"]>0 for r in valid),
                dense_with_primary_width=sum(bool(r["dense_support_matches_primary"]) for r in valid),
                dense_columns_across_frames=stats([r["occupied_columns"] for r in valid]),
                signed_difference_over_5deg_descriptive_count=sum(abs(r["signed_angle_difference_deg"])>5 for r in valid),
                quarter_valid_counts=[sum(1 for r in valid if i<=(r["turns"]-1)*4<i+1) for i in range(4)],
                density_rule=dict(height_bin_R=.035,minimum_count=3,minimum_consecutive_bins=3,
                                  column_weight="sum_r_squared",nonempty_reference_percentile=90,
                                  threshold_fraction=.15,minimum_points_to_fit=2,
                                  descriptive_width_check="at least 10 columns spanning +/-0.35 R"),
                method_status="POST_HOC_SURFACE_DEFINITION_SENSITIVITY")


if __name__=="__main__":
    main()
