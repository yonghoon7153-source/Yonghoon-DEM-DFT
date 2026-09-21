"""E1: 실물 v42 번들 + 가짜 PP 트리 + stub VASP/mpirun 으로 run_staged.sh 1 을 **끝까지** 돌린다 (CONTINUE_FROM 승계).
prev = v42 를 풀고 SEAL 을 단독으로 먼저 만든 뒤(생산 전) 회수본 7잡 산출물을 넣은 extraction.
receipt 의 실행파일·launcher·POTCAR 열은 실물 값이라 stub 봉인과 다르므로 **그 열만** stub 값으로 바꾼다
(문서화된 픽스처 적응 — 이 컨테이너에 실물 VASP/POTCAR 가 없다)."""
import hashlib, json, os, shutil, subprocess, sys, zipfile, gzip, re
from pathlib import Path
sys.path.insert(0, "/home/user/Yonghoon-DEM-DFT/tools/sdcp")
S = Path(sys.argv[1]); REPO = Path("/home/user/Yonghoon-DEM-DFT")
Z = REPO / "runs/sdcp_c12_2026_08_30/sdcp_c12_v42.zip"
RAW = REPO / "db/properties/sdcp_c12_v41_partial_raw"
import vasp_handoff_bundle as V   # STUB/FAKE 문자열·POTCAR_SPEC·KPAR/NCORE 만 쓴다
base = S / "e1"; shutil.rmtree(base, ignore_errors=True); base.mkdir()
for nm in ("cur", "prev"):
    with zipfile.ZipFile(Z) as z: z.extractall(base / nm)
cur, prev = base / "cur/sdcp_c12_v42", base / "prev/sdcp_c12_v42"
man = json.loads((cur / "MANIFEST.json").read_text())
spec = man["potcar_spec"]
# 가짜 PP 트리 + allowlist (selftest _runner_e2e 와 같은 형식)
pp = base / "pp"; lines = []
for el, var in sorted(spec.items()):
    (pp / var).mkdir(parents=True, exist_ok=True); f = pp / var / "POTCAR"
    f.write_text("  PAW_PBE %s 01Jan2000\n   TITEL  = PAW_PBE %s 01Jan2000\n   SHA256 = deadbeef %s\n   END of PSCTR\n" % (var, var, var))
    lines.append("%s  %s" % (hashlib.sha256(f.read_bytes()).hexdigest(), f))
allow = base / "site_allow.txt"; allow.write_text("\n".join(lines) + "\n")
binp = base / "bin"; binp.mkdir()
# stub vasp_std: 빈 INCAR(봉인 프로브) → 배너만 · 실제 상 → _fake_phase 로 실물 모양 OUTCAR (에너지는 E1_ENERGY.json)
real_E = {}
for j in ("prospective/ptfe_c10__b00__afm2424_pm1", "prospective/sdcp_neutral__b00__afm2424_pm1", "refs/clean_slab__afm2424_pm1",
          "refs/mol__ptfe_c10__box24", "refs/mol__sdcp_neutral__box24"):
    t = gzip.open(RAW / j / "static/OUTCAR.gz").read().decode("utf-8", "replace")
    real_E[j] = float(re.findall(r"energy\(sigma->0\)\s*=\s*(-?[\d.]+)", t)[-1])
emap = {"vacconv/ptfe_c10__b00__afm2424_pm1__c2": real_E["prospective/ptfe_c10__b00__afm2424_pm1"],
        "vacconv/sdcp_neutral__b00__afm2424_pm1__c2": real_E["prospective/sdcp_neutral__b00__afm2424_pm1"],
        "vacconv/clean_slab__afm2424_pm1__c2": real_E["refs/clean_slab__afm2424_pm1"],
        "refs/mol__ptfe_c10__box24__nzmag": real_E["refs/mol__ptfe_c10__box24"] + 0.001,
        "refs/mol__sdcp_neutral__box24__nzmag": real_E["refs/mol__sdcp_neutral__box24"] + 0.001}
(base / "E1_ENERGY.json").write_text(json.dumps(emap))
(binp / "vasp_std").write_text(r'''#!/usr/bin/env bash
set -u
if [ ! -s INCAR ]; then
  echo ' running on    1 total cores'; echo ' distrk:  each k-point on    1 cores,    1 groups'
  echo ' distr:  one band on    1 cores,    1 groups'; echo ' using from now: INCAR'
  echo ' vasp.5.4.4.18Apr17-6-g9f103f2a35 (build stub) complex'; exit 0
fi
[ -n "${STUB_LOG:-}" ] && echo "$(basename "$(dirname "$PWD")")/$(basename "$PWD")" >> "$STUB_LOG"
cp POSCAR CONTCAR; printf '   1 F= -1.0 E0= -1.0\n' > OSZICAR
python3 - <<'PY'
import json, os, sys, shutil
from pathlib import Path
sys.path.insert(0, "/home/user/Yonghoon-DEM-DFT/tools/sdcp")
import vasp_handoff_bundle as V
jd = Path(os.getcwd()).parent; root = jd.parent.parent
key = jd.relative_to(root).as_posix()
E = json.load(open(os.environ["E1_ENERGY"]))[key]
meta = json.load(open(jd / "job.json"))
prov = (jd / "POTCAR_PROVENANCE.json").read_bytes()     # _fake_phase 가 덮으므로 보존
V._fake_phase(jd, meta, E, V.POTCAR_SPEC)
(jd / "POTCAR_PROVENANCE.json").write_bytes(prov)
t = (jd / "static/OUTCAR").read_text()
t = t.replace(" vasp.6.4.2\n", " vasp.5.4.4.18Apr17-6-g9f103f2a35 (build stub) complex\n", 1)
(jd / "static/OUTCAR").write_text(t)
PY
exit 0
''')
(binp / "vasp_std").chmod(0o755)
(binp / "mpirun").write_text(V.FAKE_MPIRUN); (binp / "mpirun").chmod(0o755)
NN = V.KPAR_VAL * V.NCORE_VAL
(base / "hosts.txt").write_text("".join("e1-node%02d\n" % k for k in range(1, NN + 1)))
zsha = hashlib.sha256(Z.read_bytes()).hexdigest()
env = {k: v for k, v in os.environ.items() if not k.startswith(("SLURM_", "OMPI_", "PMIX_"))}
env.pop("NODE_MEM_GB", None)
env.update({"PATH": f"{binp}:{env.get('PATH','')}", "PP": str(pp), "POTCAR_ALLOWLIST": str(allow),
            "VASP_LAUNCHER_KIND": "mpirun", "LAUNCHER_BIN": str(binp / "mpirun"), "VASP_NPROC": str(NN),
            "VASP_EXE": str(binp / "vasp_std"), "BUNDLE_ZIP_SHA256": zsha, "EXPECT_ZIP_SHA256": zsha,
            "EXPECT_MANIFEST_SHA256": hashlib.sha256((cur / "MANIFEST.json").read_bytes()).hexdigest(),
            "PYTHONIOENCODING": "utf-8", "VASP_NODES": str(NN), "VASP_HOSTFILE": str(base / "hosts.txt"),
            "JOBS_PARALLEL": "1", "E1_ENERGY": str(base / "E1_ENERGY.json"), "STUB_LOG": str(base / "stub.log")})
# ── prev: 봉인을 **먼저** (생산 전) 만들고 나서 회수본 산출물을 넣는다 ──
r = subprocess.run(["bash", "SEAL_POTCAR_ROOT.sh"], cwd=prev, env=env, capture_output=True, text=True)
print("prev SEAL rc", r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1][:100])
assert (prev / "POTCAR_ROOT_SEAL.json").is_file()
pseal = json.loads((prev / "POTCAR_ROOT_SEAL.json").read_text())
exe_sha = hashlib.sha256((binp / "vasp_std").read_bytes()).hexdigest(); mpi_sha = hashlib.sha256((binp / "mpirun").read_bytes()).hexdigest()
done7 = ["prospective/ptfe_c10__b00__afm2424_pm1", "prospective/sdcp_neutral__b00__afm2424_pm1", "refs/clean_slab__afm2424_pm1",
         "refs/mol__ptfe_c10__box20", "refs/mol__ptfe_c10__box24", "refs/mol__sdcp_neutral__box20", "refs/mol__sdcp_neutral__box24"]
for j in done7:
    d = prev / j
    shutil.copy2(RAW / j / "_placement.tsv", d / "_placement.tsv")
    for f in sorted((RAW / j / "static").iterdir()):
        if f.name == "OUTCAR.gz":
            (d / "static/OUTCAR").write_bytes(gzip.open(f).read())
        else:
            shutil.copy2(f, d / "static" / f.name)
    shutil.copy2(d / "POTCAR", d / "static/POTCAR")
    asm = json.loads((d / "POTCAR_PROVENANCE.json").read_text())["assembled_sha256"]
    rows = []
    for ln in (RAW / j / "EXECUTABLE_RECEIPT.tsv").read_text().splitlines():
        c = ln.split("\t"); assert len(c) == 9
        c[2] = exe_sha; c[3] = str(binp / "vasp_std"); c[6] = str(binp / "mpirun"); c[7] = mpi_sha
        if c[1] != "_runner_start": c[8] = asm
        rows.append("\t".join(c))
    (d / "EXECUTABLE_RECEIPT.tsv").write_text("\n".join(rows) + "\n")
# mirae 실측 잔재: vacconv c2 의 qdel 잔재 (receipt 2행 + vasp.out · OUTCAR 없음)
c2 = prev / "vacconv/clean_slab__afm2424_pm1__c2"
shutil.copy2(prev / "refs/clean_slab__afm2424_pm1/EXECUTABLE_RECEIPT.tsv", c2 / "EXECUTABLE_RECEIPT.tsv")
(c2 / "static/vasp.out").write_text(" running on 64 total cores\n"); shutil.copy2(c2 / "POSCAR", c2 / "static/POSCAR")
# ── cur: 실물 러너 전체 경로 ──
env.update({"SKIP_COMPLETE": "1", "CONTINUE_FROM": str(prev)})
r = subprocess.run(["bash", "run_staged.sh", "1"], cwd=cur, env=env, capture_output=True, text=True, timeout=1800)
(base / "run_stage1.log").write_text(r.stdout + r.stderr)
print("RUN_STAGED_1_RC =", r.returncode)
