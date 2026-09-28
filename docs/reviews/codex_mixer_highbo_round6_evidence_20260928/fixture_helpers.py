"""Independent round-5 counterexamples. Synthetic files only; never invokes DEM."""
import contextlib, io, json, math, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"scripts"))
import check_contact_validity as cv
import mixer_restart_phase_test as pt
import measure_mixing_index as mi
import make_mixer_deck as gen
import mixer_deck_diff as dd

SMALL="""atom_style granular
region reg block -0.02 0.02 -0.02 0.02 -0.02 0.02 units box
create_box 4 reg
timestep 1e-6
fix m1 all property/global youngsModulus peratomtype 1e7 1e7 1e7 1e7
fix Drum all mesh/surface file Drum.stl type 4 scale 0.0149277
fix Front all mesh/surface file Front.stl type 4 scale 0.0149277
fix Back all mesh/surface file Back.stl type 4 scale 0.0149277
fix walls all wall/gran model hertz tangential history mesh n_meshes 3 meshes Drum Front Back
fix pt1 all particletemplate/sphere 10487 atom_type 1 density constant 4800 radius constant 0.0009
fix pdd all particledistribution/discrete 32452867 1 pt1 1.0
region ins cylinder x 0 0 0.005 -0.001 0.001 units box
fix ins all insert/pack seed 32452843 distributiontemplate pdd maxattempt 200 insert_every once region ins particles_in_region 10
run 1
unfix ins
dump dmp all custom 500 post/mix_*.liggghts id type x y z radius
restart 1000 restart/a.bin restart/b.bin
run 1000
run 1000
fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1 0 0 period 0.012
fix mvF all move/mesh mesh Front rotate origin 0 0 0 axis 1 0 0 period 0.012
fix mvB all move/mesh mesh Back rotate origin 0 0 0 axis 1 0 0 period 0.012
run 12000
"""
BANNER="LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled review-fixture)"
def quiet(fn,*a,**kw):
    with contextlib.redirect_stdout(io.StringIO()): return fn(*a,**kw)
def clean(v):
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [clean(x) for x in v]
    if isinstance(v,np.ndarray):return clean(v.tolist())
    if isinstance(v,(float,np.floating)) and not np.isfinite(v):return str(v)
    if isinstance(v,np.generic):return v.item()
    return v
def sha(p):return pt._sha(str(p))
def js(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=1),encoding="utf-8")
def write_stl(p,T):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8") as f:
        f.write("solid fixture\n")
        for tri in T:
            f.write(" facet normal 0 0 0\n  outer loop\n")
            for v in tri:f.write("   vertex "+" ".join(format(float(x),".12e") for x in v)+"\n")
            f.write("  endloop\n endfacet\n")
        f.write("endsolid fixture\n")
def rot_x(T,theta):
    # Independent explicit x-axis rotation, not production Rodrigues helper.
    out=T.copy();out[...,1]=T[...,1]*math.cos(theta)-T[...,2]*math.sin(theta)
    out[...,2]=T[...,1]*math.sin(theta)+T[...,2]*math.cos(theta)
    return out
def rundir(td,name,deck):
    p=td/name;(p/"post").mkdir(parents=True);(p/"in.mixer").write_text(deck,encoding="utf-8")
    for n in ("Drum","Front","Back"):shutil.copyfile(ROOT/f"dem_scripts/mixer_20260919/{n}.stl",p/f"{n}.stl")
    return p
def dat(P,r,types=None):
    P=np.array(P);n=len(P)
    return dict(id=np.arange(1,n+1),type=np.full(n,3) if types is None else np.array(types),
                x=P[:,0],y=P[:,1],z=P[:,2],radius=np.broadcast_to(r,(n,)).copy())
def dump(p,s,D,header=True):
    keys=list(D)
    pre=f"ITEM: TIMESTEP\n{s}\nITEM: NUMBER OF ATOMS\n{len(D[keys[0]])}\nITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\n" if header else ""
    p.write_text(pre+"ITEM: ATOMS "+" ".join(keys)+"\n"+"\n".join(
        " ".join(format(float(x),".17g") for x in row) for row in zip(*(D[k] for k in keys)))+"\n",encoding="utf-8")
def brief(v):
    return {k:v.get(k) for k in ("verdict","phase_status","wall_max","wall_lower_max","tech","reject","window","n_frames")}
def status(base):
    code=re.findall(r"<<'PY'[^\n]*\n(.*?)\nPY\n",pt.RUN_SH,re.S)[1]
    cp=subprocess.run([sys.executable,"-c",code,"0","0"],cwd=base,capture_output=True,text=True,encoding="utf-8")
    if cp.returncode:raise RuntimeError(cp.stderr)
def fixture(td,kind="normal",deck=SMALL):
    run=rundir(td,"campaign",deck);base=td/"phase"
    quiet(pt.gen,str(run/"in.mixer"),str(base))
    g=json.loads((base/"gen.json").read_text())
    spec=cv.deck_walls(deck);de=g["dump_every"]
    U=np.vstack([cv.read_stl(run/f"{n}.stl")*spec["meshes"][n][1] for n in ("Drum","Front","Back")])
    for sub,steps in (("A",range(de,g["run_total"]+1,de)),("B",range(g["n1"],g["run_total"]+1,de))):
        for s in steps:
            angle=max(s-g["rot_start"],0)*spec["dt"]/spec["moves"]["Drum"]["period"]*2*math.pi
            T=rot_x(U,angle)
            if kind=="translation" and s>2001:T[...,0]+=8e-8
            if kind=="nan_B" and sub=="B":T[:]=np.nan
            write_stl(base/sub/"post_mesh"/f"mesh_{s}.stl",T)
        (base/sub/"log.lmp").write_text(BANNER+f"\nStep Atoms KinEng\n {g['run_total']} 0 0\nLoop time fixture\n",encoding="utf-8")
    binary=td/"fixture_binary";binary.write_bytes(b"fixture-build-A")
    files={p:sha(base/p) for p in ["A/in.phase_a","B/in.phase_b"]+
           [f"{sub}/{n}.stl" for sub in ("A","B") for n in ("Drum","Front","Back")]}
    js(base/"seal.json",dict(binary_path=str(binary),binary_sha256=sha(binary),files=files))
    status(base)
    (run/"log.lmp").write_text(BANNER+"\n",encoding="utf-8")
    return run,base,U,g,binary
def receipt(base):
    return quiet(pt.analyze,str(base),out=str(base/"receipt.json"))
def old_reader(td,mode,runname=None):
    dk="timestep .001\ndump dmp all custom 40 post/mix_*.liggghts id type x y z radius\nrun 1\nrun 100\nrun 100\nfix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1 0 0 period 1\nrun 8000\n"
    run=rundir(td,runname or "reader_"+mode,dk);ref=rundir(td,"ref_"+mode,dk.replace("run 8000","run 0"))
    def cloud(kind):
        P=[];t=[]
        for j,(y,z) in enumerate([(-.01,-.01),(-.01,.01),(.01,-.01),(.01,.01)]):
            for k in range(24):
                P.append([(k-12)*1e-5,y,z]);n={"ref":(10,14),"alt":(7,17),"mid":(3,21)}.get(kind)
                t.append((1 if j<2 else 3) if kind=="seg" else 1 if k<n[0 if j<2 else 1] else 3)
        return dat(P,1e-5,t)
    dump(ref/"post/mix_160.liggghts",160,cloud("alt"))
    if mode!="no_ref_t0":dump(ref/"post/mix_200.liggghts",200,cloud("ref"))
    for s in range(200,8201,40):
        if mode=="no_t0" and s==200:continue
        D=cloud("seg" if s==200 else "mid")
        if mode=="no_id" and s==7800:D.pop("id")
        if mode=="fractional_type" and s==7800:D["type"]=D["type"]+.5
        dump(run/"post"/f"mix_{s}.liggghts",s,D,header=not(mode=="no_header" and s==7800))
    if mode=="extra":dump(run/"post/mix_7301.liggghts",7301,cloud("seg"))
    if mode=="duplicate":shutil.copyfile(run/"post/mix_7800.liggghts",run/"post/copy_7800.liggghts")
    try:
        v=mi.analyse(str(run),str(ref),.02,cells=2,x_cells=1)
        if runname:return v
        return {k:v[k] for k in ("S0","SR","planned","smoke","tech","lattice")}
    except (SystemExit,ValueError) as e:return dict(refused=str(e))

# Additional round-5 checks reuse round-4 synthetic builders above.
import importlib.util, hashlib
spec_check=importlib.util.spec_from_file_location("start_check",ROOT/"dem_scripts/mixer_20260921/start_check.py")
sc=importlib.util.module_from_spec(spec_check);spec_check.loader.exec_module(sc)

def bind(run,binary,backend="local",np_=20):
    rec=dict(schema=cv.LAUNCH_SCHEMA,run=run.name,stage="first",backend=backend,
        lmp_sha256=sha(binary),lmp_realpath=os.path.realpath(binary),
        sha256={f:sha(run/f) for f in ("in.mixer","Drum.stl","Front.stl","Back.stl")})
    if backend=="slurm":
        runner=run/"run_lh.sbatch";runner.write_text("# fixture, not executable\n")
        rec["slurm"]=dict(np=np_,runner_sha256=sha(runner),start_check_sha256=sha(ROOT/"dem_scripts/mixer_20260921/start_check.py"))
    js(run/"launch_record.json",rec);return rec

def accept(path,run,deck=SMALL,steps=(2000,2500,3000)):
    try:
        z=cv.load_phase_receipt(str(path),cv.deck_walls(deck),str(run),deck,steps)
        return dict(accepted=True,eps=z["eps_wall_deg"],pos_bound=z["pos_bound_m"])
    except (ValueError,TypeError,KeyError) as e:return dict(accepted=False,reason=str(e))

def smoke_fixture(td):
    first="LH_s32452843";refname="E0_s32452843"
    old=old_reader(td,"normal",runname=first)
    run=Path(old["run"]);ref=Path(old["ref"])
    ref.rename(td/refname);ref=td/refname
    # Four axial slabs, >=20 particles per cell, registered transverse grid.
    def cloud(kind):
        P=[];types=[]
        for j,(y,z) in enumerate([(-.008,-.008),(-.008,.008),(.008,-.008),(.008,.008)]):
            for x in (-.003,-.001,.001,.003):
                for k in range(24):
                    P.append([x,y,z])
                    types.append((1 if j<2 else 3) if kind=="seg" else 1 if k<({"ref":(10,14),"mid":(3,21)}[kind][0 if j<2 else 1]) else 3)
        return dat(P,1e-5,types)
    for s in range(200,8201,40):dump(run/"post"/f"mix_{s}.liggghts",s,cloud("seg" if s==200 else "mid"))
    dump(ref/"post/mix_200.liggghts",200,cloud("ref"))
    binary=td/"binary";binary.write_bytes(b"mock-identity-not-executed")
    rec=bind(run,binary)
    rest=[f"LH_s{s}" for s in (49979687,67867967)]
    for n in rest:rundir(td,n,dd.expected_deck("LH",int(n.split("_s")[1])))
    rec["cohort"]={n:{f:sha(td/n/f) for f in ("in.mixer","Drum.stl","Front.stl","Back.stl")} for n in [first]+rest}
    js(run/"launch_record.json",rec)
    v=mi.analyse(str(run),str(ref),.013138,cells=16,x_cells=4,n_min=20,axis="x")
    cert=td/"smoke.json";js(cert,[v])
    src=(ROOT/"dem_scripts/mixer_20260921/launch_highbo.sh").read_text(encoding="utf-8")
    blocks=re.findall(r"<<'PY'[^\n]*\n(.*?)\nPY\n",src,re.S)
    gate=next(b for b in blocks if "cert, out, first, lmp_path, root" in b)
    def invoke():
        p=subprocess.run([sys.executable,"-c",gate,str(cert),str(td),first,str(binary),str(ROOT)]+rest,capture_output=True,text=True,encoding="utf-8")
        return dict(rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
    return run,ref,cert,v,invoke

def main():
    out={}
    with tempfile.TemporaryDirectory(prefix="hbr5_synthetic_") as tmp:
        td=Path(tmp)
        for kind in ("normal","nan_B","translation","empty_seal_lists"):
            run,base,U,g,binary=fixture(td/kind,kind);bind(run,binary)
            if kind=="empty_seal_lists":
                z=json.loads((base/"seal.json").read_text());z["files"]={};js(base/"seal.json",z)
                z=json.loads((base/"run_status.json").read_text())
                for sub in ("A","B"):z[sub]["dumps"]={}
                js(base/"run_status.json",z)
            rc=receipt(base)
            out[kind]=dict(passed=rc["passed"],reasons=rc["reasons"],pos_bound_m=rc["pos_bound_m"],angle_bound_deg=rc["angle_bound_deg"],ab_max=rc["ab_max_vertex_diff_m"],consumer=accept(base/"receipt.json",run))
            if kind=="normal":
                good=json.loads((run/"launch_record.json").read_text())
                bad=dict(good,lmp_sha256="0"*64);js(run/"launch_record.json",bad)
                out["different_binary"]=accept(base/"receipt.json",run)
                js(run/"launch_record.json",good)
                changed=SMALL.replace("run 1000","run 1500");(run/"in.mixer").write_text(changed);bind(run,binary)
                out["different_clock"]=accept(base/"receipt.json",run,changed,(3000,3500,4000))
                (run/"in.mixer").write_text(SMALL);bind(run,binary);(run/"in.resume").write_text("# marker")
                out["resume_refused"]=accept(base/"receipt.json",run)
            if kind=="translation":
                r=75.7e-6;N,C,own,_=cv.container_at(str(run),cv.deck_walls(SMALL),2500)
                back=next(i for i,n in enumerate(N) if n[0]>.99)
                P=np.array([[-C[back]+r*(1-.0095),0,0]])
                for s in (2000,2500,3000):dump(run/"post"/f"mix_{s}.liggghts",s,dat(P,r))
                out["translation_wall"]=brief(cv.check_window(str(run),phase_receipt=str(base/"receipt.json")))
        # Independent static-wall and disabled-mesh controls using pinned wall geometry.
        e0=SMALL.replace('run 12000\n','run 0\n')
        er=rundir(td,'E0_control',e0)
        ep=td/'expected_e0.in';ep.write_text(e0)
        ns,cs,owners,_=cv.container_at(str(er),cv.deck_walls(e0),2000)
        ii=next(i for i,n in enumerate(ns) if abs(n[0])<.1)
        radius=75.7e-6;normal=ns[ii];tangent=np.cross([1.,0.,0.],normal)
        point=-normal*cs[ii]+normal*radius*(1-.005)+tangent*.9*cs[ii]*math.tan(math.pi/39)
        dump(er/'post/mix_2000.liggghts',2000,dat([point],radius))
        kwargs=dict(expect_deck=str(ep),stl_ref_dir=str(ROOT/'dem_scripts/mixer_20260919'))
        out['static_e0']=brief(cv.check_window(str(er),**kwargs))
        out['static_no_expected']=brief(cv.check_window(str(er)))
        end=next(i for i,n in enumerate(ns) if n[0]>.99)
        point2=-ns[end]*cs[end]+ns[end]*radius*(1-.02)
        dump(er/'post/mix_2000.liggghts',2000,dat([point2],radius))
        out['static_end_overlap']=brief(cv.check_window(str(er),**kwargs))
        (er/'post_mesh').mkdir();(er/'post_mesh/mesh_2000.stl').write_text('not even STL\n')
        out['disabled_garbage_mesh']=brief(cv.check_window(str(er),**kwargs))
        # Real start-check function and CLI against valid and malformed launch records.
        d=rundir(td,"start_guard",SMALL);binary=td/"guard_binary";binary.write_bytes(b"not-a-simulator")
        valid=bind(d,binary,backend="slurm")
        runner=d/"run_lh.sbatch";env=dict(os.environ,SLURM_NTASKS="20",SLURM_JOB_ID="12345")
        rec,why=sc.check(str(d),str(binary),str(runner),env)
        out["start_guard_normal"]=dict(ok=rec["ok"],reasons=why)
        for kind,data in (("empty_dict",{}),("null",None),("list",[]),("string","invalid")):
            js(d/"launch_record.json",data)
            p=subprocess.run([sys.executable,str(ROOT/"dem_scripts/mixer_20260921/start_check.py"),str(d),str(binary),str(runner)],env=env,capture_output=True,text=True,encoding="utf-8")
            job=json.loads((d/"job_start.json").read_text()) if (d/"job_start.json").exists() else None
            out["start_"+kind]=dict(rc=p.returncode,stdout=p.stdout,stderr=p.stderr,job_start=job)
            if (d/"job_start.json").exists():(d/"job_start.json").unlink()
        js(d/"launch_record.json",valid)
        (d/"in.mixer").write_text(SMALL+"# changed")
        rec,why=sc.check(str(d),str(binary),str(runner),env);out["start_changed_deck"]=dict(ok=rec["ok"],reasons=why)
        (d/"in.mixer").write_text(SMALL)
        # Genuine production receipt can be accepted for a sealed np20 run: np is not checked against receipt prefix.
        pr=json.loads((ROOT/"docs/data/mixer_phase_receipt_20260928/receipt_v2_ibb.json").read_text(encoding="utf-8"))
        rr=rundir(td,"LH_s32452843",dd.expected_deck("LH",32452843))
        lr=bind(rr,binary,backend="slurm",np_=20);lr["lmp_sha256"]=pr["binary_sha256"];js(rr/"launch_record.json",lr)
        job=dict(schema="mixer_highbo_job_start/1",ok=True,lmp_sha256=lr["lmp_sha256"],runner_sha256_executed=lr["slurm"]["runner_sha256"],
            start_check_sha256=lr["slurm"]["start_check_sha256"],launch_record_sha256=sha(rr/"launch_record.json"),slurm_ntasks=20)
        js(rr/"job_start.json",job);(rr/"log.lmp").write_text(pr["liggghts_version"]+"\n")
        out["np1_receipt_on_np20"]=accept(ROOT/"docs/data/mixer_phase_receipt_20260928/receipt_v2_ibb.json",rr, (rr/"in.mixer").read_text(),[9429264])
        out["np1_receipt_on_np20"].update(receipt_prefix=pr["seal"]["launch_prefix"],run_np=20,fixture_note="Synthetic run seal/start record; not an executed MPI job")
        # Smoke closed-world challenge: extra bin0 dump not listed in the genuine old certificate.
        run,ref,cert,v,invoke=smoke_fixture(td/"smoke")
        out["smoke_normal"]=invoke()
        wrong=json.loads(cert.read_text());wrong[0]["provenance"]["args"]["cells"]=2;js(cert,wrong)
        out["smoke_wrong_grid"]=invoke();js(cert,[v])
        shutil.copyfile(run/"post/mix_400.liggghts",run/"post/copy_400.liggghts")
        out["smoke_after_duplicate"]=invoke()
        now=mi.analyse(str(run),str(ref),.013138,cells=16,x_cells=4,n_min=20,axis="x")
        out["smoke_recomputed_duplicate"]=dict(smoke=now["smoke"],tech=now["tech"])
        # Producer helper completeness: transcript gen.json end lowered without modifying sealed decks.
        run,base,U,g,binary=fixture(td/"short_gen");bind(run,binary)
        original=g["run_total"];g["run_total"]=g["n1"]+g["dump_every"]
        js(base/"gen.json",g)
        for part in ("A","B"):
            for p in (base/part/"post_mesh").glob("*.stl"):
                if int(p.stem.split("_")[-1])>g["run_total"]:p.unlink()
            (base/part/"log.lmp").write_text(BANNER+f"\nStep Atoms KinEng\n {g['run_total']} 0 0\nLoop time fixture\n")
        status(base);rc=receipt(base)
        out["gen_end_truncated"]=dict(passed=rc["passed"],reasons=rc["reasons"],original_run_total=original,reported_run_total=rc["run_total"],motion_clock=rc["motion_clock"],nA=len(rc["steps_checked_A"]),nB=len(rc["steps_checked_B"]),consumer=accept(base/"receipt.json",run,SMALL,(2000,2500,3000)))
        # Quantities from the committed receipt and actual diameter plan.
        pp=gen.plan(100000,cgf=151.4)
        out["position_uncertainty_pct_points"]={t:100*pr["pos_bound_m"]/(pp["d"][t]/2) for t in ("AM_P","AM_S","SE")}
        out["radii_um"]={t:pp["d"][t]/2*1e6 for t in ("AM_P","AM_S","SE")}
        out["current_e0_decks"]={str(s):dict(bytes=len(dd.expected_deck('E0',s,revolutions=0).encode()),sha256=hashlib.sha256(dd.expected_deck('E0',s,revolutions=0).encode()).hexdigest()) for s in gen.CAMPAIGN_SEEDS}
        v1=json.loads((ROOT/"docs/data/mixer_phase_receipt_20260928/receipt_v1.json").read_text(encoding="utf-8"))
        rowfields=lambda q:[{k:r[k] for k in ("step","error_deg","resid_m")} for r in q["rows"]]
        out["receipt_rows_comparison"]=dict(n1=len(v1["rows"]),n2=len(pr["rows"]),exact_equal=rowfields(v1)==rowfields(pr),receipt_sha256=sha(ROOT/"docs/data/mixer_phase_receipt_20260928/receipt_v2_ibb.json"))
        # Algebraic counterexample: effects from execution environment alone clear the registered line.
        d=np.array([.12,.13,.11])
        out["confounding_example"]=dict(Bo_effect=0.0,environment_effects=d.tolist(),delta=float(d.mean()),SE=float(d.std(ddof=1)/np.sqrt(3)),large=bool(d.mean()>=.1 and d.mean()>=2*d.std(ddof=1)/np.sqrt(3)),note="constructed identifiability example, not measured mixer effect")
    checks=dict(nan_closed=not out["nan_B"]["passed"],empty_seal_closed=not out["empty_seal_lists"]["passed"],
        binary_closed=not out["different_binary"]["accepted"],clock_closed=not out["different_clock"]["accepted"],resume_closed=not out["resume_refused"]["accepted"],
        position_closed=out["translation_wall"]["verdict"]!="PASS",normal_receipt=out["normal"]["consumer"]["accepted"],
        normal_start=out["start_guard_normal"]["ok"],empty_start_bug=out["start_empty_dict"]["rc"]==0,
        normal_smoke=out["smoke_normal"]["rc"]==0,wrong_grid_closed=out["smoke_wrong_grid"]["rc"]!=0,
        extra_dump_bug=out["smoke_after_duplicate"]["rc"]==0 and not out["smoke_recomputed_duplicate"]["smoke"]["complete"],
        np20_unvalidated=out["np1_receipt_on_np20"]["accepted"],gen_truncation_bug=out["gen_end_truncated"]["passed"],
        static_closed=out['static_e0']['verdict']=='PASS' and out['static_no_expected']['verdict']!='PASS',
        mesh_disabled=out['disabled_garbage_mesh']['verdict']=='REJECT' and out['static_end_overlap']['verdict']=='REJECT')
    out["assertions"]=checks
    (ROOT/"review_round5_output.json").write_text(json.dumps(clean(out),ensure_ascii=False,indent=2,allow_nan=False),encoding="utf-8")
    print(json.dumps(clean({k:v for k,v in out.items() if "stdout" not in v}),ensure_ascii=False,indent=2))
    print("GATES",[(k,v["rc"]) for k,v in out.items() if "rc" in v])
    assert all(checks.values()),checks

if __name__=="__main__":main()
