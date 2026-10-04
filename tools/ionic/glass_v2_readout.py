#!/usr/bin/env python3
"""glass_v2_readout.py — li2s 소셀 유리 MD **v2 카드** 판독 (회신 CO 개정 · **결과 보기 전에 커밋** · 외부 1저자 트랙).

    python3 tools/ionic/glass_v2_readout.py --root <ROOT> --out <ROOT>/readout_v2/readout_v2.json
    python3 tools/ionic/glass_v2_readout.py --selftest

    ROOT/seed<S>/T<T>/d0.00_cfg0/T<T>/{msd.json, traj.xyz, aimd_results.json}  — 두 기계 런을 한 곳에 합친 뒤.

⛔ 트랙 li2s = 외부 1저자. 이 도구는 결과 전에 박힌 규칙(카드 v2 §4·§5 + 개정 CO)을 **기계적으로 적용**한다.
   갈래 확정·해석은 외부 1저자 몫이다. 사용자의 실행 승인은 그 동의를 대신하지 않는다.

무엇을 하나 (순서 고정)
  런마다
    C1   MTO 곡선 창끝 MSD (t ≤ 50 ps 의 최댓값 — `msd_diffusive_check` 기본 모드의 'MSD@hi' 와 같은 식) ≥ 3 Å²
    C2   β_MTO (2–50 ps log-log) · σ = 블록 부트스트랩 사다리 (원점 수 1…512 중 **블록 수 ⌈n/b⌉ ≥ 8** 인 데까지) **끝값**
         · 2σ · 가까운 쪽 문턱 (회신 CD·CH·CL) · **끝 두 b 규칙** (통과가 한쪽뿐이면 경계 · 회신 CO) → 최종 C2
    기록 열 (판정 아님)
         · 공통 b = 256 σ 로 낸 C2 (회신 CO ② — 두 온도를 같은 잣대로) · 옛 사다리 (b ≤ 32) 끝값 판정 (카드 참고 열)
         · σ 거리 (부호: 구간 안 +, 밖 −) — 끝 b · 앞 b · 공통 b (회신 CO Q-CO-2 near-miss)
         · β_MTO(50–200 ps) 와 그 σ (같은 사다리 끝 · 회신 CO 보조 창) · β_STO 병기
         · 골격 세 지표 (`quench_ss_event.production_framework` · 회신 CO Q-CO-4 숫자 · 첫 프레임 대비 + 글자 그대로)
  온도별
    N = C1 ∧ 최종 C2 '통과' 수 · 공통 b 로 낸 N (기록) · 옛 사다리로 낸 N (참고) · 런별 σ 거리 다섯 (near-miss)
    D 시드 간 상대 산포 — D/중앙값 · IQR/중앙값 (**절대값은 화면·산출물에 안 싣는다**) · 기계별 β (기술 통계)
  갈래 (카드 §4) — N₆₀₀ ≤ 2 → v2-1 · N₆₀₀ ≥ 3 ∧ N₅₅₀ ≤ 2 → v2-2 · 둘 다 ≥ 3 → v2-3. 공통 b 로 낸 갈래도 나란히 (기록).
  옛 550 K (같은 다섯 구조 · 다른 MD 난수 · 400 ps) β_MTO 를 나란히 — **기술 비교 · 판정 아님** (회신 CO Q-CO-6).

⛔ 이 도구가 못 하는 것 / 안 하는 것
  · D·σ·Ea 의 절대값을 싣지 않는다 (인용정책 2026-09-18 · 카드 §1c) — D 는 상대 산포 계산에만 쓰고 버린다.
  · 갈래를 확정하지 않는다 · 문턱을 바꾸지 않는다 · 점·시드를 빼지 않는다 · 시드를 풀링하지 않는다.
  · 골격 지표로 N 을 바꾸지 않는다 (편입은 C1·C2 로만 · 회신 CH). `--framework gate` 면 D 상대 산포에서만 뺀다
    (그 적용 여부는 카드 개정이 정한다 — 기본은 기록).
  · σ 는 **하한**이다 — 800 ps 의 끝 b = 512 (51.2 ps) 도 창 길이에 겨우 닿았을 뿐 인접 블록이 독립이 아니다 (회신 CO ①).
    그래서 n·σ 는 상한이고 통과 선언은 낙관 쪽으로 틀릴 수 있다 — 끝 두 b 규칙이 그 쪽만 막는다.
  · 옛 550 K seed1 은 파일럿 P-2 라 초기구조가 다르다 (md_init_raw) — 비교표에 그렇게 적는다.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import statistics
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

TEMPS = (550, 600)
SEEDS = (1, 2, 3, 4, 5)
#: 카드 §1b 기계 배정 (교차) — 결과 전 고정
MACHINE = {(600, 2): "gabia", (550, 1): "gabia", (600, 4): "gabia", (550, 3): "gabia", (600, 5): "gabia",
           (600, 1): "kgy", (550, 2): "kgy", (600, 3): "kgy", (550, 4): "kgy", (550, 5): "kgy"}
LADDER = (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512)
MIN_BLOCKS = 8
COMMON_B = 256
OLD_LADDER_MAX = 32
WINDOW = (2.0, 50.0)
WINDOW_AUX = (50.0, 200.0)
C1_MIN_A2 = 3.0
N_THRESH = 3
CH_RECORD = REPO / "db" / "properties" / "lpscl_smallcell_glass_md_amendment_ch_2026_09_28.json"


def ladder_for(n_origin) -> list[int]:
    """카드 규칙: 블록 수 ⌈n/b⌉ ≥ 8 인 b 까지."""
    return [b for b in LADDER if math.ceil(n_origin / b) >= MIN_BLOCKS]


def signed_n_sigma(v) -> float | None:
    """`_boundary_verdict` 결과 → 부호 있는 σ 거리 (구간 안 +, 밖 −)."""
    if not v:
        return None
    return round(v["n_sigma"] if v["in_window"] else -v["n_sigma"], 3)


def branch(n600, n550) -> str:
    if n600 is None or n550 is None:
        return "판정 못 함 (N 이 비었다)"
    if n600 <= N_THRESH - 1:
        return "v2-1 (N₆₀₀ ≤ 2 — 600 K 파일럿의 통과가 새 난수 5 시드에서 재현되지 않음 → 닫는다)"
    if n550 <= N_THRESH - 1:
        return "v2-2 (N₆₀₀ ≥ 3 · N₅₅₀ ≤ 2 — 측정 가능 온도가 550 K 보다 위 → 그 위 설계는 새 결정)"
    return "v2-3 (N₆₀₀ ≥ 3 · N₅₅₀ ≥ 3 — 두 온도가 잰다 → 둘째 묶음은 외부 1저자 결정)"


def read_run(msd_json, n_boot=400, framework=True, mq=None):
    """런 하나 → 기록 (D 는 `_D_slope` 로만 들고 있다가 집계에서 버린다)."""
    import msd_diffusive_check as M
    jp = pathlib.Path(msd_json)
    d = json.loads(jp.read_text(encoding="utf-8"))
    sf, assumed, src = M.resolve_save_fs(jp, None)
    t_m, y_m = M._curve(d, mto=True, path=jp, rebuild=False)
    t_s, y_s = M._curve(d, mto=False)
    rec = {"msd_json": str(jp), "T_K": d.get("T_K"), "save_fs": sf, "save_fs_assumed": bool(assumed)}
    if not t_m:
        return {**rec, "error": "MTO 곡선이 없다 — 판정 못 함 (통과 아님)"}
    rec["C1_msd_at_50_mto_A2"] = max((v for u, v in zip(t_m, y_m) if u <= WINDOW[1]), default=None)
    rec["C1_pass"] = rec["C1_msd_at_50_mto_A2"] is not None and rec["C1_msd_at_50_mto_A2"] >= C1_MIN_A2
    b_mto = M.loglog_slope(t_m, y_m, *WINDOW)
    b_sto = M.loglog_slope(t_s, y_s, *WINDOW) if t_s else None
    b_aux = M.loglog_slope(t_m, y_m, *WINDOW_AUX)
    rec.update({"beta_MTO": b_mto, "beta_STO": b_sto, "beta_MTO_50_200": b_aux})
    lf = M.lin_fit(t_m, y_m, *WINDOW)
    rec["_D_slope"] = (lf[0] / 6.0) if lf else None
    po = M.msd_per_origin_from_traj(jp, save_fs=sf)
    if po is None:
        return {**rec, "error": "traj.xyz 를 못 읽었다 — σ 를 못 낸다 (통과 아님)"}
    lad = ladder_for(po["n_origin"])
    rec.update({"n_origin": po["n_origin"], "ladder": lad})

    def curve_for(lo, hi):
        return M.block_sigma_curve(
            lambda b: (M.block_bootstrap_beta(po["msd_per_origin"], po["t_ps"], lo, hi, b, n_boot, seed=0) or {})
            .get("sigma_beta"), lad)

    cur = curve_for(*WINDOW)
    rec["sigma_curve"] = cur
    if b_mto is None or not cur:
        return {**rec, "error": "β_MTO 또는 σ 사다리가 비었다 — 판정 못 함 (통과 아님)"}
    c2 = M.c2_verdicts(b_sto, b_mto, cur, common_b=COMMON_B, two_end=True)
    old = M.c2_verdicts(b_sto, b_mto, [p for p in cur if p[0] <= OLD_LADDER_MAX])
    te, cb = c2.get("two_end") or {}, c2.get("common_b") or {}
    rec["C2"] = {"sigma_end": c2["sigma"], "b_end": cur[-1][0], "verdict_end": c2["main"]["ch_2sigma_verdict"],
                 "n_sigma_end_signed": signed_n_sigma(c2["main"]),
                 "b_prev": te.get("b_prev"), "verdict_prev": te.get("verdict_prev"),
                 "n_sigma_prev_signed": (round(te["n_sigma_prev"] if c2["main"]["in_window"] else -te["n_sigma_prev"], 3)
                                         if te.get("n_sigma_prev") is not None else None),
                 "final_verdict": te.get("final_verdict"), "split_on_pass": te.get("split_on_pass"),
                 "sto_listed_verdict": (c2.get("listed") or {}).get("ch_2sigma_verdict")}
    rec["C2_common_b"] = ({"b": COMMON_B, "sigma": cb["sigma"], "verdict": cb["main"]["ch_2sigma_verdict"],
                           "n_sigma_signed": signed_n_sigma(cb["main"])} if "main" in cb
                          else {"b": COMMON_B, "status": cb.get("status", "못 냈다")})
    rec["C2_old_ladder_ref"] = {"b_end": max((p[0] for p in cur if p[0] <= OLD_LADDER_MAX), default=None),
                                "verdict": (old.get("main") or {}).get("ch_2sigma_verdict"),
                                "⚠": "카드 참고 열 — 옛 판독과 나란히 보는 기록이지 판정이 아니다"}
    if b_aux is not None:
        cur_aux = curve_for(*WINDOW_AUX)
        aux = M.c2_verdicts(None, b_aux, cur_aux) if cur_aux else {}
        rec["aux_50_200"] = ({"beta_MTO": b_aux, "sigma_end": aux["sigma"], "b_end": cur_aux[-1][0],
                              "n_sigma_signed_vs_C2_band": signed_n_sigma(aux["main"]),
                              "in_C2_band": aux["main"]["in_window"],
                              "⚠": "기록 전용 — 판정 아님 (회신 CO 보조 창) · σ 하한"} if aux.get("main")
                             else {"beta_MTO": b_aux, "status": "σ 를 못 냈다"})
    else:
        rec["aux_50_200"] = {"status": "곡선이 200 ps 에 못 닿는다 — 못 쟀다"}
    if framework:
        try:
            import quench_ss_event as Q
            fw = Q.production_framework(jp.parent, mq or Q._load_mq(str(HERE)))
            rec["framework"] = {"framework_moved": fw["co_gate"]["framework_moved"],
                                "literal_framework_moved": fw["co_gate"]["literal_framework_moved"],
                                "criteria": fw["co_gate"]["criteria_vs_first_frame"],
                                "literal_criteria": fw["co_gate"]["literal_criteria"],
                                "P": fw["P"], "S_moved": fw["S"]["n_moved_first_ne_last"],
                                "S_transient": fw["S"]["n_transient_only"], "SS_new": fw["SS"]["n_new_pairs"],
                                "SS_at_first_frame": len(fw["SS"]["pairs_lt_cut_at_first_frame"]),
                                "literal": fw["literal"]}
        except Exception as e:                   # 못 쟀으면 '골격 이동 없음' 이 아니다
            rec["framework"] = {"status": f"못 쟀다 ({type(e).__name__}: {e})"}
    return rec


def run_pass(r) -> bool:
    """N 에 세는가 — C1 ∧ 최종 C2 '통과'. 오류·판정 보류(None)·경계는 통과가 아니다."""
    return bool(r.get("C1_pass")) and (r.get("C2") or {}).get("final_verdict") == "통과" and "error" not in r


def rel_spread(vals):
    v = sorted(x for x in vals if x is not None and x > 0)
    if len(v) < 2:
        return None
    med = statistics.median(v)
    q = statistics.quantiles(v, n=4, method="inclusive") if len(v) >= 2 else None
    return {"n": len(v), "D_over_median": [round(x / med, 4) for x in v],
            "IQR_over_median": round((q[2] - q[0]) / med, 4) if q else None,
            "max_over_min": round(v[-1] / v[0], 4)}


def old_550_reference(path=CH_RECORD):
    """옛 550 K 런의 β_MTO (같은 다섯 구조 · 다른 MD 난수 · 400 ps) — 기술 비교 전용."""
    try:
        d = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        rows = d["✅_본런_판독_결과_2026_09_30"]["C2_β_0.8–1.2_MTO_주_보수σ_2σ"]["런별"]
    except (OSError, ValueError, KeyError) as e:
        return {"status": f"옛 기록을 못 읽었다 ({type(e).__name__})"}
    out = {}
    for sd in SEEDS:
        key = "P2s1_T550" if sd == 1 else f"s{sd}_T550"
        if key in rows:
            out[sd] = {"beta_MTO_old_400ps": rows[key][0], "verdict_old_b32": rows[key][4], "key": key,
                       **({"⚠": "옛 seed1 = 파일럿 P-2 · 초기구조 md_init_raw (relax 판 아님) — 같은 구조가 아니다"} if sd == 1 else {})}
    return out


def aggregate(runs, framework_mode="record"):
    """{(T, seed): rec} → 온도별 N · near-miss · 상대 산포 · 갈래. ⛔ D 절대값은 결과에 남기지 않는다."""
    per_T = {}
    for T in TEMPS:
        rows = [(sd, runs.get((T, sd))) for sd in SEEDS]
        recs = [r for _, r in rows if r is not None]
        n = sum(1 for r in recs if run_pass(r))
        n_common = sum(1 for r in recs if r.get("C1_pass") and (r.get("C2_common_b") or {}).get("verdict") == "통과")
        n_old = sum(1 for r in recs if r.get("C1_pass") and (r.get("C2_old_ladder_ref") or {}).get("verdict") == "통과")
        near = [{"seed": sd, "machine": MACHINE.get((T, sd)),
                 "n_sigma_end": (r or {}).get("C2", {}).get("n_sigma_end_signed"),
                 "n_sigma_prev": (r or {}).get("C2", {}).get("n_sigma_prev_signed"),
                 "n_sigma_common_b": (r or {}).get("C2_common_b", {}).get("n_sigma_signed"),
                 "final": (r or {}).get("C2", {}).get("final_verdict") if r else "런 없음",
                 "C1": (r or {}).get("C1_pass")} for sd, r in rows]
        D_all = [r.get("_D_slope") for r in recs]
        D_pass = [r.get("_D_slope") for r in recs if run_pass(r)]
        excluded = []
        if framework_mode == "gate":
            excluded = [sd for sd, r in rows if r and (r.get("framework") or {}).get("framework_moved")]
            D_main = [r.get("_D_slope") for sd, r in rows if r and sd not in excluded]
        else:
            D_main = D_all
        mach = {}
        for sd, r in rows:
            if r:
                mach.setdefault(MACHINE.get((T, sd)), []).append({"seed": sd, "beta_MTO": r.get("beta_MTO")})
        per_T[T] = {"N": n, "of": len(SEEDS), "n_runs_present": len(recs),
                    "N_common_b256_record": n_common, "N_old_ladder_ref": n_old,
                    "near_miss_sigma_distances": near,
                    "D_relative_spread": rel_spread(D_main),
                    "D_relative_spread_C1C2_pass_only_record": rel_spread(D_pass),
                    "framework_excluded_from_D": excluded if framework_mode == "gate" else "기록 모드 — 빼지 않았다",
                    "framework_moved_count": sum(1 for r in recs if (r.get("framework") or {}).get("framework_moved")),
                    "framework_literal_moved_count": sum(1 for r in recs
                                                         if (r.get("framework") or {}).get("literal_framework_moved")),
                    "beta_by_machine_descriptive": mach}
    #: ⛔ 2026-10-04 (gabia 첫 판독 시도 · 결과 전) — 오류 런을 '통과 아님' 으로만 세면 N 이 줄어 **갈래가 '닫는다'(v2-1)
    #:   로 갈 수 있다** — 도구가 못 잰 것이 판정이 된다. 카드 §4 '점·시드를 빼지 않는다 (런 유효성 위반은 판독 전 재실행)'
    #:   대로 **오류 런이 하나라도 있으면 갈래를 내지 않는다** (통과도 미통과도 아니다 · 고치고 다시 판독).
    errs = sorted(f"T{k[0]} seed{k[1]}: {r['error']}" for k, r in runs.items() if r and r.get("error"))
    errs += [f"T{T} seed{sd}: 런 없음" for T in TEMPS for sd in SEEDS if (T, sd) not in runs]
    if errs:
        held = f"판정 보류 — 오류·결측 런 {len(errs)} 개 (통과도 미통과도 아니다 · 고치고 다시 판독한다)"
        b_main = b_common = held
    else:
        b_main = branch(per_T[600]["N"], per_T[550]["N"])
        b_common = branch(per_T[600]["N_common_b256_record"], per_T[550]["N_common_b256_record"])
    return {"per_T": per_T, "branch": b_main, "branch_common_b256_record": b_common, "errors": errs,
            "branch_same_under_common_b": b_main.split(" ")[0] == b_common.split(" ")[0],
            "framework_mode": framework_mode,
            "⛔": "갈래는 규칙의 기계적 적용이다 — 확정은 외부 1저자 · D·σ 절대값은 싣지 않는다"}


def exit_code(agg) -> int:
    """판독 종료 코드 — 오류·결측 런이 있어 갈래를 안 냈으면 3 (통과·미통과가 아니다), 아니면 0."""
    return 3 if agg.get("errors") else 0


def collect(root, n_boot=400, framework=True):
    root = pathlib.Path(root)
    runs, missing = {}, []
    mq = None
    if framework:
        import quench_ss_event as Q
        mq = Q._load_mq(str(HERE))
    for T in TEMPS:
        for sd in SEEDS:
            jp = root / f"seed{sd}" / f"T{T}" / "d0.00_cfg0" / f"T{T}" / "msd.json"
            if not jp.is_file():
                missing.append(str(jp))
                continue
            print(f"  … T{T} seed{sd} ({MACHINE.get((T, sd))})", flush=True)
            runs[(T, sd)] = read_run(jp, n_boot=n_boot, framework=framework, mq=mq)
    return runs, missing


def strip_D(runs):
    return {k: {kk: vv for kk, vv in r.items() if kk != "_D_slope"} for k, r in runs.items()}


def show(agg, runs, old):
    L = []
    for T in TEMPS:
        p = agg["per_T"][T]
        L.append(f"■ {T} K — N = {p['N']}/{p['of']} (C1 ∧ 최종 C2 · 끝 두 b 규칙) · 공통 b 256 으로는 {p['N_common_b256_record']} (기록) "
                 f"· 옛 사다리(b ≤ 32)로는 {p['N_old_ladder_ref']} (참고)")
        for nm in p["near_miss_sigma_distances"]:
            r = runs.get((T, nm["seed"])) or {}
            c2 = r.get("C2") or {}
            aux = r.get("aux_50_200") or {}
            fw = r.get("framework") or {}
            L.append(f"   seed{nm['seed']} {nm['machine']:5s} C1 {'통과' if nm['C1'] else '미달'} "
                     f"({r.get('C1_msd_at_50_mto_A2', float('nan')):.1f} Å²) · β_MTO {r.get('beta_MTO') or float('nan'):.4f} "
                     f"· σ 거리 끝 b{c2.get('b_end')} {nm['n_sigma_end']} · 앞 b{c2.get('b_prev')} {nm['n_sigma_prev']} "
                     f"· 공통 b256 {nm['n_sigma_common_b']} → **{nm['final']}** "
                     f"| 50–200 β {aux.get('beta_MTO') if aux.get('beta_MTO') is None else round(aux['beta_MTO'], 4)} "
                     f"({aux.get('n_sigma_signed_vs_C2_band', '—')}σ · 기록) "
                     f"| 골격 {'이동' if fw.get('framework_moved') else ('—' if 'status' in fw else '없음')}"
                     f"{' (글자 그대로 이동)' if fw.get('literal_framework_moved') and not fw.get('framework_moved') else ''}"
                     + (f" | ⛔ {r['error']}" if r.get("error") else ""))
        sp = p["D_relative_spread"]
        L.append(f"   D 시드 간 상대 산포 (중앙값 대비 · 절대값 없음): {sp}")
        L.append(f"   기계별 β_MTO (기술 통계 · 판정 아님): "
                 + " · ".join(f"{m}: {[round(x['beta_MTO'], 4) if x['beta_MTO'] else None for x in v]}"
                              for m, v in p["beta_by_machine_descriptive"].items()))
    L.append(f"→ 갈래 (규칙 적용): {agg['branch']}")
    L.append(f"   공통 b 256 으로 낸 갈래 (기록): {agg['branch_common_b256_record']} · "
             f"{'같다' if agg['branch_same_under_common_b'] else '⚠ 다르다 — 갈래가 잣대 차이에서 왔을 수 있다 (회신 CO ②)'}")
    if isinstance(old, dict) and "status" not in old:
        L.append("   옛 550 K β_MTO (400 ps · 다른 난수 · 기술 비교 · 판정 아님): "
                 + " · ".join(f"seed{sd} {v['beta_MTO_old_400ps']}{'⚠' if sd == 1 else ''}" for sd, v in old.items())
                 + "  (⚠ seed1 = 파일럿 P-2 · 초기구조 다름)")
    return L


def _selftest() -> int:
    import tempfile
    fails = []

    def ck(name, cond):
        print(f"  {'✓' if cond else '✗'} {name}", flush=True)
        if not cond:
            fails.append(name)

    ck("사다리: 800 ps (원점 4000) → 끝 512 · 400 ps (2000) → 끝 256 (카드 §1b)",
       ladder_for(4000)[-1] == 512 and ladder_for(2000)[-1] == 256 and ladder_for(2000)[-2] == 192)
    ck("갈래: N600 2 → v2-1 · (3, 2) → v2-2 · (3, 3) → v2-3",
       branch(2, 5).startswith("v2-1") and branch(3, 2).startswith("v2-2") and branch(3, 3).startswith("v2-3"))
    ck("⛔음성 갈래: N 이 비면 판정 못 함", branch(None, 3).startswith("판정 못 함"))

    def fake(final, c1=True, common="통과", D=1.0, fw=False, end=2.5, common_n=2.6):
        return {"C1_pass": c1, "C1_msd_at_50_mto_A2": 30.0 if c1 else 2.0, "beta_MTO": 0.9, "_D_slope": D,
                "C2": {"final_verdict": final, "n_sigma_end_signed": end, "n_sigma_prev_signed": end - 0.1, "b_end": 256, "b_prev": 192},
                "C2_common_b": {"verdict": common, "n_sigma_signed": common_n},
                "C2_old_ladder_ref": {"verdict": "통과"}, "aux_50_200": {"beta_MTO": 1.0},
                "framework": {"framework_moved": fw, "literal_framework_moved": fw}}
    runs = {(600, 1): fake("통과", D=1.0), (600, 2): fake("통과", D=1.2), (600, 3): fake("경계 · 끝 두 b 갈림", D=0.8),
            (600, 4): fake("통과", c1=False, D=1.1), (600, 5): fake(None, D=0.9),
            (550, 1): fake("통과", D=0.5), (550, 2): fake("통과", D=0.6), (550, 3): fake("통과", D=0.7, fw=True),
            (550, 4): fake("미통과", common="통과", D=0.4), (550, 5): fake("경계 · 구분 불가", common="통과", D=0.55)}
    ag = aggregate(runs)
    ck("N600 = 2: 경계(끝 두 b 갈림)·C1 미달·판정 보류(None)는 세지 않는다",
       ag["per_T"][600]["N"] == 2 and ag["per_T"][550]["N"] == 3)
    ck("⛔ 갈래 v2-1 (N600 2 · 550 이 3 이어도 600 이 먼저 닫는다)", ag["branch"].startswith("v2-1"))
    ck("⛔ 공통 b 로는 갈래가 v2-3 으로 갈린다 → '다르다' 표시 (회신 CO ②: 잣대 차이를 바로 보이게)",
       ag["branch_common_b256_record"].startswith("v2-3") and ag["branch_same_under_common_b"] is False
       and any("⚠ 다르다" in x for x in show(ag, runs, {})))
    ck("near-miss: 온도마다 σ 거리 다섯을 전부 싣는다 (판정 보류 런 포함)",
       len(ag["per_T"][600]["near_miss_sigma_distances"]) == 5 and ag["per_T"][600]["near_miss_sigma_distances"][4]["final"] is None)
    sp = ag["per_T"][550]["D_relative_spread"]
    ck("D 상대 산포: 다섯 다 (기록 모드) · D/중앙값 · 절대값은 결과에 없다",
       sp["n"] == 5 and sp["D_over_median"][2] == 1.0 and "0.55" not in json.dumps(ag) and "_D_slope" not in json.dumps(ag))
    ag2 = aggregate(runs, framework_mode="gate")
    ck("--framework gate: 골격 이동 런은 D 산포에서만 빠진다 · N 은 그대로",
       ag2["per_T"][550]["D_relative_spread"]["n"] == 4 and ag2["per_T"][550]["N"] == 3
       and ag2["per_T"][550]["framework_excluded_from_D"] == [3])
    ck("⛔ 기록 모드에서는 빼지 않는다", aggregate(runs)["per_T"][550]["framework_excluded_from_D"] == "기록 모드 — 빼지 않았다")
    runs2 = dict(runs); runs2[(600, 3)] = fake("통과")
    ck("갈래 v2-3 (600 3 · 550 3)", aggregate(runs2)["branch"].startswith("v2-3"))
    runs3 = dict(runs2); runs3[(550, 3)] = {"error": "traj.xyz 를 못 읽었다", "C1_pass": True,
                                             "C2": {"final_verdict": "통과"}}
    ck("⛔음성 오류 런은 '통과' 가 적혀 있어도 세지 않는다", aggregate(runs3)["per_T"][550]["N"] == 2)
    _a3 = aggregate(runs3)
    ck("⛔음성 오류 런이 하나라도 있으면 갈래를 내지 않는다 (판정 보류 — '닫는다' 로 새지 않는다)",
       _a3["branch"].startswith("판정 보류") and _a3["branch_common_b256_record"].startswith("판정 보류") and len(_a3["errors"]) == 1)
    runs4 = dict(runs2); runs4.pop((600, 5))
    ck("⛔음성 런이 빠져도 갈래를 내지 않는다", aggregate(runs4)["branch"].startswith("판정 보류"))
    ck("양성 오류가 없으면 errors 가 비고 갈래가 나온다", aggregate(runs2)["errors"] == [])
    ck("⛔음성 종료 코드: 보류면 3 · 갈래가 나오면 0 (스크립트가 보류를 성공으로 넘기지 않는다)",
       exit_code(_a3) == 3 and exit_code(aggregate(runs2)) == 0)
    old = old_550_reference()
    ck("옛 550 K 기술 비교: 다섯 시드 · seed1 은 초기구조가 다르다고 적는다",
       isinstance(old, dict) and len(old) == 5 and "⚠" in old[1] and old[2]["beta_MTO_old_400ps"] == 0.8198)
    ck("⛔음성 옛 기록이 없으면 '못 읽었다' (지어내지 않는다)", "status" in old_550_reference("/nonexistent.json"))

    # 실제 경로: 짧은 합성 궤적 하나 (Li 20 · PS₄ 1 · 1100 프레임 = 110 ps · save 100 fs)
    try:
        import numpy as np
        from ase import Atoms
        from ase.io import write
        import msd_diffusive_check as M
    except ImportError as e:
        ck(f"(합성 궤적 시험 건너뜀 — {e})", True)
        print(f"selftest {'PASS' if not fails else 'FAIL'} ({len(fails)} 실패)")
        return 0 if not fails else 1
    with tempfile.TemporaryDirectory() as td:
        rd = pathlib.Path(td) / "seed1" / "T600" / "d0.00_cfg0" / "T600"
        rd.mkdir(parents=True)
        rng = np.random.default_rng(1)
        L = 12.0
        P = np.array([6.0, 6.0, 6.0])
        v = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(3) * 2.05
        li = rng.uniform(0, L, (20, 3))
        for k in range(1100):
            li = li + rng.normal(0, 0.25, li.shape)                 # 브라운 — β ≈ 1
            pos = np.vstack([P, P + v, li]) + np.vstack([rng.normal(0, 0.02, (5, 3)), np.zeros((20, 3))])
            write(str(rd / "traj.xyz"), Atoms(["P"] + ["S"] * 4 + ["Li"] * 20, positions=pos, cell=np.eye(3) * L, pbc=True),
                  format="extxyz", append=True)
        (rd / "aimd_results.json").write_text(json.dumps({"T_K": 600.0, "save_fs": 100.0, "n_frames": 1100,
                                                          "prod_ps": 110.0, "dt_fs": 2.0}))
        js = rd / "msd.json"
        js.write_text(json.dumps({"T_K": 600.0, "times_ps": [0.1 * i for i in range(1, 551)],
                                  "msd_Li_A2": [0.375 * 0.1 * i for i in range(1, 551)], "save_fs": 100.0}))
        got = M.mto_from_traj(js, 100.0)
        ck("합성 MTO 곡선을 드라이버 함수(tools/modelc_v3/disorder_ensemble_diffusion.py · msd_multi_origin)로 만들었다 "
           "— 없으면 꺼낼 때 그 파일도 같이 꺼낸다 (판독 경로는 msd.json 의 MTO 를 읽어 필요 없다)", bool(got))
        if not got:
            print(f"selftest FAIL ({len(fails)} 실패) — 드라이버가 없어 합성 시험을 못 했다")
            return 1
        dd = json.loads(js.read_text()); dd.update(got or {}); js.write_text(json.dumps(dd))
        r = read_run(js, n_boot=40)
        ck("합성 브라운 궤적: C1 통과 · β_MTO ≈ 1 · σ 사다리 끝 b = 64 (원점 550 → 블록 ≥ 8)",
           r.get("C1_pass") and r.get("beta_MTO") and 0.85 < r["beta_MTO"] < 1.15 and r["ladder"][-1] == 64)
        ck("합성: 최종 C2 · 끝 두 b · 공통 b 256 은 사다리에 없어 '못 냈다' · 옛 사다리 끝 32",
           r["C2"]["final_verdict"] in ("통과", "경계 · 구분 불가", "경계 · 끝 두 b 갈림", "미통과")
           and r["C2"]["b_prev"] == 48 and "status" in r["C2_common_b"] and r["C2_old_ladder_ref"]["b_end"] == 32)
        ck("합성: 보조 창 50–200 은 곡선이 55 ps 에서 끝나 '못 쟀다' (지어내지 않는다)", "status" in r["aux_50_200"])
        ck("합성: 골격 지표 — 움직임 없음 (첫 프레임 대비 · 글자 그대로)",
           (r.get("framework") or {}).get("framework_moved") is False
           and (r.get("framework") or {}).get("literal_framework_moved") is False)
        ck("⛔ 산출물(strip_D)에 D 가 없다", "_D_slope" not in json.dumps({"T600_s1": strip_D({(600, 1): r})[(600, 1)]}, default=str))
        (rd / "traj.xyz").unlink()
        r2 = read_run(js, n_boot=10, framework=False)
        ck("⛔음성 궤적이 없으면 error · 통과 아님", "error" in r2 and not run_pass(r2))
    print(f"selftest {'PASS' if not fails else 'FAIL'} ({len(fails)} 실패)")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="li2s 소셀 유리 MD v2 판독 (회신 CO 개정 · 결과 전 커밋)")
    ap.add_argument("--root")
    ap.add_argument("--out")
    ap.add_argument("--n_boot", type=int, default=400)
    ap.add_argument("--framework", choices=["record", "gate", "off"], default="record",
                    help="골격 세 지표: record = 기록만 (기본) · gate = D 상대 산포에서 뺀다 (N 은 그대로) · off = 안 잰다")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.root:
        ap.error("--root 가 필요하다")
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    print(f"li2s v2 판독 · root {a.root} · n_boot {a.n_boot} · 골격 {a.framework} · 사다리 블록 ≥ {MIN_BLOCKS} · 공통 b {COMMON_B}")
    runs, missing = collect(a.root, n_boot=a.n_boot, framework=(a.framework != "off"))
    if missing:
        print(f"⛔ msd.json 이 없는 런 {len(missing)} 개 — 판정하지 않는다 (카드: 점·시드를 빼지 않는다):")
        for m in missing:
            print("   ·", m)
        return 2
    agg = aggregate(runs, framework_mode=a.framework if a.framework != "off" else "record")
    old = old_550_reference()
    print("\n".join(show(agg, runs, old)))
    if agg["errors"]:
        print("⛔ 오류 런이 있어 갈래를 내지 않았다 (rc 3):")
        for e in agg["errors"]:
            print("   ·", e)
    if a.out:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.out).write_text(json.dumps({"aggregate": agg, "runs": {f"T{k[0]}_s{k[1]}": v for k, v in strip_D(runs).items()},
                                                   "old_550_descriptive": old, "card": "db/properties/lpscl_smallcell_glass_md_v2_estimand_2026_09_30.json",
                                                   "amendment": "db/properties/lpscl_smallcell_glass_md_v2_amendment_co_2026_10_04.json"},
                                                  ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
        print(f"-> {a.out}")
    return exit_code(agg)


if __name__ == "__main__":
    sys.exit(main())
