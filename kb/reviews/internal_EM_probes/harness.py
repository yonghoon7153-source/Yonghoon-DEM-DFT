"""Independent-review probe harness (scratch only). Builds an a5 package with an injected registry + fake W0
(same way the module selftest does), then lets probes run the generated run_a5.sh against the module's fake VASP."""
import json
import os
import shutil
import subprocess
import sys
import tarfile

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/Yonghoon-DEM-DFT/tools/wad")
import build_a5_vasp_package as B  # noqa: E402

V = B.V
SCR = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def setup(T, cap_h=None):
    os.makedirs(T, exist_ok=True)
    potd = os.path.join(T, "pot")
    titels = {"Li_sv": "PAW_PBE Li_sv 10Sep2004", "P": "PAW_PBE P 06Sep2000", "S": "PAW_PBE S 06Sep2000", "Cl": "PAW_PBE Cl 06Sep2000", "Ag": "PAW_PBE Ag 02Apr2005"}
    zval = {"Li_sv": 3.0, "P": 5.0, "S": 6.0, "Cl": 7.0, "Ag": 11.0}
    sp_sha = {}
    for sp, t in titels.items():
        os.makedirs(os.path.join(potd, sp), exist_ok=True)
        pp = os.path.join(potd, sp, "POTCAR")
        B._write(pp, f"  PAW_PBE {sp}\n   VRHFIN =x\n   LEXCH  = PE\n   TITEL  = {t}\n   POMASS =    1.0; ZVAL   =   {zval[sp]:.1f}    mass and valenz\n")
        sp_sha[sp] = B._sha(pp)
    reg = {"schema": B.R2.REG_SCHEMA, "titel": titels, "species_sha256": sp_sha,
           "vasp_version": "vasp.5.4.4.18Apr17-6-g9f103f2a35 (build Aug 19 2022 11:57:46) complex", "restart_read_regex": "the WAVECAR file was read successfully"}
    w0p = os.path.join(T, "round2pkg", "run", "V5_s_outer_A_G4_e70_far_a4_a4", "stageA", "WAVECAR")
    os.makedirs(os.path.dirname(w0p), exist_ok=True)
    B._fake_wavecar(w0p)
    w0 = {"sha256": B._sha(w0p), "size": os.path.getsize(w0p), "NKPTS": "4", "NBANDS": "872", "ENCUT": "650.0"}
    pkg = os.path.join(T, "pkg")
    old = B.CAP_H
    if cap_h is not None:
        B.CAP_H = cap_h
    try:
        meta, msha = B.build(pkg, registry=(reg, "c" * 64), w0=w0, check_decision=False)
    finally:
        B.CAP_H = old
    fake = os.path.join(T, "fake_vasp.py")
    B._write(fake, B.FAKE_VASP5)
    return {"T": T, "pot": potd, "reg": reg, "w0p": w0p, "w0": w0, "pkg": pkg, "msha": msha, "fake": fake}


def run_pkg(E, name, plan, w0path=None, env_extra=None, args=(), fresh=True, cwd=None, vasp_cmd=None):
    w = os.path.join(E["T"], "w_" + name)
    if fresh:
        shutil.rmtree(w, ignore_errors=True)
        shutil.copytree(E["pkg"], w)
    pf = os.path.join(E["T"], f"plan_{name}.json")
    B._write(pf, json.dumps(plan))
    env = {**os.environ, "VASP_CMD": vasp_cmd or f"{PY} -B {E['fake']}", "POTCAR_DIR": E["pot"],
           "W0_WAVECAR": w0path if w0path is not None else E["w0p"], "FAKE_PLAN": pf, "FAKE_PKG": w, "WATCH_S": "1", **(env_extra or {})}
    p = subprocess.run(["bash", os.path.join(w, "run_a5.sh"), *args], cwd=cwd or w, env=env, capture_output=True, text=True, timeout=900)
    return w, p.returncode, p.stdout + p.stderr


def chk(E, w):
    ex = os.path.join(E["T"], "ex_" + os.path.basename(w))
    shutil.rmtree(ex, ignore_errors=True)
    os.makedirs(ex)
    with tarfile.open(os.path.join(w, "a5_return.tgz")) as tf:
        tf.extractall(ex, filter="data")
    return B.check_return(E["pkg"], ex, E["msha"], E["reg"])[1], ex


def dirs(w):
    run = os.path.join(w, "run")
    return sorted(x for x in os.listdir(run) if os.path.isdir(os.path.join(run, x))) if os.path.isdir(run) else []


def status_rows(w):
    p = os.path.join(w, "run", "status.tsv")
    return [ln.split("\t") for ln in open(p).read().splitlines()[1:]] if os.path.isfile(p) else []


def adopt(res, area=202.209896):
    prev = {"status": "SCF_NOT_CONVERGED", "a4_history": {"first_attempt": "SCF_NOT_CONVERGED", "r1": "SCF_NOT_CONVERGED", "a4": "SCF_NOT_CONVERGED"}}
    return V.adopt_a5(prev, res, area)
