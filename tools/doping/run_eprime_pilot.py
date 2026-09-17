#!/usr/bin/env python3
"""run_eprime_pilot.py — E′ 파일럿 **한 라운드** (카드 v5.2 동결 사양, 비준 2026-09-14).

    python3 tools/doping/run_eprime_pilot.py --dry_run
    python3 tools/doping/run_eprime_pilot.py --selftest
    python3 tools/doping/run_eprime_pilot.py --out_root ~/work/runs/eprime_2026_09_14 \
        --python $STORE/opt/miniforge3/envs/uma/bin/python

무엇을 하나
  **A단계 준비** 5구조 × 1 — 공통 총부피 V = 4066.479695 Å³(원본 셀 행렬)에서 고정셀 이온 완화
  (fmax 0.02 eV/Å). 다섯 입력 셀이 이미 같은 행렬이라 **부피를 새로 맞추지 않는다** —
  같은지 검사하고 다르면 시작하지 않는다.
  **B단계 MD** 5구조 × 3온도 × 2시드 = **30런**. Langevin NVT · dt 2 fs · friction 0.02 ·
  평형 5 ps · 생산 200 ps · save 100 fs · MSD 창 2–50 ps · UMA-s-1p1(omat).
  드라이버는 기존 것(`tools/modelc_v3/disorder_ensemble_diffusion.py`, 400 ps 캠페인이 쓴 것)을
  `--disorder_levels 0.0 --n_configs 1` 로 부른다 — 새 MD 코드를 쓰지 않는다.

비용 상한 (카드 §6 · **1저자 비준 2026-09-14: 소상한 10 · 총상한 120 GPU-h**)
  ① 총상한이 **첫 준비 계산 전에** 코드에 있다. ② 첫 런(H0 600 K seed 1)이 속도 시험이고
  거기에만 소상한이 붙는다. ③ 그 실측으로 남은 배치를 투영해 총상한과 비교한다.
  ④ 예상이 빗나가도 **누적 실사용 ≥ 총상한**이면 멈춘다.

⛔ 이 라운드가 **하지 않는 것**
  · 조건을 CLI 로 못 바꾼다 — 부피·셀·문턱·창·온도·시드·길이가 **코드에 동결**돼 있다.
    바꾸려면 코드를 고치고 커밋해야 한다(= 새 라운드 · 카드 개정).
  · **판정하지 않는다.** D_rel·ΔEa 집계와 자격 판정은 이 스크립트 밖이다
    (`msd_diffusive_check.aggregation_eligible`). 여기서는 런을 돌리고 사실만 적는다.
  · 실패했다고 창·시드·온도·부피를 넓히지 않는다. 한 부모가 준비에 실패하면 그 쌍만 미판정이고
    나머지는 진행한다.
  · 탄성을 계산하지 않는다 (카드: 보류).
  · 기존 out_root 를 재사용하지 않는다.
  · GPU 를 남과 나눠 쓰는지 **모른다** — 호출 전에 사람이 nvidia-smi 로 본다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# ── 동결 사양 ────────────────────────────────────────────────────────────────
#   출처: db/properties/cascade_rebuild_estimand_card_v5_Eprime_2026_09_13.json (ratified)
#         결정 D-2026-09-13-cascade-pilot-estimand-v5-eprime (active)
V_COMMON_A3 = 4066.479695
CELL_DIAG = (20.110191271466373, 20.110191271466373, 10.055095635733187)
V_TOL_A3 = 1e-3
CELL_TOL_A = 1e-9

STRUCTURES = ["H0_host", "P1_Al2O3_A", "P1_Al2O3_B", "P2_Al2S3_A", "P2_Al2S3_B"]
STRUCT_DIR = Path("db/structures/cascade_pilot")

PREP_FMAX = 0.02
PREP_STEPS = 3000

TEMPS = (600, 800, 1000)
SEEDS = (1, 2)
EQUILIB_PS = 5.0
PROD_PS = 200.0
DT_FS = 2.0
FRICTION = 0.02
SAVE_FS = 100.0
FIT_WINDOW_PS = (2.0, 50.0)
UMA_MODEL, UMA_TASK = "uma-s-1p1", "omat"

#: 속도 시험 런 — 이 하나에만 소상한이 붙는다 (카드 §6 ②)
PERF_RUN = {"structure": "H0_host", "temp": 600, "seed": SEEDS[0]}
PERF_SUBCAP_GPU_H = 10.0
TOTAL_CAP_GPU_H = 120.0

REPO = Path(__file__).resolve().parents[2]
MD_DRIVER = REPO / "tools" / "modelc_v3" / "disorder_ensemble_diffusion.py"


def sha256(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git_head() -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


# ── 입력 게이트 — 공통 부피·공통 셀을 **검사한다** (맞추지 않는다) ──────────────
def read_cell(path) -> tuple[list[list[float]], int]:
    """extxyz 머리에서 Lattice 3×3 과 원자수를 읽는다. 못 읽으면 ValueError."""
    txt = Path(path).read_text(encoding="utf-8", errors="ignore").split("\n")
    if len(txt) < 2:
        raise ValueError(f"{path}: 두 줄도 안 된다")
    try:
        n = int(txt[0].strip())
    except ValueError as e:
        raise ValueError(f"{path}: 첫 줄이 원자수가 아니다") from e
    m = re.search(r'Lattice="([^"]+)"', txt[1])
    if not m:
        raise ValueError(f"{path}: Lattice 가 없다 — 격자 없는 xyz 는 이 라운드가 받지 않는다")
    v = [float(x) for x in m.group(1).split()]
    if len(v) != 9:
        raise ValueError(f"{path}: Lattice 성분이 9개가 아니다 ({len(v)})")
    return [v[0:3], v[3:6], v[6:9]], n


def det3(A) -> float:
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def check_inputs(struct_dir=STRUCT_DIR, structures=STRUCTURES) -> tuple[list[dict], list[str]]:
    """→ (rows, violations). **위반이 하나라도 있으면 라운드를 시작하지 않는다.**

    ⛔ 여기서 부피를 '맞춰 주지' 않는다. 다섯 입력이 이미 같은 셀이라는 것이 카드의 전제이고,
      그 전제가 깨졌다면 그것은 고쳐서 계속할 일이 아니라 **보고할 발견**이다.
    """
    rows, bad = [], []
    for s in structures:
        p = Path(struct_dir) / f"{s}.xyz"
        if not p.is_file():
            bad.append(f"{s}: 구조 파일이 없다 ({p})")
            continue
        try:
            A, n = read_cell(p)
        except ValueError as e:
            bad.append(str(e))
            continue
        V = abs(det3(A))
        off = max(abs(A[i][j]) for i in range(3) for j in range(3) if i != j)
        diag_err = max(abs(A[i][i] - CELL_DIAG[i]) for i in range(3))
        if abs(V - V_COMMON_A3) > V_TOL_A3:
            bad.append(f"{s}: 부피 {V:.6f} ≠ 공통 {V_COMMON_A3} (Δ {V - V_COMMON_A3:+.2e} Å³)")
        if off > CELL_TOL_A or diag_err > 1e-6:
            bad.append(f"{s}: 셀 행렬이 동결값과 다르다 (비대각 {off:.2e} · 대각 오차 {diag_err:.2e})")
        rows.append({"structure": s, "path": str(p), "n_atoms": n,
                     "V_A3": V, "sha256": sha256(p)})
    return rows, bad


# ── 계획 — 속도 시험이 **맨 앞**이다 ─────────────────────────────────────────
def build_plan(out_root, python="python3", device="cuda") -> list[dict]:
    """준비 5 + MD 10 호출(=30런). MD 첫 호출은 속도 시험(H0 600 K seed 1) 하나뿐이다."""
    out_root = Path(out_root)
    plan: list[dict] = []
    for s in STRUCTURES:
        plan.append({
            "stage": "prep", "key": f"prep/{s}", "structure": s, "n_runs": 0,
            "cap_gpu_h": None,
            "cmd": [python, str(Path(__file__).resolve()), "--_prep_one",
                    "--_struct", s, "--out_root", str(out_root), "--device", device],
        })

    def md_cmd(s, temps, seed, tag):
        return [python, str(MD_DRIVER),
                "--v0_xyz", str(out_root / "prep" / f"{s}.prepared.xyz"),
                "--label", f"eprime_{s}",
                "--out_root", str(out_root / "md" / tag),
                "--disorder_levels", "0.0", "--n_configs", "1",
                "--temperatures", *[str(t) for t in temps],
                "--equilib_ps", str(EQUILIB_PS), "--prod_ps", str(PROD_PS),
                "--timestep_fs", str(DT_FS), "--friction", str(FRICTION),
                "--save_fs", str(SAVE_FS),
                "--fit_window_ps", str(FIT_WINDOW_PS[0]), str(FIT_WINDOW_PS[1]),
                "--seed", str(seed),
                "--uma_model", UMA_MODEL, "--uma_task", UMA_TASK,
                "--device", device]

    p = PERF_RUN
    tag = f"{p['structure']}__T{p['temp']}__s{p['seed']}"
    plan.append({"stage": "md_perf", "key": f"md/{tag}", "structure": p["structure"],
                 "temps": [p["temp"]], "seed": p["seed"], "n_runs": 1,
                 "cap_gpu_h": PERF_SUBCAP_GPU_H,
                 "cmd": md_cmd(p["structure"], [p["temp"]], p["seed"], tag)})

    for s in STRUCTURES:
        for seed in SEEDS:
            temps = [t for t in TEMPS
                     if not (s == p["structure"] and seed == p["seed"] and t == p["temp"])]
            if not temps:
                continue
            tag = f"{s}__s{seed}"
            plan.append({"stage": "md", "key": f"md/{tag}", "structure": s,
                         "temps": temps, "seed": seed, "n_runs": len(temps),
                         "cap_gpu_h": None, "cmd": md_cmd(s, temps, seed, tag)})
    return plan


def runs_remaining_from(plan, i) -> int:
    """`plan[i]` 부터 끝까지 남은 **런** 수. 게이트의 투영이 곱하는 값이다.

    ⚠ 이 함수가 따로 있는 이유: 2026-09-17 에 시험을 쓰면서 같은 식을 시험 쪽에
      **베껴 놓았더니**, 루프를 옛 코드(전체−1)로 되돌려도 시험이 초록이었다.
      시험이 대상이 아니라 자기 사본을 재고 있었다. 계산은 한 곳에만 둔다.
    """
    return sum(int(st.get("n_runs") or 0) for st in plan[i:])


def plan_run_count(plan) -> int:
    return sum(int(st.get("n_runs") or 0) for st in plan)


# ── 예산 — 누적을 파일에 남긴다 (세션이 끊겨도 상한이 산다) ────────────────────
def budget_load(out_root) -> dict:
    f = Path(out_root) / "budget.json"
    if f.is_file():
        return json.loads(f.read_text(encoding="utf-8"))
    return {"total_cap_gpu_h": TOTAL_CAP_GPU_H, "perf_subcap_gpu_h": PERF_SUBCAP_GPU_H,
            "used_gpu_h": 0.0, "steps": [],
            "⛔": "이 숫자는 1저자 비준값이다 (2026-09-14). 코드를 고쳐야 바뀐다."}


def budget_save(out_root, b) -> None:
    (Path(out_root) / "budget.json").write_text(
        json.dumps(b, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def gate_before(step, budget, projection=None) -> tuple[bool, str]:
    """이 스텝을 시작해도 되나 → (ok, 사유). **중단 사유를 문장으로 돌려준다.**

    ⚠ 준비(prep)도 예산을 쓴다. 그래서 누적 상한은 prep 에도 걸린다 — 카드 ①의
      '준비·MD·실패 시 소모분을 포함한 총 GPU-h' 그대로다.
    """
    used = float(budget.get("used_gpu_h") or 0.0)
    cap = float(budget.get("total_cap_gpu_h") or TOTAL_CAP_GPU_H)
    if used >= cap:
        return False, f"⛔ 누적 실사용 {used:.2f} ≥ 총상한 {cap:.0f} GPU-h — 즉시 중단 (카드 §6 ④)"
    if projection is not None and step.get("stage") == "md" and (used + projection) > cap:
        return False, (f"⛔ 투영 비용 {used:.2f} + {projection:.2f} = {used + projection:.2f} > "
                       f"총상한 {cap:.0f} GPU-h — **배치 시작 전** 중단 (카드 §6 ③)")
    return True, "ok"


def gate_after(step, gpu_h) -> tuple[bool, str]:
    """스텝이 끝난 뒤 소상한 검사. 속도 시험에만 걸린다 (카드 §6 ②)."""
    cap = step.get("cap_gpu_h")
    if cap is not None and gpu_h > cap:
        return False, (f"⛔ 속도 시험이 소상한을 넘었다: {gpu_h:.2f} > {cap:.0f} GPU-h "
                       f"— 그 런 중단·보고 (카드 §6 ②)")
    return True, "ok"


def project_remaining(perf_gpu_h, n_runs_remaining, perf_ps=EQUILIB_PS + PROD_PS) -> float:
    """속도 시험 실측 → 남은 런의 투영 비용 (GPU-h).

    ⛔ 이 함수가 못 하는 것: 구조·온도에 따른 차이를 모른다. 204/208 원자가 비슷하다고
      **가정**한다. 투영이 빗나가도 ④(누적 ≥ 상한)가 마지막 방어선이다.
    """
    if perf_gpu_h <= 0 or n_runs_remaining <= 0:
        return 0.0
    return perf_gpu_h * (EQUILIB_PS + PROD_PS) / perf_ps * n_runs_remaining


# ── A단계 준비 (이 파일이 직접 한다) ─────────────────────────────────────────
def prep_one(structure, out_root, device="cuda") -> dict:
    """공통 부피·고정셀 이온 완화 한 건 → prepared.xyz + 사실 기록 JSON.

    ⛔ `run_mlip_postproc.py --no_eos` 의 `stage1_before_eos.xyz` 를 쓰지 않는 이유:
      그 파일은 스스로 *"하류가 집어가면 안 된다"* 라고 적혀 있다. 이름과 경고가 금지하는
      파일을 하류 입력으로 쓰는 것이 바로 우리가 2026-09-13 에 여섯 건 잡은 '조용히 틀린
      경로' 다. 여기서는 **하류 입력으로 쓸 파일을 그 목적으로 만들고 그렇게 이름 붙인다.**
    """
    from ase.io import read, write
    from ase.optimize import FIRE
    from fairchem.core import FAIRChemCalculator, pretrained_mlip

    src = STRUCT_DIR / f"{structure}.xyz"
    A, _ = read_cell(src)
    V = abs(det3(A))
    if abs(V - V_COMMON_A3) > V_TOL_A3:
        raise SystemExit(f"⛔ {structure}: 입력 부피 {V:.6f} ≠ 공통 {V_COMMON_A3} — 시작하지 않는다")

    atoms = read(src)
    atoms.calc = FAIRChemCalculator(
        pretrained_mlip.get_predict_unit(UMA_MODEL, device=device), task_name=UMA_TASK)
    cell_before = atoms.get_cell().array.tolist()
    t0 = time.time()
    opt = FIRE(atoms, logfile="-")
    opt.run(fmax=PREP_FMAX, steps=PREP_STEPS)       # 셀 고정 — CellFilter 를 쓰지 않는다
    wall_s = time.time() - t0

    f = atoms.get_forces()
    fmax = float(max((sum(c * c for c in row)) ** 0.5 for row in f))
    cell_after = atoms.get_cell().array.tolist()
    moved = max(abs(cell_after[i][j] - cell_before[i][j]) for i in range(3) for j in range(3))
    if moved > CELL_TOL_A:
        raise SystemExit(f"⛔ {structure}: 완화 중 셀이 움직였다 ({moved:.2e} Å) — 고정셀이 아니다")

    d = Path(out_root) / "prep"
    d.mkdir(parents=True, exist_ok=True)
    xyz = d / f"{structure}.prepared.xyz"
    write(xyz, atoms, format="extxyz")
    rec = {
        "structure": structure, "input": str(src), "input_sha256": sha256(src),
        "V_A3": V, "n_atoms": len(atoms), "cell": cell_after,
        "fmax_target_eV_A": PREP_FMAX, "final_fmax_eV_A": fmax,
        "n_steps": int(opt.get_number_of_steps()), "max_steps": PREP_STEPS,
        "converged": bool(fmax <= PREP_FMAX),
        "E_eV": float(atoms.get_potential_energy()),
        "wall_s": wall_s, "gpu_h": wall_s / 3600.0,
        "prepared_xyz": str(xyz), "prepared_sha256": sha256(xyz),
        "uma": {"model": UMA_MODEL, "task": UMA_TASK, "device": device},
        "code_id": git_head(),
        "⚠_준비_상태_사실": ("이 기록은 준비 상태의 **사실**이다. 수렴 실패면 그 부모 쌍은 "
                             "미판정이고, 나머지 쌍은 그대로 진행한다 (카드 §6 중단 규칙)."),
    }
    (d / f"{structure}.prepared.json").write_text(
        json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[prep] {structure}: fmax {fmax:.4f} (target {PREP_FMAX}) · "
          f"steps {rec['n_steps']} · converged {rec['converged']} · {wall_s / 60:.1f} min")
    return rec


def prepared_ok(out_root, structure) -> bool:
    """MD 입력 자격 — 준비 기록이 있고 **수렴**했고 파일 해시가 맞는가."""
    j = Path(out_root) / "prep" / f"{structure}.prepared.json"
    if not j.is_file():
        return False
    try:
        rec = json.loads(j.read_text(encoding="utf-8"))
    except ValueError:
        return False
    x = Path(rec.get("prepared_xyz") or "")
    return bool(rec.get("converged")) and x.is_file() and sha256(x) == rec.get("prepared_sha256")


# ── 실행 ────────────────────────────────────────────────────────────────────
def refuse_existing(out_root) -> None:
    p = Path(out_root)
    if p.exists() and any(p.iterdir()):
        raise SystemExit(f"⛔ out_root 가 비어 있지 않다: {p}\n"
                         f"   이 라운드는 폴더를 재사용하지 않는다 — 새 경로를 주거나 옮겨라.")


def write_manifest(out_root, plan, rows) -> None:
    (Path(out_root) / "manifest.json").write_text(json.dumps({
        "schema": "eprime_pilot_round/v1",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "code_id": git_head(),
        "card": "db/properties/cascade_rebuild_estimand_card_v5_Eprime_2026_09_13.json",
        "decision": "D-2026-09-13-cascade-pilot-estimand-v5-eprime",
        "frozen": {"V_common_A3": V_COMMON_A3, "cell_diag": list(CELL_DIAG),
                   "prep_fmax": PREP_FMAX, "prep_steps": PREP_STEPS,
                   "temps": list(TEMPS), "seeds": list(SEEDS),
                   "equilib_ps": EQUILIB_PS, "prod_ps": PROD_PS, "dt_fs": DT_FS,
                   "friction": FRICTION, "save_fs": SAVE_FS,
                   "fit_window_ps": list(FIT_WINDOW_PS),
                   "uma": {"model": UMA_MODEL, "task": UMA_TASK},
                   "perf_subcap_gpu_h": PERF_SUBCAP_GPU_H,
                   "total_cap_gpu_h": TOTAL_CAP_GPU_H},
        "inputs": rows,
        "n_md_runs_planned": plan_run_count(plan),
        "steps": [{"key": s["key"], "stage": s["stage"], "n_runs": s.get("n_runs", 0)}
                  for s in plan],
        "⛔_판정하지_않는다": "이 라운드는 런을 돌리고 사실만 적는다. 집계·자격·판정은 밖이다.",
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def frozen_now() -> dict:
    """지금 코드가 얼어붙였다고 주장하는 물리 규약. write_manifest 와 **같은 값**이다."""
    return {"V_common_A3": V_COMMON_A3, "cell_diag": list(CELL_DIAG),
            "prep_fmax": PREP_FMAX, "prep_steps": PREP_STEPS,
            "temps": list(TEMPS), "seeds": list(SEEDS),
            "equilib_ps": EQUILIB_PS, "prod_ps": PROD_PS, "dt_fs": DT_FS,
            "friction": FRICTION, "save_fs": SAVE_FS,
            "fit_window_ps": list(FIT_WINDOW_PS),
            "uma": {"model": UMA_MODEL, "task": UMA_TASK},
            "perf_subcap_gpu_h": PERF_SUBCAP_GPU_H,
            "total_cap_gpu_h": TOTAL_CAP_GPU_H}


def resume_check(out_root) -> tuple[dict, set, list]:
    """이어받기 전제 확인 → (기존 budget, 이미 시도한 key 집합, 실패 key 목록).

    ⛔ **code_id 가 아니라 `frozen` 을 본다.** git sha 는 게이트 산수만 고쳐도 바뀌는데,
      이어받기가 위험한 경우는 **물리 규약이 바뀐 것**이다 (부피·온도·창·UMA 모델 …).
      sha 로 막으면 안전한 이어받기까지 막히고, 사람은 결국 우회한다.
    ⛔ 이 함수가 못 하는 것: MD 드라이버 쪽 산출물이 온전한지 **검사하지 않는다**.
      rc==0 을 믿는다 — budget.json 이 그 라운드의 사실 기록이다.
    """
    mani = Path(out_root) / "manifest.json"
    if not mani.is_file():
        raise SystemExit(f"⛔ --resume 인데 {mani} 가 없다 — 이어받을 라운드가 아니다")
    m = json.loads(mani.read_text(encoding="utf-8"))
    old, new = m.get("frozen") or {}, frozen_now()
    diff = [k for k in set(old) | set(new) if old.get(k) != new.get(k)]
    if diff:
        raise SystemExit(
            "⛔ --resume 거부: 물리 규약(frozen)이 달라졌다 — "
            + ", ".join(f"{k}: {old.get(k)!r} → {new.get(k)!r}" for k in sorted(diff))
            + "\n   이어받으면 한 라운드 안에 두 규약이 섞인다. 새 out_root 로 새 라운드를 돌려라.")
    b = budget_load(out_root)
    tried = {st["key"] for st in b.get("steps", []) if "rc" in st}
    failed = [st["key"] for st in b.get("steps", []) if st.get("rc") not in (0, None)]
    return b, tried, failed


def run_round(out_root, python, device, dry_run=False, resume=False,
              retry_failed=False) -> int:
    rows, bad = check_inputs()
    if bad:
        print("⛔ 입력 게이트 불통과 — 시작하지 않는다:")
        for b in bad:
            print("   ·", b)
        return 2
    plan = build_plan(out_root, python=python, device=device)
    print(f"계획: 준비 {sum(1 for s in plan if s['stage'] == 'prep')}건 · "
          f"MD 호출 {sum(1 for s in plan if s['stage'].startswith('md'))}건 "
          f"= **{plan_run_count(plan)}런** · 상한 {PERF_SUBCAP_GPU_H:.0f} / {TOTAL_CAP_GPU_H:.0f} GPU-h")
    if dry_run:
        for s in plan:
            print(f"  [{s['stage']:8s}] {s['key']:34s} runs={s.get('n_runs', 0)} "
                  f"cap={s.get('cap_gpu_h')}")
            print("      " + " ".join(s["cmd"]))
        return 0

    tried, failed = set(), []
    if resume:
        # ⛔ 2026-09-17 — 이어받기가 **없었다.** 게이트가 중단(return 3)하면 남은 길은
        #   빈 폴더로 새 라운드뿐이고, 그러면 이미 쓴 60 GPU-h 를 다시 쓴다. 상한
        #   규율이 오히려 낭비를 강제하는 모양이었다. 누적은 **그대로 이어간다** —
        #   이어받기는 예산을 리셋하지 않는다(그게 상한을 우회하는 길이 된다).
        budget, tried, failed = resume_check(out_root)
        if failed and not retry_failed:
            tried |= set(failed)
        print(f"↻ 이어받기: 이미 끝낸 스텝 {len(tried)}개 건너뜀 · 누적 "
              f"{float(budget.get('used_gpu_h') or 0.0):.2f} GPU-h 승계")
        if failed:
            print(f"   ⚠ 실패로 기록된 스텝 {len(failed)}개: {', '.join(failed)}")
            print("   → " + ("이번에 다시 돌린다 (--resume_retry_failed)" if retry_failed
                             else "그냥 건너뛴다. 다시 돌리려면 --resume_retry_failed"))
    else:
        refuse_existing(out_root)
        Path(out_root).mkdir(parents=True, exist_ok=True)
        write_manifest(out_root, plan, rows)
        budget = budget_load(out_root)
    perf_gpu_h = None
    if resume:
        # 속도 시험을 이미 끝냈으면 그 실측을 되살린다 — 없으면 투영도 없다(게이트는
        # 누적 상한 ④ 만으로 간다). **추정치를 지어내지 않는다.**
        pk = f"md/{PERF_RUN['structure']}__T{PERF_RUN['temp']}__s{PERF_RUN['seed']}"
        perf_gpu_h = next((st.get("gpu_h") for st in budget.get("steps", [])
                           if st.get("key") == pk and st.get("rc") == 0), None)
        print(f"   속도시험 실측 {perf_gpu_h if perf_gpu_h is not None else '없음 — 투영 없이 ④만'}")

    for i, step in enumerate(plan):
        # ⛔⛔ 2026-09-17 — **투영이 낡은 채로 굳어 있었다.** projection 은 속도 시험
        #   직후 `perf × (전체런 − 1)` 로 **한 번만** 계산되고 그대로 남았다. 그래서
        #   게이트는 런이 끝나도 늘 "남은 29런" 을 더해 봤고, 누적이 120 − 67.82 =
        #   52.18 을 넘는 순간 **남은 런 수와 무관하게** 멈췄다.
        #   실측(eprime_2026_09_14): 18/30 런을 마치고 누적 60.67 에서 중단.
        #   정직한 투영은 2.34 × 남은 12런 = 28.1 → 88.8 GPU-h 로 상한 안이다.
        #   카드 §6 ③ 문구는 *"남은 배치를 투영해"* 다 — 코드가 자기 규격과 달랐다.
        #   ⚠ 상한(120)도 속도시험 기준(perf)도 안 바꾼다. 바꾸는 것은 **남은 런 수**뿐이다.
        runs_from_here = runs_remaining_from(plan, i)
        projection = (project_remaining(perf_gpu_h, runs_from_here)
                      if perf_gpu_h is not None else None)
        if step["key"] in tried:
            continue
        if step["stage"] == "md" and not prepared_ok(out_root, step["structure"]):
            print(f"— 건너뜀 {step['key']}: {step['structure']} 준비 미확보 (그 쌍만 미판정)")
            budget["steps"].append({"key": step["key"], "skipped": "준비 미확보"})
            continue
        ok, why = gate_before(step, budget, projection if step["stage"] == "md" else None)
        if not ok:
            print(why)
            budget["steps"].append({"key": step["key"], "stopped": why})
            budget_save(out_root, budget)
            return 3
        print(f"▶ {step['key']} …")
        t0 = time.time()
        rc = subprocess.run(step["cmd"]).returncode
        gpu_h = (time.time() - t0) / 3600.0
        budget["used_gpu_h"] = float(budget.get("used_gpu_h") or 0.0) + gpu_h
        budget["steps"].append({"key": step["key"], "rc": rc, "gpu_h": round(gpu_h, 4),
                                "used_after": round(budget["used_gpu_h"], 4)})
        budget_save(out_root, budget)
        print(f"  ← rc={rc} · {gpu_h:.2f} GPU-h · 누적 {budget['used_gpu_h']:.2f} / "
              f"{TOTAL_CAP_GPU_H:.0f}")
        if step["stage"] == "md_perf":
            ok2, why2 = gate_after(step, gpu_h)
            if not ok2:
                print(why2)
                budget["steps"].append({"key": step["key"], "stopped": why2})
                budget_save(out_root, budget)
                return 4
            perf_gpu_h = gpu_h
            # ⚠ 여기 계산은 **표시용**이다. 게이트가 쓰는 값은 루프 머리에서 매 스텝
            #   다시 센다 (위 2026-09-17 주석). 두 곳에서 따로 굳지 않게 이름도 나눈다.
            remaining = runs_remaining_from(plan, i + 1)
            shown = project_remaining(perf_gpu_h, remaining)
            print(f"  투영: 남은 {remaining}런 ≈ {shown:.1f} GPU-h "
                  f"(누적 예상 {budget['used_gpu_h'] + shown:.1f} / {TOTAL_CAP_GPU_H:.0f})")
        if rc != 0:
            print(f"⛔ {step['key']} 가 rc={rc} 로 끝났다 — 이 스텝은 실패로 기록하고 다음으로 간다")
    budget_save(out_root, budget)
    print(f"■ 라운드 끝 · 누적 {budget['used_gpu_h']:.2f} / {TOTAL_CAP_GPU_H:.0f} GPU-h")
    return 0


# ── selftest — 양성 + **음성** ───────────────────────────────────────────────
def _selftest() -> int:
    import tempfile
    n = [0, 0]

    def chk(c, m):
        n[0] += 1
        n[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    plan = build_plan("/tmp/x")
    chk(sum(1 for s in plan if s["stage"] == "prep") == 5, "양성: 준비가 5건이다")
    chk(plan_run_count(plan) == len(STRUCTURES) * len(TEMPS) * len(SEEDS) == 30,
        f"양성: 계획 런 수가 30 이다 (실제 {plan_run_count(plan)})")
    md_steps = [s for s in plan if s["stage"].startswith("md")]
    chk(md_steps[0]["stage"] == "md_perf" and md_steps[0]["cap_gpu_h"] == PERF_SUBCAP_GPU_H,
        "양성: **속도 시험이 MD 의 맨 앞**이고 거기에만 소상한이 붙는다")
    chk(sum(1 for s in md_steps if s.get("cap_gpu_h")) == 1,
        "양성: 소상한이 붙은 스텝은 하나뿐이다")
    perf_tag = f"{PERF_RUN['structure']}__T{PERF_RUN['temp']}__s{PERF_RUN['seed']}"
    rest = [s for s in md_steps[1:]
            if s["structure"] == PERF_RUN["structure"] and s["seed"] == PERF_RUN["seed"]]
    chk(rest and PERF_RUN["temp"] not in rest[0]["temps"],
        "양성: 속도 시험의 (구조·시드·온도)는 뒤 배치에서 빠진다 — 두 번 안 돈다")
    chk(all("--fit_window_ps" in s["cmd"] for s in md_steps), "양성: MSD 창이 명령에 박힌다")
    rows, bad = check_inputs()
    chk(not bad and len(rows) == 5, f"양성: 실제 다섯 구조가 게이트를 통과한다 ({bad})")
    chk(all(abs(r["V_A3"] - V_COMMON_A3) <= V_TOL_A3 for r in rows),
        "양성: 다섯 입력이 공통 부피다 — 맞춰 준 것이 아니라 원래 같다")

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        # ⛔음성 ①: 부피가 다른 구조가 섞이면 거부
        src = (STRUCT_DIR / "H0_host.xyz").read_text(encoding="utf-8").split("\n")
        src[1] = re.sub(r'Lattice="[^"]+"',
                        'Lattice="21.0 0 0 0 20.110191271466373 0 0 0 10.055095635733187"', src[1])
        (d / "H0_host.xyz").write_text("\n".join(src), encoding="utf-8")
        _, bad2 = check_inputs(struct_dir=d, structures=["H0_host"])
        chk(any("부피" in b for b in bad2), "⛔음성: 부피가 다르면 거부한다 (맞춰 주지 않는다)")
        # ⛔음성 ②: 격자 줄이 없으면 거부
        (d / "noLat.xyz").write_text("2\ncomment\nLi 0 0 0\nLi 1 1 1\n", encoding="utf-8")
        _, bad3 = check_inputs(struct_dir=d, structures=["noLat"])
        chk(any("Lattice" in b for b in bad3), "⛔음성: 격자 없는 xyz 를 거부한다")
        # ⛔음성 ③: 파일이 없으면 거부 (조용히 건너뛰지 않는다)
        _, bad4 = check_inputs(struct_dir=d, structures=["nope"])
        chk(any("구조 파일이 없다" in b for b in bad4), "⛔음성: 없는 구조를 조용히 건너뛰지 않는다")
        # ⛔음성 ④: out_root 재사용 거부
        (d / "junk").mkdir()
        try:
            refuse_existing(d)
            chk(False, "⛔음성: 기존 out_root 를 거부해야 한다")
        except SystemExit:
            chk(True, "⛔음성: 비어 있지 않은 out_root 를 거부한다")

    # ⛔음성 ⑤: 누적이 총상한 이상이면 다음 스텝을 시작하지 않는다
    b = {"total_cap_gpu_h": TOTAL_CAP_GPU_H, "used_gpu_h": TOTAL_CAP_GPU_H, "steps": []}
    ok, why = gate_before(md_steps[-1], b)
    chk(not ok and "누적" in why, "⛔음성: 누적 ≥ 총상한이면 중단한다 (④)")
    # ⛔음성 ⑥: 투영이 총상한을 넘으면 **배치 시작 전** 중단
    b2 = {"total_cap_gpu_h": TOTAL_CAP_GPU_H, "used_gpu_h": 10.0, "steps": []}
    ok2, why2 = gate_before(md_steps[-1], b2, projection=200.0)
    chk(not ok2 and "투영" in why2, "⛔음성: 투영 > 총상한이면 배치 전에 멈춘다 (③)")
    # ⛔양성: 여유가 있으면 통과
    ok3, _ = gate_before(md_steps[-1], b2, projection=10.0)
    chk(ok3, "양성: 여유가 있으면 통과한다 (게이트가 늘 막기만 하면 검사가 아니다)")
    # ⛔음성 ⑦: 속도 시험이 소상한을 넘으면 그 자리에서 중단
    ok4, why4 = gate_after(md_steps[0], PERF_SUBCAP_GPU_H + 0.1)
    chk(not ok4 and "소상한" in why4, "⛔음성: 속도 시험 > 소상한이면 중단한다 (②)")
    chk(gate_after(md_steps[1], 999.0)[0],
        "양성: 소상한은 **속도 시험에만** 붙는다 (다른 스텝을 막지 않는다)")
    # ⛔음성 ⑧: 준비 기록이 없으면 MD 입력 자격이 없다
    with tempfile.TemporaryDirectory() as td2:
        chk(not prepared_ok(td2, "H0_host"), "⛔음성: 준비 기록이 없으면 MD 를 시작하지 않는다")
        pj = Path(td2) / "prep"
        pj.mkdir()
        px = pj / "H0_host.prepared.xyz"
        px.write_text("1\nLattice=\"1 0 0 0 1 0 0 0 1\"\nLi 0 0 0\n", encoding="utf-8")
        (pj / "H0_host.prepared.json").write_text(json.dumps(
            {"converged": False, "prepared_xyz": str(px), "prepared_sha256": sha256(px)}),
            encoding="utf-8")
        chk(not prepared_ok(td2, "H0_host"), "⛔음성: 준비가 **미수렴**이면 자격이 없다")
        (pj / "H0_host.prepared.json").write_text(json.dumps(
            {"converged": True, "prepared_xyz": str(px), "prepared_sha256": "0" * 64}),
            encoding="utf-8")
        chk(not prepared_ok(td2, "H0_host"), "⛔음성: 해시가 어긋나면 자격이 없다")
        (pj / "H0_host.prepared.json").write_text(json.dumps(
            {"converged": True, "prepared_xyz": str(px), "prepared_sha256": sha256(px)}),
            encoding="utf-8")
        chk(prepared_ok(td2, "H0_host"), "양성: 수렴 + 해시 일치면 자격이 있다")
    # 투영식
    chk(abs(project_remaining(2.0, 29) - 58.0) < 1e-9, "양성: 투영 = 실측 × 남은 런")
    chk(project_remaining(0.0, 29) == 0.0 and project_remaining(2.0, 0) == 0.0,
        "⛔음성: 실측이 0 이거나 남은 런이 0 이면 투영은 0 이다 (0 을 상한으로 착각하지 않게)")

    # ⛔⛔ 2026-09-17 실측 사고 — **투영이 안 줄어들었다.** 게이트가 보는 값은
    #   `plan[i:]` 의 n_runs 합이어야 한다. 옛 코드는 속도시험 직후 값(전체−1)에 굳었다.
    _plan = build_plan("/tmp/_st", python="python3", device="cpu")
    _md = [j for j, st in enumerate(_plan) if st["stage"].startswith("md")]
    _rf = lambda j: runs_remaining_from(_plan, j)   # ← 대상 함수를 직접 부른다
    chk(_rf(0) == 30, f"양성: 처음엔 남은 런 30 (계획 전체) — 실제 {_rf(0)}")
    chk(_rf(_md[0]) == 30, f"양성: 속도시험 스텝에서도 30 (자기 자신 포함) — 실제 {_rf(_md[0])}")
    chk(_rf(_md[1]) == 29, f"양성: 속도시험 직후 29 — 실제 {_rf(_md[1])}")
    _last = _md[-1]
    chk(_rf(_last) == int(_plan[_last].get("n_runs") or 0),
        f"양성: 마지막 md 스텝의 남은 런 = 그 스텝 자신뿐 ({_rf(_last)})")
    chk(_rf(_md[1]) > _rf(_md[-1]),
        "⛔음성: 투영 대상 런 수가 **단조 감소**한다 (굳어 있으면 여기서 잡힌다)")
    # 실측 재현: 18/30 을 마친 시점(=7번째 md 호출 앞)에서 남은 런은 12여야 한다.
    _done, _idx = 0, None
    for j in _md:
        if _done >= 18:
            _idx = j; break
        _done += int(_plan[j].get("n_runs") or 0)
    chk(_idx is not None and _rf(_idx) == 12,
        f"⛔음성: 18런을 마친 시점의 남은 런 = 12 (옛 코드는 29로 굳었다) — 실제 {_rf(_idx) if _idx else None}")
    _b18 = {"used_gpu_h": 60.67, "total_cap_gpu_h": TOTAL_CAP_GPU_H}
    _ok_new, _ = gate_before({"stage": "md"}, _b18, project_remaining(2.34, 12))
    _ok_old, _ = gate_before({"stage": "md"}, _b18, project_remaining(2.34, 29))
    chk(_ok_new and not _ok_old,
        "⛔음성: 같은 누적 60.67 에서 **정직한 투영은 통과 · 굳은 투영은 중단** "
        "(2026-09-14 라운드가 여기서 멈췄다)")

    # ── --resume: frozen 이 다르면 거부한다 ────────────────────────────────
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _td:
        _m = Path(_td) / "manifest.json"
        _m.write_text(json.dumps({"frozen": frozen_now()}, ensure_ascii=False), encoding="utf-8")
        (Path(_td) / "budget.json").write_text(json.dumps(
            {"used_gpu_h": 60.67, "total_cap_gpu_h": TOTAL_CAP_GPU_H,
             "steps": [{"key": "prep/H0_host", "rc": 0, "gpu_h": 0.13},
                       {"key": "md/bad", "rc": 1, "gpu_h": 0.01}]}), encoding="utf-8")
        _bb, _tried, _failed = resume_check(_td)
        chk(_tried == {"prep/H0_host", "md/bad"} and _failed == ["md/bad"],
            "양성: 이미 시도한 key 를 집어내고 실패 key 를 따로 보고한다")
        chk(abs(float(_bb["used_gpu_h"]) - 60.67) < 1e-9,
            "양성: 이어받기는 누적 예산을 **승계한다** (리셋하면 상한 우회다)")
        _bad = dict(frozen_now()); _bad["prod_ps"] = 50.0
        _m.write_text(json.dumps({"frozen": _bad}, ensure_ascii=False), encoding="utf-8")
        try:
            resume_check(_td); _refused = False
        except SystemExit as e:
            _refused = "prod_ps" in str(e)
        chk(_refused, "⛔음성: 물리 규약(prod_ps)이 달라지면 이어받기를 **거부**한다")
    try:
        resume_check(_td + "/nonexistent"); _nm = False
    except SystemExit:
        _nm = True
    chk(_nm, "⛔음성: manifest 가 없으면 이어받지 않는다")

    print(f"selftest {n[1]}/{n[0]} · {'PASS' if n[1] == n[0] else 'FAIL'}")
    return 0 if n[1] == n[0] else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="E′ 파일럿 한 라운드 (동결 사양)")
    ap.add_argument("--out_root", default=str(Path.home() / "work/runs/eprime_pilot"))
    ap.add_argument("--python", default=sys.executable or "python3")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--dry_run", action="store_true")
    ap.add_argument("--resume", action="store_true",
                    help="기존 out_root 를 이어받는다 (frozen 일치 필수 · 누적 예산 승계)")
    ap.add_argument("--resume_retry_failed", action="store_true",
                    help="--resume 시 rc≠0 으로 끝난 스텝도 다시 돌린다")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--_prep_one", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--_struct", help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a._prep_one:
        prep_one(a._struct, a.out_root, device=a.device)
        return 0
    os.chdir(REPO)
    return run_round(a.out_root, a.python, a.device, dry_run=a.dry_run,
                     resume=a.resume, retry_failed=a.resume_retry_failed)


if __name__ == "__main__":
    raise SystemExit(main())
