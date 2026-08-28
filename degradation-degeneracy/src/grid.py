"""grid.py — 조합 격자 생성 + 병렬 실행. 이 프로젝트의 핵심 (Phase 3).

- parse_axis      : "0:0.2:0.02" | "0,0.05,0.1" | "0.1" | "none" 파싱
- build_conditions: itertools.product 조합 (+ noise 축)
- run_grid        : joblib(loky) 병렬, chunk 단위 parquet 저장, resume,
                    실패 격리(failed.csv), tqdm 진행률, --dry-run

조합 프로토콜: charge_first(완방 프레임)로 통일 — manifest에 기록.
근거: 완충 프레임에서는 LAM_ne_de의 농도 보정 c/(1−i)이 i>0.036에서 c_max를
넘어 대부분의 축이 불능이 되지만, 완방 프레임에서는 NE 농도가 작아 안전하다.
(03_ARCHITECTURE.md 4절 주의 블록)
"""

from __future__ import annotations

import hashlib
import itertools
import json
import logging
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.baseline import DischargedState, get_discharged_state
from src.config import config_hash, load_config, validate_config
from src.curves import add_noise, extract_curves
from src.io import (acquire_run_lock, append_failed, base_manifest, chunk_files,
                    git_info, load_completed, load_failed, mark_completed,
                    merge_chunks, release_run_lock, save_chunk, write_manifest)
from src.modes import (Baseline, InfeasibleConditionError, build_overrides,
                       canonical_guards)
from src.runner import make_solver, run_one, solver_name

log = logging.getLogger(__name__)

GRID_PROTOCOL_KEY = "grid_protocol_override"   # base.yaml: charge_first


# ---------------------------------------------------------------- 축 파싱

def parse_axis(spec: str | float | int | list | None) -> np.ndarray:
    """축 문법 파싱 (03_ARCHITECTURE.md 2.4절).

    "0:0.2:0.02" → arange(0, 0.2+ε, 0.02)   (stop 포함)
    "0,0.05,0.1" → 명시 목록
    "0.1"        → 단일값
    "none"/None  → [0.0] (축 비활성)
    """
    if spec is None:
        return np.array([0.0])
    if isinstance(spec, (int, float)):
        return np.array([float(spec)])
    if isinstance(spec, (list, tuple)):
        return np.array([float(x) for x in spec])

    s = str(spec).strip().lower()
    if s in ("none", ""):
        return np.array([0.0])
    if ":" in s:
        parts = [float(x) for x in s.split(":")]
        if len(parts) != 3:
            raise ValueError(f"축 문법 오류 (start:stop:step 필요): {spec}")
        start, stop, step = parts
        if step <= 0:
            raise ValueError(f"step > 0 필요: {spec}")
        vals = np.arange(start, stop + step * 0.5, step)
        return np.round(vals, 10)
    if "," in s:
        return np.array([float(x) for x in s.split(",")])
    return np.array([float(s)])


def axis_from_config(node) -> np.ndarray:
    """config grid 절의 {start, stop, step} | 리스트 | 스칼라 → 배열."""
    if isinstance(node, dict):
        vals = np.arange(float(node["start"]),
                         float(node["stop"]) + float(node["step"]) * 0.5,
                         float(node["step"]))
        return np.round(vals, 10)
    return parse_axis(node)


# ---------------------------------------------------------------- 조건 생성

@dataclass(frozen=True)
class Condition:
    lli: float
    lam_pe: float
    lam_ne: float
    lam_pe_type: str
    lam_ne_type: str
    noise: float
    seed: int

    @property
    def cond_id(self) -> str:
        blob = json.dumps(asdict(self), sort_keys=True)
        return hashlib.sha1(blob.encode()).hexdigest()[:12]


def build_conditions(lli_ax, lam_pe_ax, lam_ne_ax,
                     lam_pe_types: list[str], lam_ne_types: list[str],
                     noise_ax, noise_seed: int) -> list[Condition]:
    """축들의 곱집합. noise seed는 조건별로 안정적으로 유도된다."""
    conds = []
    for lli, lpe, lne, tpe, tne, nz in itertools.product(
            lli_ax, lam_pe_ax, lam_ne_ax, lam_pe_types, lam_ne_types, noise_ax):
        key = f"{lli:.6f}|{lpe:.6f}|{lne:.6f}|{tpe}|{tne}|{nz:.6f}"
        seed = noise_seed + int(hashlib.sha1(key.encode()).hexdigest()[:6], 16)
        conds.append(Condition(float(lli), float(lpe), float(lne),
                               str(tpe), str(tne), float(nz), seed))
    return conds


def _types(spec: str) -> list[str]:
    return ["de", "li"] if str(spec).lower() == "both" else [str(spec)]


def conditions_from_config(cfg: dict, cli: dict | None = None) -> list[Condition]:
    """config grid 절 (+ CLI 축 override) → 조건 목록."""
    cli = cli or {}
    gc = cfg.get("grid", {})

    def ax(cli_key: str, cfg_key: str):
        if cli.get(cli_key) not in (None, "", "unset"):
            return parse_axis(cli[cli_key])
        if cfg_key in gc:
            return axis_from_config(gc[cfg_key])
        return np.array([0.0])

    lli_ax = ax("lli", "lli")
    lam_pe_ax = ax("lam_pe", "lam_pe")
    lam_ne_ax = ax("lam_ne", "lam_ne")

    tpe = cli.get("lam_pe_type") or (gc.get("lam_pe", {}) or {}).get("type", "de")
    tne = cli.get("lam_ne_type") or (gc.get("lam_ne", {}) or {}).get("type", "de")

    noise_spec = cli.get("noise")
    noise_ax = (parse_axis(noise_spec) if noise_spec not in (None, "")
                else np.array([float(x) for x in gc.get("noise", [0.0])]))
    noise_seed = int(cli.get("noise_seed") or gc.get("noise_seed", 42))

    return build_conditions(lli_ax, lam_pe_ax, lam_ne_ax,
                            _types(tpe), _types(tne), noise_ax, noise_seed)


# ---------------------------------------------------------------- 워커

def _solve_condition(cfg: dict, cond: Condition, d_dict: dict,
                     protocol_name: str) -> dict:
    """단일 조건 처리 (워커 프로세스에서 실행).

    각 워커는 자체 param을 생성하고(runner.build_param), 모델은 워커별
    1회 빌드 후 재사용된다(model.lru_cache). 반환은 picklable dict만.
    """
    # ★ 13차 발견 3 — 이 워커가 **실제로** 쓴 solver identity. parent 의 probe 만
    #   서명하면 워커별 fallback 을 검출할 수 없다. 모든 return 경로에 싣는다
    #   (성공·실패 무관 — main 이 전 조건을 대조한다).
    from src.runner import effective_solver as _eff_w
    _solver_id = _eff_w(cfg)

    b = Baseline.from_config(cfg)
    d = DischargedState(**d_dict)
    guards = cfg.get("guards", {})
    n_trim = int(cfg["postprocess"]["n_trim"])
    n_interp = int(cfg["postprocess"]["n_interp"])

    try:
        ov = build_overrides(cond.lli, cond.lam_pe, cond.lam_ne,
                             cond.lam_pe_type, cond.lam_ne_type, b, d, guards)
    except InfeasibleConditionError as e:
        return {"cond": asdict(cond), "cond_id": cond.cond_id,
                "error": f"infeasible: {e}", "elapsed_s": 0.0,
                "solver_identity": _solver_id}

    res = run_one(cfg, ov, protocol_name)
    if not res.ok:
        return {"cond": asdict(cond), "cond_id": cond.cond_id,
                "error": res.error, "elapsed_s": res.elapsed_s,
                "solver_identity": _solver_id}

    try:
        curves = extract_curves(res.solution, n_trim, n_interp)
    except Exception as e:  # noqa: BLE001
        return {"cond": asdict(cond), "cond_id": cond.cond_id,
                "error": f"extract: {type(e).__name__}: {e}",
                "elapsed_s": res.elapsed_s, "solver_identity": _solver_id}

    v_noisy = add_noise(curves["v_full"], cond.noise, cond.seed)
    return {
        "cond": asdict(cond), "cond_id": cond.cond_id, "error": None,
        "elapsed_s": res.elapsed_s, "solver_identity": _solver_id,
        "q_mah": curves["q_mah"],
        "x_norm": curves["x_norm"].tolist(),
        "v_pe": curves["v_pe"].tolist(),
        "v_ne": curves["v_ne"].tolist(),
        "v_full": curves["v_full"].tolist(),
        "v_full_noisy": v_noisy.tolist(),
    }


def grid_run_spec(cfg: dict, conditions: list[Condition],
                  discharged: dict | None = None,
                  discharged_sha: str | None = None) -> tuple[dict, str]:
    """★ F74 — 곡선 **계산**을 고정하는 서명 (8차 리뷰 발견 1).

    F70 의 `curves_manifest.yaml` 은 이미 존재하는 parquet 의 digest 와 호출자가
    준 metadata 를 적는 **자기기술**이었다. 그래서
      · 수제 선형 곡선을 이 함수로 포장해도 fitting·validator 가 통과했고,
      · config A 로 절반, config B 로 resume 한 혼합 곡선이 B 만 주장하는
        manifest 아래 통과했다 (리뷰 실측: ROW_MEANS 4.75/3.75 혼재, ok=True).

    fitting 의 F49/F67 과 같은 해법을 쓴다 — 서명에 코드·설정·조건 집합을 넣고,
    **모든 청크 행이 그 서명을 지닌 채** 저장되게 한다. 다른 서명의 resume 은
    병합 전에 죽는다.
    """
    from src.io import env_fingerprint, source_digest

    from src.runner import effective_solver

    cond_ids = sorted(c.cond_id for c in conditions)
    spec = {
        "grid_sig_version": 5,   # 12차: effective_solver 필수화 · 14차: noise 집합
        "config_hash": config_hash(cfg),
        # ★ 14차 발견 1 — 의도한 noise 집합을 서명한다. validator 가 family
        #   (lli, lam_pe, lam_ne, 유형)마다 이 집합이 정확히 한 번씩 있는지
        #   대조한다 — 없으면 noise 축이 조용히 줄어도 잡을 기준이 없다.
        "noise": sorted({float(c.noise) for c in conditions}),
        # extends 부모까지 — 최종 병합본 해시만으로도 내용은 고정되지만,
        # 어떤 파일들이 읽혔는지가 없으면 봉인·재검이 불가능하다 (발견 3)
        "config_files": [str(p) for p in cfg.get("_loaded_files", [])],
        "protocol_unified": cfg.get(GRID_PROTOCOL_KEY, "charge_first"),
        "parameter_set": cfg.get("parameter_set"),
        "noise_seed": int((cfg.get("grid") or {}).get("noise_seed", 42)),
        "condition_ids_sha256": hashlib.sha256(
            "\n".join(cond_ids).encode()).hexdigest()[:16],
        "n_conditions_intended": len(cond_ids),
        "postprocess": cfg.get("postprocess"),
        # ★ F82/9차 발견 1 — **완방상태가 곧 격자의 물리 기준점**이다. 모든 조건의
        #   초기 농도가 여기서 나오므로, 이게 다르면 같은 (lli, lam_pe, lam_ne)
        #   라도 다른 truth 다. 서명에 없으면 중단 후 캐시가 바뀐 채 resume 했을 때
        #   **서로 다른 truth 의 행이 같은 서명 아래 섞인다** (리뷰 실측:
        #   ROW_MEANS 6.0/3.0 혼재, ROW_SIGS 단일, VALIDATOR_OK=True).
        "discharged_state": discharged,
        "discharged_state_sha": discharged_sha,
        # ★ 11차 발견 3 — 실패 사유("infeasible:")를 **재평가**하는 데 필요한
        #   물리·guard recipe 를 서명 안에 봉인한다. 예전에는 검증자가 호출자가
        #   준 cfg 로 replay 해서, (a) cfg 를 안 주는 경로(archive·격리 복원)는
        #   재검 자체를 건너뛰었고, (b) 준 cfg 가 producer 의 것과 같다는 보장도
        #   없었다. 서명된 recipe 만 쓰면 어느 경로에서 검증하든 같은 기준이다.
        "replay_recipe": {
            "baseline": {k: float(v) for k, v in (cfg.get("baseline") or {}).items()},
            # ★ 14차 발견 5 — canonical 3-key 로 채워 서명한다. 부분 guards 를
            #   그대로 서명하면 코드 기본값이 바뀐 미래의 재검이 어긋난다.
            "guards": canonical_guards(cfg.get("guards")),
        },
        # ★ 12차 발견 2 — 요청(cfg.solver)이 아니라 **실제로 쓰인** solver 를
        #   서명에 넣는다. IDAKLU 생성 실패 시 Casadi 로 조용히 fallback 하므로,
        #   요청만 봉인하면 중단 후 resume 에서 backend 가 달라져도 같은 서명이
        #   된다 — 서로 다른 solver 의 곡선이 한 artifact 에 섞인다.
        "effective_solver": effective_solver(cfg),
        "source_digest": source_digest(),
        "env": env_fingerprint(),
    }
    sig = hashlib.sha1(
        json.dumps(spec, sort_keys=True, default=str).encode()).hexdigest()[:12]
    return spec, sig


def _assert_worker_solvers(results: list[dict], want: dict) -> None:
    """★ 13차 발견 3 — **워커가 실제로 쓴** solver 가 서명과 같은지 확인한다.

    실제 solve 는 loky worker 안에서 각자 `make_solver()` 를 호출한다. parent 가
    probe 한 identity 만 서명에 들어가므로, 어느 워커에서 IDAKLU constructor 가
    실패해 Casadi 로 fallback 하면 **다른 solver 의 곡선이 같은 서명 아래** 저장
    된다. 청크를 쓰기 전에 전 조건을 대조하고, 하나라도 다르면 즉시 멈춘다.
    identity 를 안 실은 결과(옛 워커)도 증명 불가이므로 실패다 (fail-closed).
    """
    want_key = {k: want.get(k) for k in ("effective_class", "pybamm",
                                         "pybammsolvers", "casadi")}
    bad, missing = [], []
    for r in results:
        got = r.get("solver_identity")
        if not got:
            missing.append(str(r.get("cond_id")))
            continue
        if {k: got.get(k) for k in want_key} != want_key:
            bad.append(f"{r.get('cond_id')}({got.get('effective_class')})")
    if missing or bad:
        raise RuntimeError(
            f"워커가 실제로 쓴 solver 가 서명과 다르거나 기록되지 않았습니다 "
            f"(13차 발견 3): 불일치 {bad[:3]} / 미기록 {missing[:3]}\n"
            f"  서명: {want_key}\n"
            f"  같은 서명 아래 서로 다른 solver 의 곡선이 섞이면 합성 truth 가 "
            f"무너집니다. 환경을 확인하고 처음부터 다시 생성하세요.")


def _result_to_frame(r: dict, protocol_name: str,
                     grid_sig: str | None = None) -> pd.DataFrame:
    n = len(r["x_norm"])
    c = r["cond"]
    if grid_sig is not None:
        return _result_to_frame(r, protocol_name).assign(grid_run_sig=grid_sig)
    return pd.DataFrame({
        "cond_id": [r["cond_id"]] * n,
        "lli": [c["lli"]] * n,
        "lam_pe": [c["lam_pe"]] * n,
        "lam_ne": [c["lam_ne"]] * n,
        "lam_pe_type": [c["lam_pe_type"]] * n,
        "lam_ne_type": [c["lam_ne_type"]] * n,
        "noise": [c["noise"]] * n,
        "seed": [c["seed"]] * n,
        "protocol": [protocol_name] * n,
        "q_mah": [r["q_mah"]] * n,
        "x_norm": r["x_norm"],
        "v_pe": r["v_pe"],
        "v_ne": r["v_ne"],
        "v_full": r["v_full"],
        "v_full_noisy": r["v_full_noisy"],
    })


# ---------------------------------------------------------------- 본체

CURVES_MANIFEST = "curves_manifest.yaml"


def write_curves_manifest(out_dir, cfg: dict, conditions=None, extra=None) -> Path:
    """★ F70 — 곡선을 만든 쪽의 provenance를 **별도 파일**로 남긴다.

    이 연구의 전제는 "정답을 아는 PyBaMM 합성 곡선"이다. 그런데 지금까지 fit
    artifact 가 증명하는 것은 *"어떤 parquet 을 fit 했다"* 뿐이었다 — 손으로 만든
    비-PyBaMM `curves.parquet` 도 실제 fit 후 validator 를 통과했다. 즉 **실험
    전제 자체가 봉인되지 않았다.**

    왜 `manifest.yaml` 이 아니라 별도 파일인가:
    `write_manifest()` 는 `existing.update(payload)` 로 **얕게 병합**한다. grid 와
    fit 을 같은 디렉터리에 쓰면 fit manifest 가 grid 의 핵심 필드를 덮어써서,
    나중에 보면 곡선을 누가 어떤 solver·seed 로 만들었는지 알 수 없다.
    이 파일은 fitting 이 건드리지 않고 **입력으로 봉인**한다.
    """
    import yaml

    from src.io import env_fingerprint, file_digest, source_digest

    out_dir = Path(out_dir)
    curves = out_dir / "curves.parquet"
    gc = cfg.get("grid", {}) if isinstance(cfg, dict) else {}
    payload = {
        "run_type": "grid_producer",
        "producer_version": 1,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "config_hash": config_hash(cfg),
        "parameter_set": cfg.get("parameter_set"),
        "protocol_unified": cfg.get(GRID_PROTOCOL_KEY, "charge_first"),
        "grid_config": gc,
        "noise_seed": int(gc.get("noise_seed", 42)),
        "source_digest": source_digest(),
        "env": env_fingerprint(),
        **git_info(Path(__file__).resolve().parent.parent),
        "curves_sha256": file_digest(curves, full=True),
        "n_conditions": len(conditions) if conditions is not None else None,
        "_주의": ("이 파일은 곡선을 만든 실행의 기록이다. fitting 은 이것을 "
                 "**입력으로 봉인**하며 덮어쓰지 않는다 (F70)."),
    }
    if extra:
        payload.update(extra)
    p = out_dir / CURVES_MANIFEST
    p.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")
    return p


def _assert_grid_authorized(cfg: dict, out_dir, conditions=None,
                            dry_run: bool = False, leg: str | None = None,
                            attempt: str | None = None):
    """계획 gate — smoke namespace 밖이면 승인된 claim 이 있어야 한다.

    ★ 48차 P0-5 — 승인 spec 이 **실행을 고정한다.** 47차 spec 은
      `{leg_id, mode, dry_run, config_digest}` 넷뿐이라 `--lli`·`--lam-pe`·
      `--noise`(=조건 집합)와 `--out`(=결과가 놓일 자리)을 승인 뒤에 통째로
      갈아도 같은 digest 가 나왔다. 그러면 승인한 것은 실행이 아니라 다리
      **이름**이다.

      이제 조건 집합의 내용 주소와 산출 위치가 spec 에 들어가고, fit 쪽 절반은
      계획이 선언한 값을 그대로 쓴다 — 그래야 두 phase 가 **하나의 claim** 아래
      묶인다 (`leg_run_spec()`).
    """
    import hashlib as _h

    from src.io import source_digest
    from tools.preserve import (assert_run_is_authorized, declared_leg_run_spec,
                                leg_run_spec, is_inside_namespace,
                                SMOKE_NAMESPACE)

    leg = leg_name(leg)
    # smoke namespace 안이면 계획을 요구하지 않는다 (계약 §13.3.3). 그 판정은
    # `assert_run_is_authorized()` 와 **같은 함수**로 한다 — 두 규칙이 갈리면
    # 어느 쪽이 경계인지 정할 수 없다.
    if is_inside_namespace(out_dir, SMOKE_NAMESPACE):
        return None
    cond_ids = sorted(c.cond_id for c in (conditions or []))
    live_grid = {
        "config_digest": _cfg_digest(cfg),
        "condition_ids_sha256": _h.sha256(
            "\n".join(cond_ids).encode("utf-8")).hexdigest()[:16],
        "n_conditions": len(cond_ids),
        "out": leg_out_key(out_dir)}
    declared = declared_leg_run_spec(leg)
    spec = leg_run_spec(leg, live_grid, declared.get("fit") or {})
    return assert_run_is_authorized(leg, "grid", [out_dir], spec,
                                    source_digest(), attempt=attempt)

def leg_name(explicit: str | None = None) -> str:
    """이 실행이 어느 다리인가 (48차 P0-5).

    47차는 `os.environ["LEG"]` 만 봤고, `run.sh` 는 `LEG` 를 **export 하지
    않은 채** `--leg` 를 argv 로 넘겼는데 두 모듈 다 그 인자를 선언하지 않았다.
    실측: `python -m src.grid --leg L --out ... --dry-run` →
    `error: unrecognized arguments: --leg L`, rc 2. 즉 `--leg` 는 켜는 순간
    실행이 죽는 축이었고 gate 는 한 번도 진짜 다리 이름을 본 적이 없다
    (`grid_fit_v4` 로 떨어졌다).

    이제 CLI 가 먼저, 그 다음 환경변수다. 둘 다 없으면 정본 실행 이름을 쓴다.
    """
    import os as _os

    return (explicit or _os.environ.get("LEG")
            or _os.environ.get("CANONICAL_RUN") or "grid_fit_v4")


def leg_out_key(out_dir) -> str:
    """산출 위치를 **저장소 기준 경로**로 — spec 이 기계마다 달라지지 않게."""
    from pathlib import Path as _P

    root = _P(__file__).resolve().parents[1]
    q = _P(out_dir).resolve()
    try:
        return q.relative_to(root).as_posix()
    except ValueError:
        return q.as_posix()



def _cfg_digest(cfg: dict) -> str:
    import hashlib as _h
    import json as _j

    return _h.sha256(_j.dumps(cfg, sort_keys=True, ensure_ascii=False,
                              default=str).encode("utf-8")).hexdigest()[:16]


def run_grid(cfg: dict, conditions: list[Condition], nproc: int,
             chunk_size: int, out_dir: str | Path,
             resume: bool = False, dry_run: bool = False,
             leg: str | None = None) -> dict:
    """조합 격자 실행. 반환: 요약 dict."""
    from joblib import Parallel, delayed
    from tqdm import tqdm

    out_dir = Path(out_dir)
    # ★ 47차 P0-2 (조건 11-c) — **첫 부작용 전에** 계획 gate 를 지난다.
    #   46차 gate 는 `run.sh` 안에만 있어서 `python -m src.grid` 직접 호출이
    #   계획을 전혀 보지 않았다. mkdir 도 부작용이므로 그보다 먼저 본다.
    _claim = _assert_grid_authorized(cfg, out_dir, conditions=conditions,
                                     dry_run=dry_run, leg=leg)
    out_dir.mkdir(parents=True, exist_ok=True)
    protocol_name = cfg.get(GRID_PROTOCOL_KEY, "charge_first")

    # ── resume: 완료 조건 건너뛰기 ──
    done: set[str] = load_completed(out_dir) if resume else set()
    todo = [c for c in conditions if c.cond_id not in done]
    if resume and done:
        log.info("resume: %d개 완료 확인, %d개 남음", len(done), len(todo))
    elif not resume and not dry_run:
        prev = load_completed(out_dir)
        if prev:
            log.warning(
                "출력 디렉터리에 이미 완료 기록 %d건이 있는데 --resume 없이 실행합니다. "
                "전부 재계산되고 청크가 중복 누적됩니다. "
                "이어서 하려면 --resume, 새로 하려면 다른 --out 을 쓰세요.", len(prev))

    # ── 완방상태는 병렬 전에 1회 산출 (워커에 값만 전달) ──
    d = get_discharged_state(cfg)
    d_dict = asdict(d)
    b = Baseline.from_config(cfg)
    guards = cfg.get("guards", {})

    # ── 사전 검증: guards 위반 조건은 solve 없이 즉시 failed 처리 ──
    feasible, infeasible = [], []
    for c in todo:
        try:
            build_overrides(c.lli, c.lam_pe, c.lam_ne, c.lam_pe_type,
                            c.lam_ne_type, b, d, guards)
            feasible.append(c)
        except InfeasibleConditionError as e:
            infeasible.append((c, str(e)))

    # ── dry-run: 조건 수 · 예상시간 · 예상용량 출력 후 종료 ──
    if dry_run:
        n = len(feasible)
        sample = feasible[: min(3, n)]
        if sample:
            t0 = time.perf_counter()
            for c in sample:
                _solve_condition(cfg, c, d_dict, protocol_name)
            per = (time.perf_counter() - t0) / len(sample)
        else:
            per = 0.0
        est_min = per * n / max(nproc, 1) / 60
        n_interp = int(cfg["postprocess"]["n_interp"])
        est_mb = n * n_interp * 15 * 8 / 1e6  # 15열 × float64
        print(f"[dry-run] 조건 수: {len(conditions)} "
              f"(완료 스킵 {len(done)}, guards 불능 {len(infeasible)}, 실행 대상 {n})")
        print(f"[dry-run] 실측 {per:.1f} s/cond × {n} / {nproc} proc ≈ {est_min:.1f} min")
        print(f"[dry-run] 예상 출력 크기 ≈ {est_mb:.0f} MB (parquet 압축 전)")
        for c, reason in infeasible[:5]:
            print(f"[dry-run] 불능 예시: lli={c.lli} lam_pe={c.lam_pe} "
                  f"lam_ne={c.lam_ne} → {reason}")
        return {"dry_run": True, "n_total": len(conditions), "n_todo": n,
                "n_infeasible": len(infeasible), "est_min": est_min}

    # ── 동시 실행 방지 (청크 덮어쓰기·집계 오염 차단) ──
    acquire_run_lock(out_dir)

    # ── ★ F74/F82: 실행 서명 + 시작 기록 + resume 가드 ──
    from src.baseline import _cache_path as _dsp
    from src.io import file_digest as _fd
    g_spec, g_sig = grid_run_spec(cfg, conditions, discharged=d_dict,
                                  discharged_sha=_fd(_dsp(cfg, None), full=True))
    start_rec = {"grid_run_sig": g_sig, "grid_run_spec": g_spec,
                 "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                 "resume": bool(resume),
                 **git_info(Path(__file__).resolve().parent.parent)}
    import yaml as _yaml
    (out_dir / "curves_manifest_start.yaml").write_text(
        _yaml.safe_dump(start_rec, allow_unicode=True, sort_keys=False),
        encoding="utf-8") if not (out_dir / "curves_manifest_start.yaml").exists()         else None
    # 기존 청크가 있으면 서명이 같아야 한다 — 다른 config/코드의 resume 혼합이
    # 8차 리뷰에서 실제로 재현됐다 (A 절반 + B resume → B 만 주장, ok=True)
    for old in chunk_files(out_dir):
        try:
            sigs = set(pd.read_parquet(old, columns=["grid_run_sig"])["grid_run_sig"])
        except Exception:  # noqa: BLE001 — 열 자체가 없는 옛 형식
            sigs = {"<서명 없음(F74 이전)>"}
        if sigs != {g_sig}:
            raise RuntimeError(
                f"기존 청크의 grid_run_sig {sorted(sigs)}가 이번 실행 {g_sig}와 "
                f"다릅니다. 다른 config/코드의 결과가 섞입니다 (F74). "
                f"{out_dir}/chunks 를 비우고 처음부터 다시 돌리세요.")

    # ── manifest 초기화 ──
    write_manifest(out_dir, base_manifest(config_hash(cfg), extra={
        "run_type": "grid",
        "protocol_unified": protocol_name,
        "solver": solver_name(make_solver(cfg)),
        "nproc": nproc,
        "chunk_size": chunk_size,
        "n_conditions": len(conditions),
        "n_resume_skipped": len(done),
        "discharged_state": d_dict,
    }))

    # failed.csv 중복 방지 — 이미 기록된 조건은 다시 쓰지 않는다
    recorded_failed = load_failed(out_dir)

    def _record_failure(cond_id: str, cond: dict, reason: str) -> None:
        if cond_id not in recorded_failed:
            append_failed(out_dir, cond_id, cond, reason)
            recorded_failed.add(cond_id)

    for c, reason in infeasible:
        _record_failure(c.cond_id, asdict(c), f"infeasible: {reason}")
        mark_completed(out_dir, c.cond_id)   # 재실행에서도 건너뛰도록

    # ── chunk 단위 병렬 실행 ──
    n_failed = len(infeasible)
    n_ok = 0
    t_start = time.perf_counter()
    chunk_idx = _next_chunk_idx(out_dir)

    # ★ 워커 풀을 청크 간에 재사용한다.
    #   청크마다 Parallel을 새로 만들면 워커가 매번 pybamm import + composite DFN
    #   빌드를 반복해 청크당 수십 초가 낭비된다 (V100 32코어 실측: 95조건에 71.6 s,
    #   이론값 10 s). context manager로 묶으면 그 비용을 실행당 1회로 상각한다.
    try:
        with tqdm(total=len(feasible), desc="grid", unit="cond") as bar, \
                Parallel(n_jobs=nproc, backend="loky") as parallel:
            for start in range(0, len(feasible), chunk_size):
                chunk = feasible[start:start + chunk_size]
                results = parallel(
                    delayed(_solve_condition)(cfg, c, d_dict, protocol_name)
                    for c in chunk
                )
                # ★ 13차 발견 3 — 저장 **전에** 워커 solver 를 서명과 대조한다
                _assert_worker_solvers(results, g_spec["effective_solver"])
                frames = []
                for r in results:
                    if r["error"] is not None:
                        _record_failure(r["cond_id"], r["cond"], r["error"])
                        n_failed += 1
                    else:
                        frames.append(_result_to_frame(r, protocol_name, g_sig))
                        n_ok += 1
                if frames:
                    save_chunk(pd.concat(frames, ignore_index=True), out_dir, chunk_idx)
                    chunk_idx += 1
                # 청크 flush 후에만 완료 마킹 → kill돼도 데이터 없는 완료가 없음
                for r in results:
                    mark_completed(out_dir, r["cond_id"])
                bar.update(len(chunk))
    finally:
        release_run_lock(out_dir)

    merged = merge_chunks(out_dir, "curves.parquet")
    elapsed = time.perf_counter() - t_start

    # 누적 집계 (resume 시 이전 실행분 포함) — 파일 기준이 진실.
    # 양쪽 모두 '고유 cond_id 수'로 세야 한다 (한쪽만 set이면 재실행 시 어긋남).
    n_done_total = len(load_completed(out_dir))
    n_failed_total = len(load_failed(out_dir))
    write_manifest(out_dir, {
        "n_ok": n_ok, "n_failed": n_failed,               # 이번 호출분
        "n_completed_total": n_done_total,                 # 누적 (failed 포함)
        "n_failed_total": n_failed_total,
        "n_curves_total": n_done_total - n_failed_total,
        "elapsed_s": round(elapsed, 1),
        "curves_parquet": str(merged) if merged else None,
        "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    # ★ F70/F74 — 곡선 producer 기록을 별도 파일로. fitting 이 이걸 봉인한다.
    from src.io import source_digest as _sd
    write_curves_manifest(out_dir, cfg, conditions, extra={
        "solver": solver_name(make_solver(cfg)),
        "n_curves": n_done_total - n_failed_total,
        "elapsed_s": round(elapsed, 1),
        "grid_run_spec": g_spec,
        "grid_run_sig": g_sig,
        "source_digest_changed_during_run": bool(
            g_spec["source_digest"] != _sd()),
        # ★ F83/9차 발견 4 — 의도한 조건집합이 **관측 ⊎ 실패**로 정확히 나뉘는지
        #   검증기가 판정할 수 있게 실패 목록의 서명도 남긴다. 예전에는
        #   n_curves 만 맞으면 통과해, 어려운 조건이 통째로 빠져도 검출되지 않았다
        #   (리뷰 실측: INTENDED 3 / OBSERVED 2 / VALIDATOR_OK=True).
        "failed_ids_sha256": hashlib.sha256(
            "\n".join(sorted(load_failed(out_dir))).encode()).hexdigest()[:16],
        "n_failed_total": n_failed_total,
        # ★ 10차 자체 확인 3 — CLI 축 override 시 grid_config(=config 파일 축)는
        #   실제 축과 다를 수 있다. 실제 조건에서 유도한 축을 함께 기록한다.
        #   (조건 집합 자체는 grid_run_spec.condition_ids_sha256 이 서명한다)
        "effective_axes": {
            "lli": sorted({float(c.lli) for c in conditions}),
            "lam_pe": sorted({float(c.lam_pe) for c in conditions}),
            "lam_ne": sorted({float(c.lam_ne) for c in conditions}),
            "noise": sorted({float(c.noise) for c in conditions}),
        },
        "_grid_config_주의": ("grid_config 는 config 파일 원본이다 — CLI 축 "
                             "override 는 effective_axes 와 "
                             "condition_ids_sha256 에만 반영된다 (10차)."),
    })
    log.info("grid 완료: ok=%d failed=%d (누적 곡선 %d) elapsed=%.1fs",
             n_ok, n_failed, n_done_total - n_failed_total, elapsed)
    summary = {"n_ok": n_ok, "n_failed": n_failed,
               "n_curves_total": n_done_total - n_failed_total,
               "elapsed_s": elapsed, "out_dir": str(out_dir)}
    # ★ 48차 P0-4 — 끝난 phase 를 **durable 하게 닫는다.** 47차는
    #   `phase_done()`·`finalize_leg()` 을 만들어 놓고 production 에서 한 번도
    #   부르지 않았다 — lifecycle 이 있는데 아무 것도 그 상태를 움직이지 않으면
    #   그것은 lifecycle 이 아니라 죽은 코드다.
    if _claim is not None:
        _claim.phase_done("grid", {
            "out": str(out_dir),
            "n_curves_total": summary["n_curves_total"],
            "grid_run_sig": g_sig,
            "finished_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    return summary


def _next_chunk_idx(out_dir: Path) -> int:
    """기존 청크 다음 번호. 파일명은 chunk_<idx>_<pid>.parquet (구형은 chunk_<idx>)."""
    idxs = []
    for f in chunk_files(out_dir):
        try:
            idxs.append(int(f.stem.split("_")[1]))
        except (IndexError, ValueError):
            continue
    return max(idxs) + 1 if idxs else 0


# ---------------------------------------------------------------- CLI

def main() -> None:
    import argparse
    import multiprocessing

    ap = argparse.ArgumentParser(description="조합 격자 실행")
    ap.add_argument("--config", default="configs/grid_coarse.yaml")
    ap.add_argument("--lli", default=None)
    ap.add_argument("--lam-pe", dest="lam_pe", default=None)
    ap.add_argument("--lam-ne", dest="lam_ne", default=None)
    ap.add_argument("--lam-pe-type", dest="lam_pe_type", default=None)
    ap.add_argument("--lam-ne-type", dest="lam_ne_type", default=None)
    ap.add_argument("--noise", default=None)
    ap.add_argument("--noise-seed", dest="noise_seed", default=None)
    ap.add_argument("--nproc", type=int, default=multiprocessing.cpu_count())
    ap.add_argument("--chunk-size", dest="chunk_size", type=int, default=None)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dry-run", dest="dry_run", action="store_true")
    ap.add_argument("--out", required=True)
    ap.add_argument("--leg", default=None,
                    help="`LEG_PRESERVATION.yaml` 의 `planned:` 에서 찾을 다리 "
                         "이름 (48차 P0-5 — 없으면 LEG/CANONICAL_RUN 환경변수)")
    ap.add_argument("--tag", default="")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = load_config(args.config)
    validate_config(cfg)

    # ★ 10차 자체 리뷰 — CLI 덮어쓰기는 **cfg 에 먼저 반영**한다. 예전에는 조건
    #   생성만 CLI seed 를 쓰고, 서명(grid_run_spec)과 curves_manifest 는 config
    #   의 seed(42)를 봉인했다 — 서명된 재현 기록이 거짓이 된다.
    if args.noise_seed is not None:
        cfg.setdefault("grid", {})["noise_seed"] = int(args.noise_seed)

    conds = conditions_from_config(cfg, cli={
        "lli": args.lli, "lam_pe": args.lam_pe, "lam_ne": args.lam_ne,
        "lam_pe_type": args.lam_pe_type, "lam_ne_type": args.lam_ne_type,
        "noise": args.noise,     # noise_seed 는 위에서 cfg 로 일원화했다
    })
    chunk = args.chunk_size or int(cfg.get("run", {}).get("chunk_size", 200))

    summary = run_grid(cfg, conds, nproc=args.nproc, chunk_size=chunk,
                       out_dir=args.out, resume=args.resume, dry_run=args.dry_run,
                       leg=args.leg)
    if args.tag and not summary.get("dry_run"):
        write_manifest(args.out, {"tag": args.tag})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
