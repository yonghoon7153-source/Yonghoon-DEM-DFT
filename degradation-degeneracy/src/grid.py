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
from src.io import (append_failed, base_manifest, load_completed, mark_completed,
                    merge_chunks, save_chunk, write_manifest)
from src.modes import Baseline, InfeasibleConditionError, build_overrides
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
                "error": f"infeasible: {e}", "elapsed_s": 0.0}

    res = run_one(cfg, ov, protocol_name)
    if not res.ok:
        return {"cond": asdict(cond), "cond_id": cond.cond_id,
                "error": res.error, "elapsed_s": res.elapsed_s}

    try:
        curves = extract_curves(res.solution, n_trim, n_interp)
    except Exception as e:  # noqa: BLE001
        return {"cond": asdict(cond), "cond_id": cond.cond_id,
                "error": f"extract: {type(e).__name__}: {e}",
                "elapsed_s": res.elapsed_s}

    v_noisy = add_noise(curves["v_full"], cond.noise, cond.seed)
    return {
        "cond": asdict(cond), "cond_id": cond.cond_id, "error": None,
        "elapsed_s": res.elapsed_s,
        "q_mah": curves["q_mah"],
        "x_norm": curves["x_norm"].tolist(),
        "v_pe": curves["v_pe"].tolist(),
        "v_ne": curves["v_ne"].tolist(),
        "v_full": curves["v_full"].tolist(),
        "v_full_noisy": v_noisy.tolist(),
    }


def _result_to_frame(r: dict, protocol_name: str) -> pd.DataFrame:
    n = len(r["x_norm"])
    c = r["cond"]
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

def run_grid(cfg: dict, conditions: list[Condition], nproc: int,
             chunk_size: int, out_dir: str | Path,
             resume: bool = False, dry_run: bool = False) -> dict:
    """조합 격자 실행. 반환: 요약 dict."""
    from joblib import Parallel, delayed
    from tqdm import tqdm

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    protocol_name = cfg.get(GRID_PROTOCOL_KEY, "charge_first")

    # ── resume: 완료 조건 건너뛰기 ──
    done: set[str] = load_completed(out_dir) if resume else set()
    todo = [c for c in conditions if c.cond_id not in done]
    if resume and done:
        log.info("resume: %d개 완료 확인, %d개 남음", len(done), len(todo))

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

    for c, reason in infeasible:
        append_failed(out_dir, c.cond_id, asdict(c), f"infeasible: {reason}")
        mark_completed(out_dir, c.cond_id)   # 재실행에서도 건너뛰도록

    # ── chunk 단위 병렬 실행 ──
    n_failed = len(infeasible)
    n_ok = 0
    t_start = time.perf_counter()
    chunk_idx = _next_chunk_idx(out_dir)

    with tqdm(total=len(feasible), desc="grid", unit="cond") as bar:
        for start in range(0, len(feasible), chunk_size):
            chunk = feasible[start:start + chunk_size]
            results = Parallel(n_jobs=nproc, backend="loky")(
                delayed(_solve_condition)(cfg, c, d_dict, protocol_name)
                for c in chunk
            )
            frames = []
            for r in results:
                if r["error"] is not None:
                    append_failed(out_dir, r["cond_id"], r["cond"], r["error"])
                    n_failed += 1
                else:
                    frames.append(_result_to_frame(r, protocol_name))
                    n_ok += 1
            if frames:
                save_chunk(pd.concat(frames, ignore_index=True), out_dir, chunk_idx)
                chunk_idx += 1
            # 청크 flush 후에만 완료 마킹 → kill돼도 데이터 없는 완료가 없음
            for r in results:
                mark_completed(out_dir, r["cond_id"])
            bar.update(len(chunk))

    merged = merge_chunks(out_dir, "curves.parquet")
    elapsed = time.perf_counter() - t_start

    # 누적 집계 (resume 시 이전 실행분 포함) — 파일 기준이 진실
    n_done_total = len(load_completed(out_dir))
    fail_path = out_dir / "failed.csv"
    n_failed_total = (max(0, len(fail_path.read_text(encoding="utf-8").splitlines()) - 1)
                      if fail_path.exists() else 0)
    write_manifest(out_dir, {
        "n_ok": n_ok, "n_failed": n_failed,               # 이번 호출분
        "n_completed_total": n_done_total,                 # 누적 (failed 포함)
        "n_failed_total": n_failed_total,
        "n_curves_total": n_done_total - n_failed_total,
        "elapsed_s": round(elapsed, 1),
        "curves_parquet": str(merged) if merged else None,
        "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    log.info("grid 완료: ok=%d failed=%d (누적 곡선 %d) elapsed=%.1fs",
             n_ok, n_failed, n_done_total - n_failed_total, elapsed)
    return {"n_ok": n_ok, "n_failed": n_failed,
            "n_curves_total": n_done_total - n_failed_total,
            "elapsed_s": elapsed, "out_dir": str(out_dir)}


def _next_chunk_idx(out_dir: Path) -> int:
    files = sorted((Path(out_dir) / "chunks").glob("chunk_*.parquet"))
    if not files:
        return 0
    return int(files[-1].stem.split("_")[1]) + 1


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
    ap.add_argument("--tag", default="")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = load_config(args.config)
    validate_config(cfg)

    conds = conditions_from_config(cfg, cli={
        "lli": args.lli, "lam_pe": args.lam_pe, "lam_ne": args.lam_ne,
        "lam_pe_type": args.lam_pe_type, "lam_ne_type": args.lam_ne_type,
        "noise": args.noise, "noise_seed": args.noise_seed,
    })
    chunk = args.chunk_size or int(cfg.get("run", {}).get("chunk_size", 200))

    summary = run_grid(cfg, conds, nproc=args.nproc, chunk_size=chunk,
                       out_dir=args.out, resume=args.resume, dry_run=args.dry_run)
    if args.tag and not summary.get("dry_run"):
        write_manifest(args.out, {"tag": args.tag})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
