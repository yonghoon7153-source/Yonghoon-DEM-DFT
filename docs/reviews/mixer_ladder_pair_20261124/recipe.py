"""Generate two intermediate levels from the B2 executable deck and original matrix routines."""
import hashlib
import json
import math
from pathlib import Path
import re
import runpy

LEVELS = {"L020":.20, "L050":.50}
U_DECK = "b37974e5c0674947912e932c55517e9e84243293f29257183f8f70cc032f2fd7"
C_DECK = "d36d199388243ccd630cbd346cbcdb6f37bf8bb92ae9c8f4e73e2e98597a6a3e"
GD = "dc253bc8319077bc1e41635ae30ec588eb4a14c899db075e064192c4ef9cf6f7"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def generate(generator, u_raw, c_raw, u_meta):
    if [digest(x) for x in (generator.read_bytes(),u_raw,c_raw)] != [GD,U_DECK,C_DECK]:
        raise ValueError("B2 reference identities")
    g=runpy.run_path(str(generator))
    g["set_phases"](("AM_P","AM_S","SE"))
    plan=g["plan"](100000,cgf=151.4,stiffen_se=20.,dens_gen="lab20261014")
    meta=json.loads(u_meta)
    if meta["deck_sha256"] != U_DECK or meta["seed"] != 32452843 or meta["steps"]["dump_every"] != 32976:
        raise ValueError("B2-U reference metadata")
    names=["AM_P","AM_S","SE","WALL"]
    def executable(raw):
        return [l for l in raw.decode().splitlines() if l.strip() and not l.lstrip().startswith("#")]
    u,c=executable(u_raw),executable(c_raw)
    idx,=[i+1 for i,line in enumerate(u) if line.startswith("fix mC all property/global cohesionEnergyDensity")]
    if u[:idx]+u[idx+4:] != c[:idx]+c[idx+4:]:
        raise ValueError("unexpected U/C executable difference")
    wall=g["gm_wall_from_ncm"](.1)
    def matrices(ratio):
        spec=g["gm_arm"]({"AM_P":ratio,"AM_S":ratio,"SE":1.},gamma_wall=wall,bo_se=21.244)
        soft=g["ced_matrix_geomean"](spec, plan["d"],dens=meta["dens_g_cm3"])
        stiff=g["hold_bo_pairwise_matrix"](soft,g["E_PHASE"],plan["E"])
        g["_assert_ceiling_pairwise"]("ladder",stiff,plan["d"],plan["E"])
        return soft,stiff
    def lines(matrix):
        return ["    "+" ".join(f"{v:.6g}" for v in row)+(" &" if n<3 else "") for n,row in enumerate(matrix)]
    for ratio,reference in ((.1,u),(1.,c)):
        if lines(matrices(ratio)[1]) != reference[idx:idx+4]:
            raise ValueError("generator matrix does not replay endpoint exactly")
    result={}
    u_pairs={(p["i"],p["j"]):p for p in meta["pairs"]}
    for level,ratio in LEVELS.items():
        soft,stiff=matrices(ratio)
        pairs=g["stiffness_rows"](plan["d"],soft,stiff,g["E_PHASE"],plan["E"])
        for row in pairs:
            i,j=row["i"],row["j"]
            ref=u_pairs[i,j]
            # The registered geometric-mean law scales each AM endpoint by sqrt(ratio/0.1).
            for field in ("F0_N","F0_soft_N"):
                if ref[field] is not None:
                    exponent=(int(i<=2)+int(j<=2))/2
                    if not math.isclose(row[field],ref[field]*(ratio/.1)**exponent,rel_tol=1e-12):
                        raise ValueError("nominal force differs from B2 geometric mixing")
        text=("# DEVELOPMENT_ONLY MIXER_B2_"+level+"; AM/SE="+str(ratio)+"; wall/SE=0.00256; Bo_SE=21.244\n"+
              "\n".join(u[:idx]+lines(stiff)+u[idx+4:])+"\n").encode()
        new=dict(meta,schema="mixer_ladder_deck/1",arm="MIXER_B2_"+level,arm_desc="Development ratio ladder",
                 registered=None,pairs=pairs,deck_bytes=len(text),deck_sha256=digest(text),
                 template_deck_sha256=U_DECK,recipe_sha256=digest(Path(__file__).read_bytes()),
                 development_contract="mixer_b2_prereg_20261124/ladder",
                 adhesion_rule=dict(rule="geomean",gamma=dict(AM_P=ratio,AM_S=ratio,SE=1.),
                     gamma_wall=wall,bo_se=21.244,wall_reference_rho=.1))
        result[level]=(text,(json.dumps(new,indent=2,ensure_ascii=False)+"\n").encode())
    return result
