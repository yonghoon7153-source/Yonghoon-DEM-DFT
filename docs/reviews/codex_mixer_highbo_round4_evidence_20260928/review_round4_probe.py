"""Independent round-4 counterexamples. Synthetic files only; never invokes DEM."""
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
def main():
    out={}
    with tempfile.TemporaryDirectory(prefix="hbr4_synthetic_") as tmp:
        td=Path(tmp)
        for kind in ("normal","nan_B","translation","no_A","no_B_after_restart","empty_seal_lists"):
            run,base,U,g,binary=fixture(td/kind,kind)
            if kind=="no_A":
                for f in (base/"A/post_mesh").glob("*.stl"):f.unlink()
                status(base)
            if kind=="no_B_after_restart":
                for f in (base/"B/post_mesh").glob("*.stl"):f.unlink()
                write_stl(base/"B/post_mesh/mesh_0.stl",U);status(base)
            if kind=="empty_seal_lists":
                z=json.loads((base/"seal.json").read_text());z["files"]={};js(base/"seal.json",z)
                z=json.loads((base/"run_status.json").read_text())
                for sub in ("A","B"):z[sub]["dumps"]={}
                js(base/"run_status.json",z)
            rc=receipt(base)
            out[kind+"_receipt"]={k:rc[k] for k in ("passed","reasons","angle_error_deg","angle_bound_deg","residual_max_m","ab_max_vertex_diff_m","steps_checked_A","steps_checked_B","rows")}
            if kind in ("nan_B","empty_seal_lists"):
                try:
                    loaded=cv.load_phase_receipt(str(base/"receipt.json"),cv.deck_walls(SMALL),run_dir=str(run),deck_text=SMALL,need_steps=[2000,2500,3000])
                    out[kind+"_receipt"]["consumer_accepted"]=loaded["passed"]
                except ValueError as e:out[kind+"_receipt"]["consumer_error"]=str(e)
            if kind=="normal":
                sp=cv.deck_walls(SMALL)
                # Contradictory on-disk launch record: never read by the receipt consumer.
                other=td/"different_binary";other.write_bytes(b"fixture-build-B-same-version-string")
                js(run/"launch_record.json",dict(lmp_sha256=sha(other)))
                loaded=cv.load_phase_receipt(str(base/"receipt.json"),sp,run_dir=str(run),deck_text=SMALL,need_steps=[2000,2500,3000])
                out["binary_mismatch_accepted"]=dict(accepted=loaded["passed"],receipt_sha=rc["binary_sha256"],run_seal_sha=sha(other),same_banner=BANNER)
                changed=SMALL.replace("run 1000","run 1500")
                loaded=cv.load_phase_receipt(str(base/"receipt.json"),cv.deck_walls(changed),run_dir=str(run),deck_text=changed,need_steps=[3000,3500,4000])
                out["rotation_start_mismatch_accepted"]=dict(accepted=loaded["passed"],signature_same=cv.motion_signature(SMALL,str(run))==cv.motion_signature(changed,str(run)),tested_start=2001,other_start=3001)
                # All validation fields present; step timeline is not verified by the motion hash.
            if kind=="translation":
                r=75.7e-6
                N,C,owner,_=cv.container_at(str(run),cv.deck_walls(SMALL),2500)
                back=[i for i,n in enumerate(N) if n[0]>.99][0]
                P=np.array([[-C[back]+r*(1-.0095),0,0]])
                D=dat(P,r)
                for s in (2000,2500,3000):dump(run/"post"/f"mix_{s}.liggghts",s,D)
                v=cv.check_window(str(run),phase_receipt=str(base/"receipt.json"))
                out["ignored_shape_residual_false_pass"]=dict(receipt_pass=rc["passed"],translation_m=8e-8,
                    nominal_overlap=float(cv.wall_overlaps(P,np.array([r]),N,C)[0][0]),true_overlap=.0095+8e-8/r,result=brief(v))
        # Existing mesh cap omission is closed; preserve vertices and counts but destroy cap triangles.
        run=rundir(td,"topology",SMALL);sp=cv.deck_walls(SMALL)
        U=np.vstack([cv.read_stl(run/f"{n}.stl")*.0149277 for n in ("Drum","Front","Back")])
        nf=len(cv.read_stl(run/"Front.stl"));front=cv.read_stl(run/"Front.stl")*.0149277
        center=np.array([front[0,0,0],0,0]);border=np.unique(front.reshape(-1,3),axis=0)
        border=border[np.linalg.norm(border[:,1:],axis=1)>1e-6]
        broken=np.array([[center,v,center] for v in border])
        assert len(broken)==nf
        badU=U.copy();badU[78:78+nf]=broken
        rr=75.7e-6;P=np.array([[float(front[0,0,0])-rr*(1-.02),0,0]])
        for s in (2000,2500,3000):
            dump(run/"post"/f"mix_{s}.liggghts",s,dat(P,rr))
            write_stl(run/"post_mesh"/f"mesh_{s}.stl",rot_x(badU,max(s-2001,0)*1e-6/.012*2*math.pi))
        out["degenerate_front_false_pass"]=brief(cv.check_window(str(run)))
        out["degenerate_front_false_pass"].update(true_complete_overlap=.02,triangles=len(U),degenerate_front_triangles=nf)
        for s in (2000,2500,3000):
            write_stl(run/"post_mesh"/f"mesh_{s}.stl",rot_x(U[:78],max(s-2001,0)*1e-6/.012*2*math.pi))
        out["old_missing_caps_closed"]=brief(cv.check_window(str(run)))
        for mode in ("normal","no_ref_t0","no_t0","extra","duplicate","no_id","no_header","fractional_type"):
            out["reader_"+mode]=old_reader(td,mode)
        # Cohort check: old copied actual seed bug; wrong target CED still passes launcher command.
        pairs=td/"pairs";pairs.mkdir()
        lhtarget=dd.expected_deck("LH",32452843)
        expected=td/"expect.in";expected.write_text(lhtarget,encoding="utf-8")
        def matrix_mutant(txt):
            parsed=dd.parse_deck(txt);n,vals=parsed["ced"];names=parsed["names"];vv=list(vals)
            for i in range(n):
                for j in range(n):
                    if tuple(sorted((names[i+1],names[j+1]))) in dd.ALLOW["B"]:vv[i*n+j]*=2
            blocks=[]
            for _,blk in pt.logical_commands(txt):
                toks=pt._tokens(blk)
                if "cohesionEnergyDensity" in toks:
                    ix=toks.index("cohesionEnergyDensity")
                    blocks.append(" ".join(toks[:ix+3]+[format(v,".12g") for v in vv])+"\n")
                else:blocks.append("\n".join(blk) if isinstance(blk,list) else blk)
            return "\n".join(blocks)+"\n"
        def ddcli(extra):
            c=subprocess.run([sys.executable,str(ROOT/"scripts/mixer_deck_diff.py"),"--runs",str(pairs),"--allow","B"]+extra,capture_output=True,text=True,encoding="utf-8")
            return dict(rc=c.returncode,stdout=c.stdout,stderr=c.stderr)
        for seed in gen.CAMPAIGN_SEEDS:
            for arm in ("LC","LH"):
                d=pairs/f"{arm}_s{seed}";d.mkdir()
                (d/"in.mixer").write_text(dd.expected_deck(arm,32452843),encoding="utf-8")
        out["copied_seeds_closed"]=ddcli(["--expect-deck",str(expected)])
        for seed in gen.CAMPAIGN_SEEDS:
            for arm in ("LC","LH"):
                t=dd.expected_deck(arm,seed)
                if arm=="LH":t=matrix_mutant(t)
                (pairs/f"{arm}_s{seed}/in.mixer").write_text(t,encoding="utf-8")
        out["launcher_target_without_expect"]=ddcli([])
        out["launcher_target_with_expect"]=ddcli(["--expect-deck",str(expected)])
        # The actual Python gate extracted from launch_highbo.sh, never the launcher itself.
        first="LH_s32452843";others=[f"LH_s{s}" for s in gen.CAMPAIGN_SEEDS[1:]]
        own=td/"launch_out";own.mkdir()
        binary=td/"launch_binary";binary.write_bytes(b"fixture-not-executable")
        for name in [first]+others:
            rr=rundir(own,name,dd.expected_deck("LH",int(name.split("_s")[1])))
        (own/first/"log.lmp").write_text(BANNER+"\n")
        fs=("in.mixer","Drum.stl","Front.stl","Back.stl")
        record=dict(stage="first",run=first,lmp_sha256=sha(binary),cohort={n:{f:sha(own/n/f) for f in fs} for n in [first]+others})
        js(own/first/"launch_record.json",record)
        # Genuine reader JSON from another folder and 2x2x1 rather than registered 16x16x4.
        v=old_reader(td/"foreign_results","normal",runname=first)
        cert=td/"copied_smoke.json";js(cert,[v])
        src=(ROOT/"dem_scripts/mixer_20260921/launch_highbo.sh").read_text(encoding="utf-8")
        gate=re.findall(r"<<'PY'[^\n]*\n(.*?)\nPY\n",src,re.S)[1]
        cp=subprocess.run([sys.executable,"-c",gate,str(cert),str(own),first,str(binary)]+others,capture_output=True,text=True,encoding="utf-8")
        out["foreign_wrong_grid_smoke_gate"]=dict(rc=cp.returncode,stdout=cp.stdout,stderr=cp.stderr,reader_grid=[2,2,1],required_grid=[16,16,4],actual_run=v["run"],intended_run=str(own/first),smoke=v["smoke"])
        # Analytic interval crosscheck against independent rotations at dense sampled angles.
        wallrun=rundir(td,"interval",SMALL);sp=cv.deck_walls(SMALL);planes=cv.container_planes0(str(wallrun),sp)
        rng=np.random.default_rng(20260928);violations=[];max_upper_gap=0.0;max_lower_gap=0.0
        for i in range(100):
            theta=rng.uniform(-8*np.pi,8*np.pi);eps=rng.uniform(0,np.radians(.05))
            points=rng.uniform(-.008,.008,(4,3));radii=np.full(4,75.7e-6)
            upper,lower,_=cv.wall_interval(points,radii,planes,theta-eps,theta+eps)
            vals=[]
            N,C=planes[:2]
            for ang in np.linspace(theta-eps,theta+eps,201):
                Nr=rot_x(N,ang);dist=points@Nr.T+C
                vals.append(((radii[:,None]-dist)/radii[:,None]).max(1))
            vals=np.array(vals);tol=1e-10
            if np.any(upper+tol<vals.max(0)) or np.any(lower-tol>vals.min(0)):violations.append(i)
            max_upper_gap=max(max_upper_gap,float((upper-vals.max(0)).max()))
            max_lower_gap=max(max_lower_gap,float((vals.min(0)-lower).max()))
        out["interval_independent_grid_check"]=dict(cases=100,particles=400,angles_each=201,violations=violations,max_upper_gap=max_upper_gap,max_lower_gap=max_lower_gap)
        # The old off-center angular maximum: three samples missed it, exact extrema include it.
        N,C=cv.container_at(str(wallrun),sp,0)[:2];r0=75.7e-6
        j=next(j for j,n in enumerate(N) if abs(n[0])<.1)
        thstar=np.radians(.025)
        P=rot_x(np.array([-N[j]*(C[j]-r0*(1-.010008))]),thstar)
        upper,lower,_=cv.wall_interval(P,np.array([r0]),planes,-np.radians(.05),np.radians(.05))
        out["old_interval_counterexample_closed"]=dict(upper=float(upper[0]),lower=float(lower[0]),expected="TECH" if lower[0]<=.01<upper[0] else "unexpected")
        # Code Bo is a homogeneous calibration target, not the actual mixed-pair F/W.
        pp=gen.plan(100000,cgf=151.4);M=gen.ced_matrix("LH",pp["d"]);mixbo={}
        se=gen.TYPES.index("SE");rs=pp["d"]["SE"]/2;ws=4*np.pi/3*rs**3*gen.DENS[gen.PHASE_MECH["SE"][1]]*1000*9.81
        for ta in ("AM_P","AM_S","SE"):
            ia=gen.TYPES.index(ta);ra=pp["d"][ta]/2;nu1=gen.PHASE_MECH[ta][0];nu2=gen.PHASE_MECH["SE"][0]
            es=1/((1-nu1**2)/gen.E_PHASE[ta]+(1-nu2**2)/gen.E_PHASE["SE"])
            rr=ra*rs/(ra+rs);ced=M[ia][se];delta=(3*np.pi*ced*np.sqrt(rr)/(2*es))**2
            mixbo[ta+"-SE"]=dict(ced_J_m3=ced,Bo_eq_over_SE_weight=ced*2*np.pi*rr*delta/ws)
        out["SE_pair_Bo_label"]=dict(BO_BASE=gen.BO_BASE,pairs=mixbo)
        # Real generator settings, synthetic meshes: E0's static reference grid is not the LC grid.
        prod=gen.plan(100000,cgf=151.4);rpm=gen.resolve_rpm(prod["R"])
        lcd=gen.deck(prod,rpm,8,seed=32452843,arm="LC")
        e0d=gen.deck(prod,rpm,0,seed=32452843,arm="E0")
        camp,base,U,g,binary=fixture(td/"production_grid",deck=lcd);rc=receipt(base)
        erun=rundir(td,"E0_static",e0d);(erun/"log.lmp").write_text(BANNER+"\n")
        esp=cv.deck_walls(e0d);est=mi.planned_t0(mi.deck_plan(str(erun/"in.mixer")))
        N,C,owners,_=cv.container_at(str(erun),esp,est)
        TT=cv.read_stl(erun/"Drum.stl")*esp["meshes"]["Drum"][1]
        u=TT.reshape(-1,3)[0].copy();u[0]=0;u/=np.linalg.norm(u)
        dots=N@u;rr=75.7e-6
        rho=min((C[j]-rr*(1-.005))/(-dots[j]) for j in range(len(N)) if dots[j]<-1e-6)
        PP=np.array([rho*u]);dump(erun/"post"/f"mix_{est}.liggghts",est,dat(PP,rr))
        truth=float(cv.wall_overlaps(PP,np.array([rr]),N,C)[0][0])
        out["E0_static_contract"]=dict(receipt_pass=rc["passed"],LC_grid=rc["dump_every"],E0_t0=est,E0_rotation_start=esp["moves"]["Drum"]["start_step"],
            true_static_overlap=truth,without_receipt=brief(cv.check_window(str(erun))),
            with_LC_receipt=brief(cv.check_window(str(erun),phase_receipt=str(base/"receipt.json"))))
    (ROOT/"review_round4_output.json").write_text(json.dumps(clean(out),ensure_ascii=False,indent=2,allow_nan=False),encoding="utf-8")
    print(json.dumps(clean({k:v for k,v in out.items() if not k.startswith("reader_") and not k.endswith("_receipt") and "stdout" not in v}),ensure_ascii=False,indent=2,allow_nan=False))
    print("CLI",[(k,v["rc"]) for k,v in out.items() if isinstance(v,dict) and "rc" in v])
    print("receipts",[(k,v["passed"]) for k,v in out.items() if k.endswith("_receipt")])
    print("reader",[(k,v.get("refused") or v.get("planned")) for k,v in out.items() if k.startswith("reader_")])
    checks=dict(
        normal=out["normal_receipt"]["passed"], missing_A_closed=not out["no_A_receipt"]["passed"],
        missing_B_closed=not out["no_B_after_restart_receipt"]["passed"],
        nan_B_false_green=out["nan_B_receipt"]["passed"] and out["nan_B_receipt"]["consumer_accepted"],
        residual_false_green=out["ignored_shape_residual_false_pass"]["true_overlap"]>.01 and out["ignored_shape_residual_false_pass"]["result"]["verdict"]=="PASS",
        degenerate_caps_false_green=out["degenerate_front_false_pass"]["verdict"]=="PASS",
        missing_caps_closed=out["old_missing_caps_closed"]["verdict"]!="PASS",
        missing_ref_closed="refused" in out["reader_no_ref_t0"],
        extra_excluded=out["reader_extra"]["planned"]["M_final"]==.45 and bool(out["reader_extra"]["tech"]),
        duplicate_excluded=out["reader_duplicate"]["planned"]["M_final"] is None,
        copied_seeds_closed=out["copied_seeds_closed"]["rc"]==1,
        target_not_wired=out["launcher_target_without_expect"]["rc"]==0 and out["launcher_target_with_expect"]["rc"]==1,
        smoke_not_bound=out["foreign_wrong_grid_smoke_gate"]["rc"]==0,
        interval_correct=not out["interval_independent_grid_check"]["violations"])
    out["probe_assertions"]=checks
    (ROOT/"review_round4_output.json").write_text(json.dumps(clean(out),ensure_ascii=False,indent=2,allow_nan=False),encoding="utf-8")
    assert all(checks.values()),checks
if __name__=="__main__":main()
