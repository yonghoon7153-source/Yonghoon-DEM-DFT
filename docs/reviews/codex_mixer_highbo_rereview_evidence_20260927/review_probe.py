"""Independent adversarial probes. Synthetic files only; no DEM or campaign launch."""
import sys, os, json, math, re, shutil, tempfile
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import make_mixer_deck as gen
import mixer_deck_diff as diff
import check_contact_validity as cv
import measure_mixing_index as mi

def dump(path, step, D):
    keys = ["id", "type", "x", "y", "z", "radius"]
    rows = zip(*(D[k] for k in keys))
    head = (f"ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(D['id'])}\n"
            "ITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\nITEM: ATOMS " + " ".join(keys) + "\n")
    Path(path).write_text(head + "\n".join(" ".join(format(float(x), ".17g") for x in row) for row in rows) + "\n", encoding="utf-8")

def write_case(base, name, deck):
    d = Path(base) / name
    (d/"post").mkdir(parents=True)
    (d/"in.mixer").write_text(deck, encoding="utf-8")
    for nm in ("Drum", "Front", "Back"):
        shutil.copyfile(ROOT/f"dem_scripts/mixer_20260919/{nm}.stl", d/f"{nm}.stl")
    return d

def mutate_ced(deck, mutate):
    cmds = diff.logical_commands(deck)
    lines = deck.split("\n")
    for at, block in cmds:
        tok = diff._tokens(block)
        if tok[:1] == ["fix"] and len(tok)>4 and tok[4]=="cohesionEnergyDensity":
            n = int(tok[6]); mat = np.array(list(map(float,tok[7:]))).reshape(n,n)
            mat = mutate(mat.copy())
            lines[at:at+len(block)] = [" ".join(tok[:7]+[format(x,".17g") for x in mat.ravel()])]
            return "\n".join(lines)
    raise ValueError("no CED")

def compact_window(w):
    return {k:w[k] for k in ("verdict","pp_max","wall_max","phase_status","phase","reject","tech","n_frames")}

def main():
    out = {}
    p = gen.plan(100000, cgf=151.4)
    rpm = gen.resolve_rpm(p["R"])
    lc = gen.deck(p, rpm, 8, seed=32452843, arm="LC")
    lh = gen.deck(p, rpm, 8, seed=32452843, arm="LH")
    out["matrix_baseline"] = diff.diff_decks(lc,lh,"B")["verdict"]
    def asym(M): M[0,1] *= 2; return M
    def nanse(M): M[2,2] = np.nan; return M
    def negative(M): M[0,0] *= -1; return M
    out["matrix_mutants"] = {k:diff.diff_decks(lc, mutate_ced(lh,f),"B")
                              for k,f in (("asymmetric_new",asym),("SE_SE_NaN",nanse),("negative_AM",negative))}
    out["matrix_header_mutant"] = diff.diff_decks(lc,lh.replace("fix mC all property/global","fix bogus nonexisting property/global"),"B")
    spec = cv.deck_walls(lh)
    plan_dt = spec["dt"]
    with tempfile.TemporaryDirectory(prefix="mhr_probe_") as td:
        geometry = write_case(td,"geometry",lh)
        T = cv.read_stl(geometry/"Drum.stl") * spec["meshes"]["Drum"][1]
        N,C = cv._planes(T,T.reshape(-1,3).mean(0))
        nf = len(C); facet = 2*np.pi/nf
        radius = p["d"]["SE"]/2
        apo = float(C.mean())
        out["geometry"] = dict(n_facets=nf,n_triangles=len(T),apo=apo,facet_deg=float(np.degrees(facet)),
                               sagitta_m=float(apo/np.cos(facet/2)-apo),r_SE=radius,
                               dt=plan_dt,rotation_start=spec["moves"]["Drum"]["start_step"])
        de = mi.deck_plan(geometry/"in.mixer")["dump_every"]
        t0 = (spec["moves"]["Drum"]["start_step"]//de)*de
        steps = [t0+i*de for i in range(7)]
        for name, true_extra, overlap in (("wrong_phase_false_pass",facet/2,0.02),
                                          ("right_phase_false_tech",0.0,0.005)):
            run = write_case(td,name,lh)
            truth=[]
            for st in steps:
                sched=cv.mesh_angle(spec,"Drum",st)
                # Exactly on the actual face centres. Phase truth is prescribed independently.
                P0 = -(C-radius+overlap*radius)[:,None]*N
                R=cv._rot(np.array([1.,0,0]),sched+true_extra)
                P=P0@R.T
                rr=np.full(nf,radius)
                Nt=N@R.T
                wr,_=cv.wall_overlaps(P,rr,Nt,C)
                truth.append(float(wr.max()))
                D=dict(id=np.arange(1,nf+1),type=np.full(nf,3),x=P[:,0],y=P[:,1],z=P[:,2],radius=rr)
                dump(run/"post"/f"mix_{st}.liggghts",st,D)
            w=cv.check_window(str(run),n_expected=nf)
            out[name]=dict(actual_max_overlap=max(truth),phase_truth_minus_sched_deg=float(np.degrees(true_extra)),
                           result=compact_window(w))
        # Phase counts and total IDs do not detect IDs exchanging phases, or a radius change.
        run=write_case(td,"identity",lh)
        D=dict(id=np.arange(1,5), type=np.array([1,2,3,3]),
               x=np.array([-.001,.001,-.001,.001]),y=np.array([-.004,-.004,.004,.004]),z=np.zeros(4),
               radius=np.full(4,1e-4))
        for st in steps:
            D2={k:v.copy() for k,v in D.items()}
            if st>t0:
                D2["type"][[0,1]]=D2["type"][[1,0]]
                D2["radius"][2]*=0.5
            dump(run/"post"/f"mix_{st}.liggghts",st,D2)
        out["identity_type_radius_mutant"]=compact_window(cv.check_window(str(run),n_expected=4))
        # Contract checker sees all supplied snapshots, not the steps between them.
        run2=write_case(td,"missing_frame",lh)
        for st in (steps[0],steps[2]):
            dump(run2/"post"/f"mix_{st}.liggghts",st,D)
        out["contact_missing_frame"]=compact_window(cv.check_window(str(run2),n_expected=4))
        hidden=np.c_[D["x"],D["y"],D["z"]]
        hidden[0,0]=0.0
        hidden[1,0]=1.98e-4
        _,hidden_rel,_=cv.contacts(hidden,D["radius"],types=D["type"])
        out["contact_missing_frame"]["unsaved_instant_overlap"]=float(hidden_rel.max())

        # Small deterministic reader clouds, not mechanical simulation states.
        def cloud(kind):
            ys=[];zs=[];ts=[];xs=[]
            for j,(y,z) in enumerate([(-.01,-.01),(-.01,.01),(.01,-.01),(.01,.01)]):
                for k in range(24):
                    ys.append(y);zs.append(z);xs.append((k-12)*1e-5)
                    if kind=="seg": typ=1 if j<2 else 3
                    elif kind=="ref": typ=1 if k<(6 if j<2 else 18) else 3
                    else: typ=1 if k<(3 if j<2 else 21) else 3
                    ts.append(typ)
            return dict(id=np.arange(1,97),type=np.array(ts),x=np.array(xs),y=np.array(ys),z=np.array(zs),radius=np.full(96,1e-5))
        # 25 samples/revolution and 8 planned revolutions; t0=200.
        dk=("timestep 0.001\nrun 1\nrun 100\nrun 100\n"
            "dump dmp all custom 40 post/mix_*.liggghts id type x y z radius\n"
            "fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1 0 0 period 1.00001\nrun 8000\n")
        ref=write_case(td,"ref",dk); dump(ref/"post"/"mix_200.liggghts",200,cloud("ref"))
        run=write_case(td,"smoke",dk)
        for i in range(26):
            st=200+40*i
            dump(run/"post"/f"mix_{st}.liggghts",st,cloud("seg") if i==0 else cloud("mid"))
        r=mi.analyse(str(run),str(ref),.02,cells=2,x_cells=1)
        out["bin0_smoke"]=dict(planned=r["planned"],tech=r["tech"],bins=r["by_rev"])
        # Missing entire middle including most of previous bin: gap starts too early for the test.
        run=write_case(td,"missing_prev",dk)
        for i in [0,*range(174,201)]:
            st=200+40*i
            dump(run/"post"/f"mix_{st}.liggghts",st,cloud("seg") if i==0 else cloud("mid"))
        r=mi.analyse(str(run),str(ref),.02,cells=2,x_cells=1)
        out["missing_previous_bin"]=dict(planned=r["planned"],tech=r["tech"],gaps=r["dump_gaps"],
                                          bins={k:v["n"] for k,v in r["by_rev"].items()})
        # Missing final planned sample but final bin endpoint is inside one-interval tolerance.
        run=write_case(td,"missing_last",dk)
        for i in range(200):
            st=200+40*i
            dump(run/"post"/f"mix_{st}.liggghts",st,cloud("seg") if i==0 else cloud("mid"))
        r=mi.analyse(str(run),str(ref),.02,cells=2,x_cells=1)
        out["missing_last_sample"]=dict(planned=r["planned"],tech=r["tech"],last_step=r["rows"][-1]["step"])

    # Per-phase volume retention does not bound unweighted cell variance error.
    ys=[];zs=[];xs=[];types=[];rads=[]
    # Two high-density cells with 100 AM + 100 SE each.
    for y,z in [(-.75,-.75),(-.25,-.75)]:
        for k in range(200):
            ys.append(y);zs.append(z);xs.append(k*1e-5);types.append(1 if k<100 else 3);rads.append(1e-6)
    # Eight sparse pure AM/SE cells, only one small grain in each.
    coords=[(.25,-.75),(.75,-.75),(-.75,-.25),(-.25,-.25),(.25,-.25),(.75,-.25),(-.75,.25),(-.25,.25)]
    for j,(y,z) in enumerate(coords):
        ys.append(y);zs.append(z);xs.append(0);types.append(1 if j<4 else 3);rads.append(1e-6)
    D=dict(id=np.arange(1,len(xs)+1),type=np.array(types),x=np.array(xs),y=np.array(ys),z=np.array(zs),radius=np.array(rads))
    st=mi.cell_stats(D,1,cells=4,x_cells=1,n_min=20)
    out["retention_not_variance_bound"]={k:v for k,v in st.items() if k!="p"}
    out["phase_mean_can_hide_bad_frames"]={"25_frame_retention":float(np.mean([0.,0.]+[1.]*23))}
    vtip = math.sqrt(gen.FR_ANCHOR*9.81*p["R"])
    collision = {}
    for a,b in (("SE","SE"),("AM_P","SE"),("SE","WALL")):
        ra=p["d"][a]/2
        nua,mata=gen.PHASE_MECH[a]
        ma=4*math.pi*ra**3*(gen.DENS[mata]*1000)/3
        if b=="WALL":
            rb=float("inf"); nub=gen.WALL_NU; mb=float("inf")
        else:
            rb=p["d"][b]/2
            nub,matb=gen.PHASE_MECH[b]
            mb=4*math.pi*rb**3*(gen.DENS[matb]*1000)/3
        Re=1/(1/ra+1/rb); me=1/(1/ma+1/mb)
        Ee=1/((1-nua**2)/gen.E_PHASE[a]+(1-nub**2)/gen.E_PHASE[b])
        h=4*Ee*math.sqrt(Re)/3
        delta=(5*me*vtip*vtip/(4*h))**.4
        th=2.87*(me**2/(Re*Ee**2*vtip))**.2
        collision[a+"-"+b]={"elastic_no_damping_delta_over_rmin":delta/min(ra,rb),"hertz_time_us":th*1e6}
    out["K1_collision_scale"]={"tip_speed_m_s":vtip,"dump_interval_s":de*plan_dt,
                                "pairs":collision,"note":"Two-body elastic Hertz estimate, not measured maxima or a rigorous velocity bound."}
    dv=np.array([-.3,.9,.3])
    out["small_difference_label"]={"paired_d":dv.tolist(),"mean":float(dv.mean()),
                                    "SE":float(dv.std(ddof=1)/np.sqrt(3)),
                                    "passes_abs_mean_le_SE":bool(abs(dv.mean())<=dv.std(ddof=1)/np.sqrt(3))}
    assert out["wrong_phase_false_pass"]["result"]["verdict"]=="PASS"
    assert len(out["wrong_phase_false_pass"]["result"]["phase"])==5
    assert out["right_phase_false_tech"]["result"]["verdict"]=="TECH"
    assert out["bin0_smoke"]["tech"]
    assert out["missing_previous_bin"]["planned"]["flat"] is True and not out["missing_previous_bin"]["tech"]
    assert all(x["verdict"]=="PASS" for x in out["matrix_mutants"].values())
    assert st["am_vol_kept"]>.9 and st["se_vol_kept"]>.9 and st["s2"]==0 and st["s2_all"]>.19
    def clean(x):
        if isinstance(x,dict): return {k:clean(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)): return [clean(v) for v in x]
        if isinstance(x,(float,np.floating)) and not np.isfinite(x): return str(x)
        if hasattr(x,"item"): return x.item()
        return x
    print(json.dumps(clean(out),ensure_ascii=False,indent=2,allow_nan=False))

if __name__=="__main__":
    main()
