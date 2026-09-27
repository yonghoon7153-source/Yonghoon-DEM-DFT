"""Read-only production audit; synthetic fixtures only. Never starts LIGGGHTS."""
import contextlib, io, json, math, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"scripts"))
import make_mixer_deck as gen
import check_contact_validity as cv
import measure_mixing_index as mi
import mixer_deck_diff as dd
import mixer_restart_phase_test as pt

def clean(v):
    if isinstance(v,dict): return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [clean(x) for x in v]
    if isinstance(v,np.ndarray): return clean(v.tolist())
    if isinstance(v,(float,np.floating)) and not np.isfinite(v): return str(v)
    if isinstance(v,np.generic): return v.item()
    return v

def write_stl(p,T):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8") as f:
        f.write("solid test\n")
        for tri in T:
            f.write("facet normal 0 0 0\nouter loop\n")
            for v in tri: f.write("vertex "+" ".join(format(x,".17g") for x in v)+"\n")
            f.write("endloop\nendfacet\n")
        f.write("endsolid test\n")

def dump(p,st,D,header=True):
    keys=list(D)
    text=(f"ITEM: TIMESTEP\n{st}\nITEM: NUMBER OF ATOMS\n{len(D[keys[0]])}\n"
          "ITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\n") if header else ""
    p.write_text(text+"ITEM: ATOMS "+" ".join(keys)+"\n"+"\n".join(
        " ".join(format(float(x),".17g") for x in row) for row in zip(*(D[k] for k in keys)))+"\n",encoding="utf-8")

def run_dir(td,name,deck):
    r=Path(td)/name
    (r/"post").mkdir(parents=True)
    (r/"in.mixer").write_text(deck,encoding="utf-8")
    for nm in ("Drum","Front","Back"):
        shutil.copyfile(ROOT/f"dem_scripts/mixer_20260919/{nm}.stl",r/f"{nm}.stl")
    return r

def dat(P,r,types=None):
    P=np.array(P);n=len(P)
    return dict(id=np.arange(1,n+1),type=np.full(n,3) if types is None else np.array(types),
                x=P[:,0],y=P[:,1],z=P[:,2],radius=np.broadcast_to(r,(n,)).copy())

def short(w):
    return {k:w.get(k) for k in ("verdict","phase_status","wall_max","wall_bound_worst","wall_bound_best","pp_max","tech","reject","window","n_frames")}

def receipt(path,spec,err=0.05,**kw):
    v=dict(test="restart_phase",passed=True,period=spec["moves"]["Drum"]["period"],
           axis=spec["moves"]["Drum"]["axis"].tolist(),angle_error_deg=err,binary_sha256="0"*64)
    v.update(kw);path.write_text(json.dumps(v),encoding="utf-8");return str(path)

def cloud(kind):
    P=[];t=[]
    for j,(y,z) in enumerate([(-.01,-.01),(-.01,.01),(.01,-.01),(.01,.01)]):
        for k in range(24):
            P.append([(k-12)*1e-5,y,z])
            counts={"ref":(10,14),"ref_alt":(7,17),"mid":(3,21)}
            t.append((1 if j<2 else 3) if kind=="seg" else 1 if k<counts[kind][0 if j<2 else 1] else 3)
    return dat(P,1e-5,t)

def main():
    out={}
    p=gen.plan(100000,cgf=151.4);rpm=gen.resolve_rpm(p["R"])
    lc=gen.deck(p,rpm,8,seed=32452843,arm="LC")
    lh=gen.deck(p,rpm,8,seed=32452843,arm="LH")
    sp=cv.deck_walls(lh);axis=sp["moves"]["Drum"]["axis"];dt=sp["dt"];period=sp["moves"]["Drum"]["period"]
    with tempfile.TemporaryDirectory(prefix="r3_review_") as td_:
        td=Path(td_)
        # Analyze nominal synthetic A/B continuation, then evidence-deletion mutants.
        a,b=pt.gen_decks(lc);ra=td/"phase"/"A";rb=td/"phase"/"B"
        for dest,deck,name in ((ra,a,"in.phase_a"),(rb,b,"in.phase_b")):
            (dest/"post_mesh").mkdir(parents=True)
            (dest/name).write_text(deck,encoding="utf-8")
            for nm in ("Drum","Front","Back"):shutil.copyfile(ROOT/f"dem_scripts/mixer_20260919/{nm}.stl",dest/f"{nm}.stl")
        base=ra.parent
        (base/"gen.json").write_text(json.dumps(dict(n1=pt.N1,n2=pt.N2,every=pt.EVERY,deck="synthetic",deck_sha256="0"*64)),encoding="utf-8")
        T=np.vstack([cv.read_stl(ra/f"{nm}.stl")*sp["meshes"][nm][1] for nm in ("Drum","Front","Back")])
        for st in (25000,30000):
            rot=cv._rot(axis,2*np.pi*st*dt/period)
            for dest in (ra,rb):write_stl(dest/"post_mesh"/f"mesh_{st}.stl",T@rot.T)
        def analyze():
            with contextlib.redirect_stdout(io.StringIO()): return pt.analyze(str(base))
        v=analyze();out["receipt_nominal_no_binary_no_logs"]=v
        for path in (ra/"post_mesh").glob("mesh_*.stl"):path.unlink()
        out["receipt_missing_all_A"]=analyze()
        (rb/"post_mesh"/"mesh_30000.stl").unlink()
        out["receipt_one_B_missing_all_A"]=analyze()
        # Pre-restart-only B is not a test of read_restart.
        (rb/"post_mesh"/"mesh_25000.stl").unlink()
        write_stl(rb/"post_mesh"/"mesh_0.stl",T)
        write_stl(ra/"post_mesh"/"mesh_0.stl",T)
        out["receipt_only_step0"]=analyze()
        # The consumer does not bind the purported binary or numeric fields.
        rp=td/"r.json"
        cases=dict(null_binary=dict(binary_sha256=None),nonsense_binary=dict(binary_sha256="not-a-sha"),
                   wrong_dt=dict(dt=dt*2),wrong_deck=dict(deck_source_sha256="f"*64),
                   zero_axis=dict(axis=[0,0,0]),nan_period=dict(period=float("nan")),string_false=dict(passed="false"))
        accepted={}
        for name,kw in cases.items():
            receipt(rp,sp,**kw)
            try:
                with np.errstate(all="ignore"): cv.load_phase_receipt(str(rp),sp)
                accepted[name]=True
            except Exception as e: accepted[name]=str(e)
        out["receipt_load_mutants"]=accepted
        # Actual 39-facet geometry, campaign SE radius.
        geom=run_dir(td,"geometry",lh)
        T0=cv.read_stl(geom/"Drum.stl")*sp["meshes"]["Drum"][1]
        N,C=cv._planes(T0,T0.reshape(-1,3).mean(0))
        r=p["d"]["SE"]/2;facet=2*np.pi/len(C);eps=np.radians(.05)
        de=mi.deck_plan(geom/"in.mixer")["dump_every"]
        t0=(sp["moves"]["Drum"]["start_step"]//de)*de;steps=[t0+i*de for i in range(3)]
        out["geometry"]=dict(r_SE_m=r,apo_m=float(C[0]),facets=len(C),eps_deg=.05,dt=dt,period=period,t0=t0,dump_every=de)
        # True maximum at an interior angle +eps/2, not 0 or either endpoint.
        run=run_dir(td,"interior_angle",lh);truth=[];true_rel=.010008
        for st in steps:
            P0=-(C-r+true_rel*r)[:,None]*N
            P=P0@cv._rot(axis,cv.mesh_angle(sp,"Drum",st)+eps/2).T
            dump(run/"post"/f"mix_{st}.liggghts",st,dat(P,r))
            n,c,_,_=cv.container_at(str(run),sp,st,dtheta=eps/2)
            truth.append(float(cv.wall_overlaps(P,np.full(len(P),r),n,c)[0].max()))
        w=cv.check_window(str(run),n_expected=len(N),phase_receipt=receipt(rp,sp))
        out["angle_interior_false_pass"]=dict(truth_max=max(truth),result=short(w))
        # Tolerance effect near the side of a real facet, not just its midpoint.
        ni=N[0];tan=np.cross(axis,-ni);apo=C[0];half=apo*np.tan(facet/2)
        P=(-(apo-r+.005*r)*ni+.8*half*tan)[None,:]
        vals=[]
        for th in (0,-eps,eps):
            NN=N@cv._rot(axis,th).T
            vals.append(float(cv.wall_overlaps(P,np.array([r]),NN,C)[0][0]))
        out["angle_tolerance_side"]=dict(relative_overlap_at_0_minus_plus=vals,
                                         increase_percentage_points=100*(max(vals)-vals[0]))
        # Whole initial portion is missing: st0 silently reanchors.
        run=run_dir(td,"missing_t0",lh)
        D=dat([[0,0,0],[.001,0,0]],r,[1,3])
        for st in [t0-de,t0+de,t0+2*de]:dump(run/"post"/f"mix_{st}.liggghts",st,D)
        # Add a much earlier frame; remove the intended t0 and its immediate prefix.
        (run/"post"/f"mix_{t0-de}.liggghts").unlink()
        dump(run/"post"/"mix_0.liggghts",0,D)
        out["contact_missing_prefix"]=short(cv.check_window(str(run),n_expected=2))
        # An absent id/header after t0 is not rejected.
        for name,mode in (("missing_id_after_t0","id"),("missing_headers","header"),("fractional_type","type")):
            run=run_dir(td,name,lh)
            for st in steps:
                d={k:v.copy() for k,v in D.items()}
                if mode=="id" and st>t0:d.pop("id")
                if mode=="type":d["type"]=d["type"].astype(float)+.5
                dump(run/"post"/f"mix_{st}.liggghts",st,d,header=mode!="header")
            out[name]=short(cv.check_window(str(run),n_expected=2,expect_counts={1:1,3:1}))
        # Missing mesh end-caps; convexity is not closure/completeness.
        run=run_dir(td,"mesh_drum_only",lh)
        for st in steps:
            NN,CC,owner,_=cv.container_at(str(run),sp,st)
            j=owner.index("Front");nc=NN[j];cc=CC[j]
            P=(-(cc-r+.02*r)*nc)[None,:]
            dump(run/"post"/f"mix_{st}.liggghts",st,dat(P,r))
            write_stl(run/"post_mesh"/f"mesh_{st}.stl",T0@cv._rot(axis,cv.mesh_angle(sp,"Drum",st)).T)
        out["mesh_missing_caps"]=short(cv.check_window(str(run),n_expected=1))
        out["mesh_missing_caps"]["true_complete_wall_overlap"]=float(cv.wall_overlaps(P,np.array([r]),NN,CC)[0].max())
        # Missing planned reference/t0 boundaries, and extra off-lattice sample.
        dk=("timestep 0.001\nrun 1\nrun 100\nrun 100\n"
            "dump dmp all custom 40 post/mix_*.liggghts id type x y z radius\n"
            "fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1 0 0 period 1.00001\nrun 8000\n")
        ref=run_dir(td,"ref",dk);dump(ref/"post"/"mix_200.liggghts",200,cloud("ref"))
        def reader_case(name,start=200,extra=None,missing_prev=False):
            run=run_dir(td,name,dk)
            for st in range(start,8201,40):
                if missing_prev and 6240<=st<7160:continue
                if name=="reader_missing_t0" and st==200:continue
                dump(run/"post"/f"mix_{st}.liggghts",st,cloud("seg") if st==start else cloud("mid"))
            if extra: dump(run/"post"/f"mix_{extra}.liggghts",extra,cloud("seg"))
            v=mi.analyse(str(run),str(ref),.02,cells=2,x_cells=1)
            return {k:v[k] for k in ("t0_step","S0","SR","planned","smoke","tech","dump_gaps")}
        out["reader_nominal"]=reader_case("reader_nominal")
        out["reader_missing_t0"]=reader_case("reader_missing_t0",start=160)
        out["reader_offgrid_extra"]=reader_case("reader_offgrid_extra",extra=7301)
        out["reader_prev_missing"]=reader_case("reader_prev_missing",missing_prev=True)
        # A lost reference endpoint silently substitutes an earlier settling frame.
        (ref/"post"/"mix_200.liggghts").unlink()
        dump(ref/"post"/"mix_160.liggghts",160,cloud("ref_alt"))
        out["reference_endpoint_missing"]=reader_case("reference_endpoint_missing")
        # Same physics seed in every pair but directory labels promise three different seeds.
        runs=td/"pairs";runs.mkdir()
        for seed in gen.CAMPAIGN_SEEDS:
            for arm,deck in (("LC",lc),("LH",lh)):
                rdir=runs/f"{arm}_s{seed}";rdir.mkdir();(rdir/"in.mixer").write_text(deck,encoding="utf-8")
        pairs,found,missing=dd.collect_pairs(str(runs),"LH","LC",gen.CAMPAIGN_SEEDS)
        out["duplicated_physical_seed_three_dirs"]=dict(found=sorted(found),missing=sorted(missing),
             verdicts=[dd.diff_decks(Path(a).read_text(encoding="utf-8"),Path(b).read_text(encoding="utf-8"),"B",
               expect=dd.parse_deck(lh)["ced"])["verdict"] for a,b in pairs],
             actual_unique_decks=2)
        cp=subprocess.run([sys.executable,str(ROOT/"scripts/mixer_deck_diff.py"),"--runs",str(runs),"--allow","B",
                           "--expect-deck",str(runs/"LH_s32452843/in.mixer")],capture_output=True,text=True,encoding="utf-8")
        out["duplicated_physical_seed_three_dirs"]["cli"]={"returncode":cp.returncode,"stdout":cp.stdout,"stderr":cp.stderr}
    # Required old counterexamples run independently with changed expectations.
    oldpath=ROOT/"previous_review_probe.py"
    source=oldpath.read_text(encoding="utf-8")
    source="\n".join(l for l in source.splitlines() if not l.strip().startswith("assert "))
    ns={"__name__":"old_probe_replayed","__file__":str(ROOT/"old_probe_replayed.py")}
    exec(compile(source,str(oldpath),"exec"),ns)
    capture=io.StringIO()
    with contextlib.redirect_stdout(capture): ns["main"]()
    out["old_probe_replay"]=json.loads(capture.getvalue())
    assertions={
        "analyzer_missing_A_false_green":out["receipt_missing_all_A"]["passed"],
        "pre_restart_only_false_green":out["receipt_only_step0"]["passed"],
        "interval_false_green":out["angle_interior_false_pass"]["truth_max"]>.01 and out["angle_interior_false_pass"]["result"]["verdict"]=="PASS",
        "removed_caps_false_green":out["mesh_missing_caps"]["verdict"]=="PASS",
        "missing_id_false_green":out["missing_id_after_t0"]["verdict"]=="PASS",
        "missing_t0_reader_false_green":out["reader_missing_t0"]["t0_step"]==160 and not out["reader_missing_t0"]["tech"],
        "old_wrong_phase_closed":out["old_probe_replay"]["wrong_phase_false_pass"]["result"]["verdict"]=="TECH",
        "old_right_phase_closed":out["old_probe_replay"]["right_phase_false_tech"]["result"]["verdict"]=="PASS",
        "old_matrix_closed":all(v["verdict"]=="FAIL" for v in out["old_probe_replay"]["matrix_mutants"].values()),
        "old_previous_bin_closed":out["old_probe_replay"]["missing_previous_bin"]["planned"]["flat"] is None,
    }
    out["probe_assertions"]=assertions
    (ROOT/"review_round3_output.json").write_text(json.dumps(clean(out),ensure_ascii=False,indent=2,allow_nan=False),encoding="utf-8")
    print(json.dumps(clean({k:v for k,v in out.items() if k!="old_probe_replay"}),ensure_ascii=False,indent=2,allow_nan=False))
    if not all(assertions.values()): raise AssertionError(assertions)

if __name__=="__main__":main()
