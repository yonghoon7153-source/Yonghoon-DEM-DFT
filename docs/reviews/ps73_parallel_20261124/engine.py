"""Run a frozen deck under one isolated NP6 allocation."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
import parallel as p
import ps73_node as original
import ps73_sequence as sequence

HOME=Path.home()
ROOT=HOME/p.ORIG
OPS=(HOME/p.OPS).resolve()
STATE=HOME/p.OLD/"state"
LEGACY="b3e96718e99fcc6334182079c6b077ab5bff0b9d2d2a9a091fa2cee26e8f6685"
STAGE="c037e44ed202dc4412b467372dce04a0bc9df8928d8b916193142f4c41fc1ac8"

def reserved():
    jobs=STATE/"jobs"
    manual=STATE/"author_stages_1123"
    marker=manual/"before_UT.json"
    expected=dict(action="AUTHOR_REQUESTED_STAGEWISE",before="UT",ub_job=p.UB_JOB,
                  legacy_release=LEGACY,stagewise_sha256=STAGE)
    p.need(p.read(marker)==expected,"existing serial reservation changed")
    for name in ("UT","UC","UVa","UVb","UTc",".ps73_author_steps_1123"):
        target=jobs/name
        p.need(target.is_file() and not target.is_symlink() and target.samefile(marker),"legacy claimed "+name)
    active=p.read(manual/"active.json")
    ack=p.read(jobs/"UB"/"reply.json")
    p.need(active["status"]=="BOUNDARY_RESERVED" and active["before"]=="UT"
           and active["stagewise_sha256"]==STAGE and active["previously_claimed"]=={}
           and ack["job_id"]==p.UB_JOB and ack["arm"]=="UB","UB boundary mismatch")

def reader(kit):
    sys.path.insert(0,str(kit))
    import rt_restore_a5
    p.need(rt_restore_a5.job_restored(ROOT,p.BED,"RJ",kit),"A5 restored certificate refused")
    return rt_restore_a5.legacy_reader(kit)

def inputs(kit,arm):
    bed=ROOT/p.BED
    par=p.read(kit/"unload_params.json")
    files=par["beds"][p.BED]["in_files"]
    for key in ("ckpt","mesh","atom"):
        item=files[key]
        path=bed/"in"/item["file"]
        original.checked(path,item["sha256"])
        p.need(path.stat().st_size==item["size"],"source size mismatch")
    ub=bed/"UB"
    original.checked(ub/"deck.liggghts",p.digest(kit/"decks"/p.BED/"in.U_UB.liggghts"))
    lines=(ub/"run_manifest.txt").read_text(encoding="utf8").splitlines()
    for line in ("job=UB","bed="+p.BED,"np=6","gate=ALLOW","lmp_sha256="+original.LMP_SHA):
        p.need(lines.count(line)==1,"running UB provenance "+line)
    p.need(any(x.startswith("slurm_job="+p.UB_JOB+" slurm_ntasks=6 ") for x in lines),"wrong UB allocation")
    ck=bed/"in"/files["ckpt"]["file"]
    plate=bed/"in"/files["mesh"]["file"]
    ident=dict(source_job="368315",UB_job=p.UB_JOB,restart=p.digest(ck),plate=p.digest(plate),
               base=original.BASE_SHA,restore=original.VERDICT_SHA,kit=original.SUMS_SHA,
               atom=files["atom"]["sha256"],np=6)
    return par,ck,plate,ident

def run_function(kit):
    text=(kit/"run_unload.sh").read_text(encoding="utf8")
    start=text.index("run_deck() {")
    return text[start:text.index("\n}\n",start)+2]

def probe_deck(text):
    split="jump SELF ul_next\n# <<< block start"
    p.need(text.count(split)==1 and "label ul_resumed" in text.split(split)[0],"restart branch not recognized")
    names=("ul_step","ul_k","probe_atoms")
    marker='print "RESTART_PROBE_OK step=%s k=%s atoms=%s"'%tuple("$"+"{"+name+"}" for name in names)
    return text.split(split)[0]+"run 0\nvariable probe_atoms equal atoms\n"+marker+"\n"

def snapshot(src,dest,meta):
    p.need(not dest.exists() and not dest.is_symlink() and not (src/"ul_summary.txt").exists(),
           "existing UB copy or terminal summary")
    dest.parent.mkdir(parents=True,exist_ok=True)
    stage=dest.parent/"UB.copying"
    p.need(not stage.exists(),"unfinished UB copy; review")
    for path in src.rglob("*"):
        p.need(not path.is_symlink() and (path.is_file() or path.is_dir()),"non-regular UB source")
    stage.mkdir()
    subprocess.run(["cp","-R","--reflink=auto",str(src)+"/.",str(stage)],check=True)
    p.need(p.checkpoint(stage)==meta and p.checkpoint(src)==meta,"UB copy checkpoint mismatch")
    for path in src.rglob("*"):
        if path.is_file():
            clone=stage/path.relative_to(src)
            p.need(not path.samefile(clone) and p.digest(path)==p.digest(clone),"UB copy identity")
    stage.rename(dest)

def run_probe(folder,deck,expected,env,state,binary,base,plate,atoms):
    scratch=folder/"restart_probe"
    scratch.mkdir()
    for n in ("post","dump","obs","g2","restart"):
        (scratch/n).mkdir()
    path=scratch/"probe.liggghts"
    path.write_text(probe_deck(deck.read_text(encoding="utf8")),encoding="utf8")
    args=[env["MPIRUN"],*env["MPIRUN_FLAGS"].split(),"-np","6",env["LMP"],"-in",str(path),
          "-log",str(scratch/"log"),"-var","ckpt",str(binary),"-var","plate_stl",str(plate),
          "-var","ul_base",str(base),"-var","ul_state",str(state),"-var","ul_resume","1","-var","out",str(scratch)]
    with (scratch/"screen").open("xb") as f:
        subprocess.run(args,cwd=scratch,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600,check=True)
    out=(scratch/"screen").read_text(errors="replace")
    match=re.findall(r"^RESTART_PROBE_OK step=(\d+) k=(\d+) atoms=(\d+)$",out,re.M)
    p.need(match==[(str(expected["step"]),str(expected["k"]),str(atoms))] and
           re.search(r"Loop time of \S+ on 6 procs",out) and "LIGGGHTS-PUBLIC 3.8.0" in out and
           not re.search(r"^(ERROR|UL_ABORT)",out,re.M),"restart probe refused")
    p.publish(folder/"probe_ok.json",dict(expected,np=6,engine=original.LMP_SHA))

def assess(old,params,d,arm):
    raw=old.arm_verdict(str(d),p.BED,arm,params,root=str(ROOT))
    run=old.read_run(str(d),params)
    if arm=="UC":
        valid=sequence.control_ok(run,params)
        return raw,valid,valid
    summary=run.get("summary") or {}
    marks=[row.get("event") for row in run["events"]]
    ends={"DONE","SEP_INCOMPLETE","LIFT_CAP"}
    if arm=="UT":
        ends.add("RM_STOP")
    valid=(not run["problems"] and not raw.get("resume_tail") and old._valid_rho(raw)
           and summary.get("result") in ends and marks[:1]==["START"] and "GUARD" not in marks
           and all(marks.count(m)==1 for m in ("START","CROSS","RM"))
           and marks.index("CROSS")<marks.index("RM"))
    return raw,bool(valid),None

def worker(arm,folder):
    reserved()
    job=original.allocation(os.environ)
    p.need(folder.resolve()==Path.cwd().resolve() and folder.parent==OPS/"attempts"/arm,"wrong allocation folder")
    for _ in range(60):
        if (folder/"ack.json").is_file():
            break
        time.sleep(1)
    ack=p.read(folder/"ack.json")
    p.need(ack["arm"]==arm and ack["job"]==job,"submission binding")
    d=p.arm_dir(OPS,ROOT,arm)
    kit=original.pinned_kit(ROOT)
    old=reader(kit)
    P,ck,plate,ident=inputs(kit,arm)
    p.need(p.read(OPS/"source.json")==ident,"arm and dispatch source differ")
    env=original.engine_env(HOME,ROOT)
    env.update(OMP_NUM_THREADS="1",MKL_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1")
    if arm in ("UT","UC"):
        original.check_gate(ROOT,kit,arm,env["PY"])
    kind=original.STAGES[arm]
    deck=kit/"decks"/p.BED/("in."+kind+".liggghts")
    base=ROOT/p.BED/"ul_base.in"
    meta=ack["resume"]
    if meta and arm=="UB" and not d.exists():
        snapshot(ROOT/p.BED/arm,d,meta)
    if meta:
        p.need(p.checkpoint(d)==meta and not (d/"ul_summary.txt").exists(),"restart pair changed or summary present")
        prior=p.read(OPS/"attempts"/arm/ack["previous"]/"started.json") if ack["previous"] else None
        p.need(original.SUMS_SHA==ident["kit"] and (prior is None or prior["identity"]==ident),"earlier segment identity")
        original.checked(d/"deck.liggghts",p.digest(deck))
        ck=d/"restart"/("restart_unload_%d.bin"%meta["step"])
        state=d/"restart"/("state_unload_%d.in"%meta["step"])
        run_probe(folder,deck,meta,env,state,ck,base,plate,P["beds"][p.BED]["atoms"])
        p.need(p.checkpoint(d)==meta,"restart changed after probe")
    else:
        d.mkdir(parents=True)
        state="-"
    screen="screen.txt" if not meta else "screen_a%d.txt"%(int(folder.name)+(1 if arm=="UB" else 0))
    p.need(not (d/screen).exists(),"screen path already used")
    manifest=d/"run_manifest.txt"
    with manifest.open("a",encoding="utf8") as f:
        f.write("bed=%s\njob=%s\nnp=6\nslurm_job=%s slurm_ntasks=6\n"%(p.BED,arm,job))
        if meta:
            f.write("resume_from=%d\n"%meta["step"])
    p.publish(folder/"started.json",dict(job=job,identity=ident,deck=p.digest(deck),checkpoint=meta))
    script='set -u\nEXTRA_VARS=()\nFAILS=0\nsay(){ echo "$*"; }\nnote(){ echo "$*" >> "$MAN"; }\ndie(){ echo "$*" >&2; exit 2; }\n'+run_function(kit)+'\nrun_deck "$@"\n'
    env.update(BASE=str(base),PLATE=str(plate),KIT=str(kit),BED=p.BED,MAN=str(manifest),WORK_ROOT=str(d.parent.parent))
    subprocess.run(["bash","-c",script,"isolated_deck",str(d),kind,str(ck),str(state),
                    "1" if meta else "0",screen],cwd=d,env=env,check=True)
    original.prove_origin(ROOT)
    verdict,usable,control=assess(old,P,d,arm)
    technical=not verdict.get("problems") if arm!="UC" else control
    # The frozen reader uses sets in some nested diagnostic fields.
    normal=json.loads(json.dumps(verdict,default=lambda x:sorted(x) if isinstance(x,set) else str(x),allow_nan=False))
    p.publish(d/"arm_verdict.json",normal)
    with manifest.open("a",encoding="utf8") as f:
        f.write("reader_arm_rc=0\nend=%s fails=0 reader_rc=0\n"%original.now())
    p.publish(folder/"finished.json",dict(job=job,arm=arm,technical_ok=technical,endpoint_usable=usable,runner_rc=0,control_ok=control,
              verdict=p.digest(d/"arm_verdict.json"),manifest=p.digest(manifest),identity=ident))
