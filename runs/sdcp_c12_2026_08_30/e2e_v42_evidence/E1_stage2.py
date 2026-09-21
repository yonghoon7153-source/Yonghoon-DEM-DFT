import hashlib, json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, "/home/user/Yonghoon-DEM-DFT/tools/sdcp")
import vasp_handoff_bundle as V
S = Path(sys.argv[1]); base = S / "e1"; cur = base / "cur/sdcp_c12_v42"; prev = base / "prev/sdcp_c12_v42"
binp = base / "bin"; NN = V.KPAR_VAL * V.NCORE_VAL
Z = Path("/home/user/Yonghoon-DEM-DFT/runs/sdcp_c12_2026_08_30/sdcp_c12_v42.zip"); zsha = hashlib.sha256(Z.read_bytes()).hexdigest()
# 2단계 잡 에너지 (실물 근처 값 — 실측이 아니라 stub)
E1 = json.load(open(base / "E1_ENERGY.json"))
E1.update({"prospective/ptfe_c10__b00__afm2424_net4": -1123.60, "prospective/ptfe_c10__b52__afm2424_pm1": -1123.40,
           "prospective/ptfe_c10__b52__afm2424_net4": -1123.41, "prospective/sdcp_neutral__b00__afm2424_net4": -1151.30,
           "prospective/sdcp_neutral__b12__afm2424_pm1": -1151.00, "prospective/sdcp_neutral__b12__afm2424_net4": -1151.01,
           "refs/clean_slab__afm2424_net4": -944.95})
(base / "E1_ENERGY.json").write_text(json.dumps(E1))
env = {k: v for k, v in os.environ.items() if not k.startswith(("SLURM_", "OMPI_", "PMIX_"))}; env.pop("NODE_MEM_GB", None)
env.update({"PATH": f"{binp}:{env.get('PATH','')}", "PP": str(base / "pp"), "POTCAR_ALLOWLIST": str(base / "site_allow.txt"),
            "VASP_LAUNCHER_KIND": "mpirun", "LAUNCHER_BIN": str(binp / "mpirun"), "VASP_NPROC": str(NN),
            "VASP_EXE": str(binp / "vasp_std"), "BUNDLE_ZIP_SHA256": zsha, "EXPECT_ZIP_SHA256": zsha,
            "EXPECT_MANIFEST_SHA256": hashlib.sha256((cur / "MANIFEST.json").read_bytes()).hexdigest(),
            "PYTHONIOENCODING": "utf-8", "VASP_NODES": str(NN), "VASP_HOSTFILE": str(base / "hosts.txt"),
            "JOBS_PARALLEL": "1", "E1_ENERGY": str(base / "E1_ENERGY.json"), "STUB_LOG": str(base / "stub2.log"),
            "SKIP_COMPLETE": "1", "CONTINUE_FROM": str(prev)})     # ← 셸에 남아 있는 상태 그대로 (2단계 내성 시험)
r = subprocess.run(["bash", "run_staged.sh", "2"], cwd=cur, env=env, capture_output=True, text=True, timeout=1800)
(base / "run_stage2.log").write_text(r.stdout + r.stderr)
print("RUN_STAGED_2_RC =", r.returncode)
