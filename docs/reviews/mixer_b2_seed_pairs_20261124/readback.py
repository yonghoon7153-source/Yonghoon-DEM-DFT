"""WSL contact-only readback of verified local returns; compute per-seed paired contrasts."""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import runpy
import shutil
import statistics
import tarfile
import tempfile
import types

ROOT=Path(__file__).resolve().parent
STEPS=[n*32976 for n in range(134,234)]
METRICS={"se_frac_in_clusters":"s1_se_clusters","se_attached_any_frac":"s2_am_se_attach"}

def need(ok,label):
    if not ok:raise ValueError(label)
def read(p):return json.loads(p.read_bytes())
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()

def verify_return(path,arm,campaign):
    r=read(path/"return.json")
    group=arm[:2]
    case="MIXER_B2_"+arm
    need(r["case"]==case and r["role"]==arm and r["ratio"]==campaign["arms"][arm]["ratio"] and
         r["release_pin"]==campaign["pin"] and r["job_id"]==r["scheduler"]["job_id"] and
         re.fullmatch(r"[1-9]\d*",r["job_id"]) and re.fullmatch(r"collection_\w+",r["directory"]),"return identity")
    hashes={n:s for s,n in (line.split("  ") for line in (path/"SHA256SUMS").read_text().splitlines())}
    need(hashes==r["archive_hashes"] and set(hashes)=={"b2_full_result.tar.gz","b2_report.tar.gz"},"archive manifest")
    for n,s in hashes.items():need(sha(path/n)==s,"archive mismatch "+n)
    with tarfile.open(path/"b2_report.tar.gz") as t:
        def get(n):
            mem=[m for m in t.getmembers() if m.name==n]
            need(len(mem)==1 and mem[0].isfile(),"missing or ambiguous report item")
            return t.extractfile(mem[0]).read()
        base="arms/"+arm+"/"
        need(get("release.json")== (ROOT/group/"release.json").read_bytes(),"stale wave release")
        need(json.loads(get("authorization.json"))["seed"]==campaign["seeds"][group],"seed approval")
        embedded=json.loads(get(base+"evidence/"+r["directory"]+".json"))
        need(embedded=={k:v for k,v in r.items() if k not in ("directory","archive_hashes")},"terminal receipt binding")
        if r["disposition"]!="COMPLETE": return r
        need(r["return_ready"] is r["post_runtime_matches"] is r["exact_frame_names"] is True
             and r["job_end_id"]==r["job_id"] and type(r["runner_rc"]) is int and r["runner_rc"]==0
             and r["frame_count"]==234 and r["scheduler"]["state"]=="COMPLETED" and r["scheduler"]["exit_code"]=="0:0"
             and r["w9"]=="LIVE_TERMINAL_MATCH" and r["post_runtime_error"] is None,"incomplete normal return")
        need(json.loads(get(base+"submission.json"))["job_id"]==r["job_id"],"submitted job differs")
    return r

def extract(full,dest,arm,jid):
    case="MIXER_B2_"+arm
    selected={case+"/post/mix_%d.liggghts"%s for s in [34*32976,*STEPS]}
    names={"in.mixer","deck_meta.json","log.liggghts","job_end.json","job_start.json","Drum.stl","Front.stl","Back.stl"}
    wanted=selected|{case+"/"+n for n in names}
    seen=set()
    frame_names=set()
    with tarfile.open(full,"r|gz") as t:
        for m in t:
            n=m.name
            need(m.isfile() and n.startswith(case+"/") and ".." not in n.split("/") and n not in seen,"invalid full return")
            seen.add(n)
            if n.startswith(case+"/post/mix_"):frame_names.add(n)
            if n in wanted or n==case+"/n_expected":
                out=dest/n
                out.parent.mkdir(parents=True,exist_ok=True)
                with t.extractfile(m) as src,out.open("xb") as dst:shutil.copyfileobj(src,dst)
    need(wanted<=seen and frame_names=={case+"/post/mix_%d.liggghts"%(32976*i) for i in range(1,235)},"full dump identity")
    run=dest/case
    for n in ("in.mixer","deck_meta.json","Drum.stl","Front.stl","Back.stl"):
        need(sha(run/n)==sha(ROOT/arm[:2]/"assets"/arm/n),"dump input mismatch "+n)
    start,end=read(run/"job_start.json"),read(run/"job_end.json")
    need(start["job_id"]==end["job_id"]==jid and start["case"]==case and
         type(end["returncode"]) is int and end["returncode"]==0,"full job identity")
    return run

def qualifier(obs,arm,manifest):
    case="MIXER_B2_"+arm
    recipe=runpy.run_path(str(ROOT/"seed_decks.py"))
    entry=manifest["arms"][arm]
    # The immutable generator is already included in the bound observer registry.
    gen=vars(obs["_REGISTRY"]["make_mixer_deck"])
    def bind(cid,deck,meta):
        need(cid==case,"unregistered case")
        refid="PRECAL_R1_B2_"+arm[-1]
        ref=obs["preparation"].prepare_case(refid)
        expected,m,pair=recipe["generate"](gen,ref["deck"],ref["meta"],arm)
        need(deck==expected and m==meta and tuple(pair)==(entry["seed"],entry["secondary_seed"]),"wrong seed or printed B2 recipe")
        geom=obs["validate_case"](refid,ref["deck"],ref["meta"])
        return dict(geom,case_id=cid,seed=pair[0],frame_pm=dict(geom["frame_pm"],seed=pair[0]))
    return bind

def observe(run,arm,manifest):
    obs=runpy.run_path(str(ROOT/"observer/mixer_precal_observe.py"))
    need(obs["_BOOT_ERROR"] is None,"observer dependencies")
    case="MIXER_B2_"+arm
    # Reuse the complete native log, frame and ID qualification; bind only the four additional case names.
    native=obs["_load"]
    loader=types.FunctionType(native.__code__,dict(native.__globals__,validate_case=qualifier(obs,arm,manifest)))
    sources,listings,optional={},{},{}
    obs["_verify_bound"]()
    data=loader(case,run,sources,listings,optional)
    need(data["frame_plan"]["bin_steps"]==STEPS and data["frame_plan"]["t0_step"]==34*32976,"observation window")
    obs["_verify_sources"](sources,listings,optional)
    rows=[dict(step=step,**obs["contact"].frame_quantities(arr,data["binding"]["frame_pm"]))
          for step,arr in zip(STEPS,data["arrays"][1:])]
    native_bin=obs["contact"].bin_summary(rows,STEPS)
    need(native_bin["status"]=="OK" and native_bin["n"]==100,"bin failure")
    obs["_verify_sources"](sources,listings,optional)
    return obs["_clean"](dict(steps=STEPS,frames=rows,frame_hashes=[(f["step"],f["sha256"]) for f in data["frames"]],
                observed_counts=data["counts"],observer=obs["_BOUND_DIGESTS"]))

def paired(u,c):
    need(u["steps"]==c["steps"]==STEPS and u["observer"]==c["observer"],"pair provenance")
    out={}
    for key,g in METRICS.items():
        deltas=[];lo=[];hi=[];u_values=[];c_values=[]
        for step,a,b in zip(STEPS,u["frames"],c["frames"]):
            need(a["step"]==b["step"]==step,"unmatched phase")
            def frac(row):
                n=row["n"]["SE"];x=row[g][key];i=round(x*n)
                need(n>0 and 0<=x<=1 and i/n==x,"native integer count")
                return Fraction(i,n)
            au,ac=frac(a),frac(b)
            u_values.append(au)
            c_values.append(ac)
            deltas.append(ac-au)
            lo.append(b["resolution"]["lo"][key]-a["resolution"]["hi"][key])
            hi.append(b["resolution"]["hi"][key]-a["resolution"]["lo"][key])
        need(len(deltas)==100,"missing frame")
        exact=sum(deltas)/len(deltas)
        out[key]=dict(exact_fraction_delta=str(exact),C_minus_U_percentage_points=float(100*exact),
                      sign="zero" if exact==0 else "positive" if exact>0 else "negative",
                      U_percent=float(100*sum(u_values)/len(u_values)),C_percent=float(100*sum(c_values)/len(c_values)),
                      frame_sd_pp=statistics.stdev([float(100*v) for v in deltas]),
                      precision_interval_pp=[statistics.mean(lo)*100,statistics.mean(hi)*100])
    return out

def aggregate(rows):
    if any(r.get("status")!="OK" for r in rows) or len(rows)!=3:return dict(status="NEED_THREE_VALID_SEEDS")
    need([r["seed"] for r in rows]==[32452843,49979687,67867967],"repeated or reordered seeds")
    t=4.302652729696142
    intervals={}
    for key in METRICS:
        values=[float(Fraction(r["metrics"][key]["exact_fraction_delta"])*100) for r in rows]
        mean=statistics.mean(values)
        half=t*statistics.stdev(values)/math.sqrt(3)
        intervals[key]=dict(seed_mean_pp=mean,paired_95pct_t_pp=[mean-half,mean+half])
    both=(intervals["se_frac_in_clusters"]["paired_95pct_t_pp"][1]<=-2 and
          intervals["se_attached_any_frac"]["paired_95pct_t_pp"][0]>=2)
    return dict(status="THREE_SEED_PAIRS",comparison="0.10_to_1.00",df=2,metrics=intervals,both_practical_directions=both)

def save(path,obj):
    with path.open("x",encoding="utf8") as f:json.dump(obj,f,indent=2,allow_nan=False)

def one(root,arm,man):
    folder=root/arm
    receipt=verify_return(folder,arm,man)
    if receipt["disposition"]!="COMPLETE":return receipt["disposition"],None
    # Reverify both archives on every return, cache only the derived observations.
    cache=root/(arm+"_"+receipt["archive_hashes"]["b2_full_result.tar.gz"]+"_"+man["pin"]+".json")
    stamp=cache.with_suffix(".sha256")
    if cache.is_file() and stamp.is_file() and sha(cache)==stamp.read_text().strip():
        return "COMPLETE",read(cache)
    with tempfile.TemporaryDirectory() as scratch:
        run=extract(folder/"b2_full_result.tar.gz",Path(scratch),arm,receipt["job_id"])
        observed=observe(run,arm,man)
    with tempfile.TemporaryDirectory(dir=root) as stage:
        temp=Path(stage)/"cache"
        save(temp,observed)
        signature=Path(stage)/"sha"
        signature.write_text(sha(temp)+"\n")
        temp.replace(cache)
        signature.replace(stamp)
    return "COMPLETE",observed

def main(root,out):
    man=read(ROOT/"campaign.json")
    prior=read(ROOT/"prior_pair.json")
    rows=[dict(seed=prior["seed"],status="OK",metrics=prior["metrics"])]
    for family,seed in man["seeds"].items():
        valid={};states={};reasons={}
        for role in "UC":
            arm=family+role
            folder=root/arm
            if not folder.is_dir():
                states[role]="NOT_RETURNED";continue
            try:
                state,observed=one(root,arm,man)
                states[role]=state
                if observed is not None:valid[role]=observed
            except (ValueError,TypeError,KeyError,OSError,tarfile.TarError,EOFError) as exc:
                states[role]="READBACK_REFUSED"
                reasons[role]=str(exc)
        row=dict(seed=seed,arms=states,reasons=reasons,status="PENDING_OR_TECH_MISSING")
        if set(valid)==set("UC"):row.update(status="OK",metrics=paired(valid["U"],valid["C"]))
        rows.append(row)
    summary=dict(development_only=True,seeds=rows,comparison=aggregate(rows))
    save(out,summary)
    print(json.dumps(summary,ensure_ascii=True,allow_nan=False))
if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("cache",type=Path)
    cli.add_argument("out",type=Path)
    args=cli.parse_args()
    main(args.cache,args.out)
