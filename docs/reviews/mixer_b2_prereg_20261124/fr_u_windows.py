"""Observe an existing B2-U return. Read 4 equispaced 5-frame clips for flight witnesses."""
import argparse
import csv
import gzip
import hashlib
import io
import itertools
import json
import tarfile
from pathlib import Path

import numpy as np

CASE = "PRECAL_R1_B2_U"
R = .01258325
HALF_LENGTH = .00251665
STRIDE = 32976
DT = 2.373e-7 * STRIDE
G = np.array([0., 0., -9.81])
CENTERS = (146,171,196,221)


def summaries(directory, records, dest):
    data = {frame["frame_index"]:frame for frame in records}
    rows = []
    for i in range(4):
        a=134+25*i
        window=[data[j] for j in range(a,a+25)]
        def median(key):
            return float(np.median([f[key] for f in window if f.get(key) is not None]))
        # Existing positive-surface velocity observable, not a new motion-type threshold.
        valid=[f for f in window if f["delta_over_R"] is not None]
        rows.append(dict(quarter=i+1,first=a,last=a+24,angles=len(window),valid_layer=len(valid),
                         theta_deg=median("theta_deg"),delta_R=median("delta_over_R"),
                         surface_rms_R=median("surface_rms_over_R")))
    with (dest/"fr_u_quarters.csv").open("x",newline="",encoding="ascii") as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    return rows


def clear(table, candidate):
    """All sphere neighbors, cylinder and endcaps for the small witness set."""
    from scipy.spatial import cKDTree
    xyz=table[:,1:4];r=table[:,7]
    tree=cKDTree(xyz)
    near=tree.query_ball_point(xyz[candidate], r[candidate]+r.max())
    open_mask=np.ones(len(candidate),dtype=bool)
    for k,(idx,others) in enumerate(zip(candidate,near,strict=True)):
        others=np.asarray(others,dtype=int)
        others=others[others!=idx]
        if len(others):
            open_mask[k]=bool(np.all(np.linalg.norm(xyz[idx]-xyz[others],axis=1)>r[idx]+r[others]))
    return open_mask & (np.linalg.norm(xyz[candidate,1:],axis=1)+r[candidate]<R) & (np.abs(xyz[candidate,0])+r[candidate]<HALF_LENGTH)


def witness(clip):
    a,b,c,d,e=clip
    for f in clip[1:]:
        if not np.array_equal(f[:,0],a[:,0]) or not np.array_equal(f[:,7],a[:,7]):raise ValueError("ID/radius changed")
    def ballistic(f,h,tol):
        dv=h[:,4:7]-f[:,4:7]-DT*G
        dp=h[:,1:4]-f[:,1:4]-DT*f[:,4:7]-.5*DT**2*G
        return (np.linalg.norm(dv,axis=1)<=tol*9.81*DT) & (np.linalg.norm(dp,axis=1)<=tol*.5*9.81*DT**2)
    # Two consecutive saved intervals, within tolerance of gravity for both position and velocity.
    choices={}
    for tol in (.01,.05,.10):
        ok=ballistic(b,c,tol)&ballistic(c,d,tol)
        choices[tol]=ok
    ids=np.flatnonzero(choices[.10])
    result={"kinematic_ids":len(ids),"all_particles":len(a)}
    if len(ids):
        isclear=[clear(f,ids) for f in clip]
        airborne=isclear[1]&isclear[2]&isclear[3]
        contact_to_contact=(~isclear[0])&(~isclear[4])
    else:
        airborne=contact_to_contact=np.zeros(0,dtype=bool)
    for tol,eyes in choices.items():
        selected=eyes[ids]&airborne
        result[f"clear_three_at_{tol}"]=int(selected.sum())
        result[f"contact_before_and_after_at_{tol}"]=int((selected&contact_to_contact).sum())
    return result


def sample(archive,prov,dest):
    ref=json.loads(prov.read_bytes())
    assert (ref["case"],str(ref["job_id"]))==(CASE,"368758")
    wanted={n for center in CENTERS for n in range(center-2,center+3)}
    expected={int(v["step"])//STRIDE:v["sha256"] for v in ref["observed_steps_sha256"]}
    frames={};results={}
    with gzip.open(archive,"rb") as stream,tarfile.open(fileobj=stream,mode="r|",bufsize=2**20) as tar:
        for m in tar:
            if not m.isfile() or not m.name.startswith(CASE+"/post/mix_"): continue
            step=int(m.name.rsplit("_",1)[1].split(".")[0]); index=step//STRIDE
            if index not in wanted: continue
            raw=tar.extractfile(m).read()
            assert hashlib.sha256(raw).hexdigest()==expected[index]
            src=io.BytesIO(raw); head=[src.readline().strip() for _ in range(9)]
            assert int(head[1])==index*STRIDE and head[8]==b"ITEM: ATOMS id type x y z vx vy vz fx fy fz radius"
            values=np.loadtxt(src,usecols=(0,2,3,4,5,6,7,11)); assert values.shape==(int(head[3]),8)
            values=values[np.argsort(values[:,0])]
            frames[index]=values
            for n in CENTERS:
                if n not in results and all(j in frames for j in range(n-2,n+3)):
                    results[n]=witness([frames.pop(j) for j in range(n-2,n+3)])
                    print(n,results[n],flush=True)
            if len(results)==len(CENTERS): break
    assert sorted(results)==list(CENTERS)
    output=dict(archive_sha256_by_prior_verified_receipt=ref["archives"]["b2_full_result.tar.gz"],job="368758",case=CASE,
                interval_s=DT,clip_five_centers=list(CENTERS),input_frame_sha256={n:expected[n] for n in sorted(wanted)},
                counts_by_clip=results)
    with (dest/"fr_u_flight.json").open("x") as f:json.dump(output,f,indent=2)


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("mode",choices=("quarters","clips"));p.add_argument("directory",type=Path);p.add_argument("source",type=Path);p.add_argument("dest",type=Path);a=p.parse_args()
    if a.mode=="quarters":
        r=[json.loads(s) for s in a.source.read_text().splitlines()]
        print(summaries(a.directory,r,a.dest))
    else:sample(a.directory/"b2_full_result.tar.gz",a.source,a.dest)
