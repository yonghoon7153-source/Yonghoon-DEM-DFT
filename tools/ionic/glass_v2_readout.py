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

대조 계 카드 (a-Li₃PS₄ 유리 · 회신 CR · 2026-10-05) — 두 계의 D 상대차 R
    python3 tools/ionic/glass_v2_readout.py --detect_limit [--sigma_ln 0.026 0.094] [--n_a 5 --n_b 5]
  · `ratio_boot` — R = 중앙값 D_A / 중앙값 D_B · 계 안에서만 복원추출하는 시드 부트스트랩 95 % 백분위 구간.
    **두 계 모두 통과 시드 ≥ 4 일 때만** R 을 낸다 (회신 CR Q-CR-3 — 3 개 중앙값의 비는 '구분 안 됨' 이
    계의 성질인지 표본 수인지 못 가른다).
  · `ratio_detect_limit` — 위와 **같은 부트스트랩 함수**로 모의 실험을 돌려, 참 비가 R 일 때 구간이 1 을 벗어날
    확률을 낸다 → R₅₀ · R₈₀ (50 · 80 % 검출) 과 R = 1 의 오검출률. 결과 전에 적어 두어 '구분되지 않았다' 를
    '같다' 로 읽지 않게 한다 (회신 CR · 편지 BU 의 검출한계 형식).
  대조 판독 (2026-10-14 · 카드 §4 · §5 · 결과 전 커밋 · 점검 목록 lpscl_smallcell_glass_control_li3ps4_readout_checklist_2026_10_14.json)
    python3 tools/ionic/glass_v2_readout.py --control --root_a <A 600 K 다섯 루트> --root_b <B 600 K 다섯 루트> --out <json>
  · 런마다 C1 · 최종 C2 (v2 600 K 와 같은 식) · 골격 네 기준 (① P ≤ 5 % · ② S 이동 0 · ③ 새 S–S 0 · ④ 일시 변화 ≤ 5) ·
    기록 열 (β_STO · STO−MTO · 50–200 ps β · N_eff · 생산 T · 5 ps lag p90² · 골격 글자 그대로).
  · 계별 N = C1 ∧ C2 · R 집합 = N ∧ 골격 통과 → 갈래 c2 (N_B ≤ 2) · c1a / c1b (R 집합 둘 다 ≥ 4 · 구간이 1 밖 / 포함) ·
    c1c (그 밖) · 오류 · 결측 · 골격 못 잰 런이 있으면 판정 보류 (종료 3) · 런이 빠지면 판독하지 않는다 (종료 2).
  · 계별 시드 간 상대 산포 (카드 §1 보고량 ③ · R 집합 = 주 · N 집합 = 기록 · IQR/중앙 · max/min · sd(ln D)).
  · 대조 잡 (결과 전 박음): A 600 K 다섯을 다시 읽어 v2 마감의 D/중앙 (넷째 자리) 과 창별 p90² (±0.05 Å²) 를 재현하는가 —
    D/중앙이 어긋나거나 마감을 못 읽으면 판정 보류 (A 쪽 R 을 믿을 수 없다) · p90² 만 어긋나면 B p90² 를 같은 잣대로 안 읽는다.
  · p90² 창 수 = 선언된 prod_ps / 50 (aimd_results.json) — 400 ps 는 4000 프레임이라 프레임 수로 세면 7 창이 된다.
  ⛔ 대조 모드가 못 하는 것: 담금질 기록 (밀도 · T₅₀ · 시드 게이트) 과 기계 · 벽시계 · VRAM 은 러너 기록 (runlog) 에서 온다 —
    이 도구가 다시 재지 않는다 · 갈래를 확정하지 않는다 (외부 1저자) · Tg 를 맞추지 않는다.
  B 측정 가능 조건 카드 ① 단계 (2026-10-19 · 카드 lpscl_smallcell_glass_control_bmeasurable_estimand_2026_10_14 §1b · §4 ·
  개정 CX · 결과 전 커밋)
    python3 tools/ionic/glass_v2_readout.py --bmeas_b --root_a <A 600 K 다섯 루트> --root_b <B 650 K 다섯 루트> --out <json>
  · B 650 K 다섯만 — 런마다 C1 · 최종 C2 · 골격 네 기준 (대조 모드와 같은 함수 `_control_system` · 같은 숫자) → N_B ·
    b1 (N_B ≤ 2 → A 650 K 를 돌리지 않고 닫는다) · b2 (N_B ≥ 3 → ② 단계 A 650 K · 새 GPU 결정 · B R 집합 < 4 면 '② 를 돌려도
    R 은 없다' 를 적고 A 실행은 외부 1저자 확인) · 허용 문장 (카드 §1a · 단서를 문장 안에 — 개정 CX §8).
  · 대조 잡 둘 (상시 · 개정 CX §7): ① A 600 K ↔ v2 마감 ② A 600 K ↔ 10-14 판독 기록 (도구를 바꿨으니 — 행 그대로 ·
    같은 n_boot) — 다르거나 못 보면 판정 보류. 최종 C2 가 빈 런도 판정 보류 (미통과로 세지 않는다). 런이 빠지면 읽기 전에 종료 2.
  · 기록 (개정 CX §4): 골격 네 지표 분포 (모든 런 · B 650 · A 600 · B 600 기록) · p90² 창 초과 · 포화 런 수 ·
    b2 · B R 집합 ≥ 4 면 ② 단계 검출한계를 A 650 K 결과 전에 낸다 (B 650 K 실측 σ_ln · A 600 K 기준 0.0935 가정).
  ⛔ ① 단계가 못 하는 것: R 을 내지 않는다 (A 650 K 가 없다 · 600 K 런을 650 K R 에 섞지 않는다) · 온도를 못 바꾼다
    (650 고정 · CLI 인자 없음) · ② 단계 판독 (A · B 650 K · R · b2a/b2b/b2c) 은 아직 없다 — b2 면 A 결과 전에 넣는다 ·
    갈래를 확정하지 않는다 (외부 1저자).
  ⛔ 검출한계가 못 하는 것: 산포 모양을 로그정규로 가정한다 (치우침·이상치는 σ 를 고르는 데서만 들어간다) ·
    B 의 산포는 가정이다 (기본 = A 와 같음) · 시드 다섯의 백분위 부트스트랩은 덜 덮인다 — 그건 R = 1 의
    오검출률 줄로만 보인다 (고치지 않고 적는다).
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
WINDOW_AUX = (50.0, 200.0)   # aux-window-ok: 회신 CO 기록 전용 열 (개정 CO 2026-10-04 비준) · 주 판정은 WINDOW (2,50) · 이 창으로 미통과 런을 구제하지 않는다
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


# ── 대조 계 카드 (회신 CR · 2026-10-05) — R 과 검출한계 (같은 부트스트랩) ─────────────
MIN_SEEDS_FOR_R = 4          # 회신 CR Q-CR-3: 두 계 모두 통과 시드 ≥ 4 일 때만 R
R_BOOT_SEED = 20261005       # 고정 난수 — 같은 입력이면 같은 구간
DETECT_GRID = (1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5, 1.75, 2.0)


def _boot_ratio_interval(a, b, n_boot, rng):
    """계 안에서만 복원추출 → 중앙값의 비 → 백분위 2.5 · 97.5. `ratio_boot` 와 `ratio_detect_limit` 가 **같이** 쓴다."""
    import numpy as np
    ia = rng.integers(0, len(a), (n_boot, len(a)))
    ib = rng.integers(0, len(b), (n_boot, len(b)))
    rb = np.median(a[ia], axis=1) / np.median(b[ib], axis=1)
    lo, hi = np.percentile(rb, [2.5, 97.5])
    return float(lo), float(hi)


def ratio_boot(d_a, d_b, n_boot=10000, seed=R_BOOT_SEED, min_seeds=MIN_SEEDS_FOR_R) -> dict:
    """R = median(D_A) / median(D_B) 와 시드 부트스트랩 95 % 구간 — 비만 돌려준다 (D 는 버린다)."""
    import numpy as np
    a = np.asarray([x for x in d_a if x is not None], float)
    b = np.asarray([x for x in d_b if x is not None], float)
    if len(a) < min_seeds or len(b) < min_seeds:
        return {"status": f"R 을 내지 않는다 — 통과 시드 A {len(a)} · B {len(b)} (둘 다 ≥ {min_seeds} 필요 · 회신 CR Q-CR-3)",
                "n_a": int(len(a)), "n_b": int(len(b))}
    if (a <= 0).any() or (b <= 0).any():
        return {"status": "D ≤ 0 인 시드가 있다 — 비가 정의되지 않아 R 을 내지 않는다", "n_a": int(len(a)), "n_b": int(len(b))}
    lo, hi = _boot_ratio_interval(a, b, n_boot, np.random.default_rng(seed))
    return {"R": float(np.median(a) / np.median(b)), "lo": lo, "hi": hi, "excludes_1": bool(lo > 1.0 or hi < 1.0),
            "n_a": int(len(a)), "n_b": int(len(b)), "n_boot": int(n_boot), "seed": int(seed)}


def ratio_detect_limit(sigma_ln, n_a=5, n_b=5, sigma_b=None, r_grid=DETECT_GRID, n_sim=2000, n_boot=2000,
                       seed=7) -> dict:
    """참 비 R 에서 이 설계가 '구간이 1 밖' 을 낼 확률 — 로그정규 D · 시드 독립 · `_boot_ratio_interval` 그대로."""
    import numpy as np
    rng = np.random.default_rng(seed)
    sb = sigma_ln if sigma_b is None else sigma_b
    rows = []
    for r in r_grid:
        hit = 0
        for _ in range(n_sim):
            a = np.exp(rng.normal(0.0, sigma_ln, n_a))
            b = np.exp(rng.normal(-math.log(r), sb, n_b))
            lo, hi = _boot_ratio_interval(a, b, n_boot, rng)
            hit += (lo > 1.0) or (hi < 1.0)
        rows.append([float(r), hit / n_sim])

    def first(p):
        return next((r for r, q in rows if r > 1.0 and q >= p), None)
    return {"sigma_ln_A": sigma_ln, "sigma_ln_B": sb, "n_a": n_a, "n_b": n_b, "n_sim": n_sim, "n_boot": n_boot,
            "seed": seed, "rows": rows, "false_detect_at_R1": next((q for r, q in rows if r == 1.0), None),
            "R50": first(0.5), "R80": first(0.8),
            "⚠": "로그정규·독립 시드 가정 · B 산포는 가정 · 격자 밖이면 None (격자 끝보다 크다)"}



# ── 대조 계 판독 모드 (카드 lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05 §4 · §5 · 회신 CR · 2026-10-14 · 결과 전) ──
CONTROL_CARD = REPO / "db" / "properties" / "lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05.json"
CONTROL_T = 600
#: 회신 CR Q-CR-6 — A 600 K (v2) 와 같은 시드–기계 대응 (결과 전 고정)
CONTROL_MACHINE = {1: "kgy", 2: "gabia", 3: "kgy", 4: "gabia", 5: "gabia"}
#: 회신 CR Q-CR-1 — 두 계 모두 120 원자 · A Li 48 · B (Li₃PS₄) Li 45
N_LI = {"A": 48, "B": 45}
#: 카드 §4 골격 게이트 (두 계 모두 · 600 K 에서도 · 회신 CR Q-CR-4) — ④ 문턱 5 = A 600 K 실측 최대 2 의 2.5 배
SKELETON_GATE = {"①_P_frac_frames_changed_max": 0.05, "②_S_moved_max": 0, "③_SS_new_pairs_max": 0,
                 "④_S_transient_max": 5}
N_B_MIN = 3                  # 카드 §4 — B 온도당 3/5
P90_LAG_PS, P90_MIN_DIST_A, P90_WIN_PS = 5.0, 2.0, 50.0     # v2 마감 §4 기록 형식 그대로 (CH 선례)


def skeleton_gate(r) -> dict:
    """카드 §4 골격 네 기준 — 생산 첫 프레임 대비 (`quench_ss_event.production_framework` 값).
    ④ = 일시 변화를 겪은 S 의 수 (`S.n_transient_only` — A 600 K 의 '최대 2' 를 잰 같은 필드).
    못 쟀으면 pass None = 판정 보류 (통과도 '골격 이동' 도 아니다)."""
    fw = (r or {}).get("framework") or {}
    if not fw or "status" in fw:
        return {"pass": None, "status": fw.get("status", "골격을 안 쟀다")}
    v = {"①_P_frac": (fw.get("P") or {}).get("frac_frames_any_P_changed_vs_first"), "②_S_moved": fw.get("S_moved"),
         "③_SS_new": fw.get("SS_new"), "④_S_transient": fw.get("S_transient")}
    if any(x is None for x in v.values()):
        return {"pass": None, "status": "골격 값이 비었다", "values": v}
    g = SKELETON_GATE
    crit = {"①": v["①_P_frac"] <= g["①_P_frac_frames_changed_max"], "②": v["②_S_moved"] <= g["②_S_moved_max"],
            "③": v["③_SS_new"] <= g["③_SS_new_pairs_max"], "④": v["④_S_transient"] <= g["④_S_transient_max"]}
    return {"pass": all(crit.values()), "criteria": crit, "values": v}


def prod_temperature(md_log, equilib_ps):
    """md.log (ASE MDLogger · `Time[ps] … T[K]`) — 생산 구간 (t ≥ equilib) 의 T 평균 · 표준편차 · 줄 수. 못 읽으면 None."""
    try:
        lines = pathlib.Path(md_log).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    hdr = lines[0].split() if lines else []
    if "Time[ps]" not in hdr or "T[K]" not in hdr:
        return None
    it, iT = hdr.index("Time[ps]"), hdr.index("T[K]")
    vals = []
    for ln in lines[1:]:
        q = ln.split()
        try:
            if float(q[it]) >= equilib_ps - 1e-9:
                vals.append(float(q[iT]))
        except (IndexError, ValueError):
            continue
    if len(vals) < 2:
        return None
    return {"mean_K": round(statistics.fmean(vals), 2), "sd_K": round(statistics.stdev(vals), 2), "n_rows": len(vals),
            "from_ps": equilib_ps}


def p90sq_windows(traj, save_fs, lag_ps=P90_LAG_PS, min_dist=P90_MIN_DIST_A, win_ps=P90_WIN_PS, prod_ps=None) -> dict:
    """5 ps lag p90² (v2 마감 §4 형식 · CH 선례) — 생산 궤적을 50 ps 창으로 나눠 창마다 `aimd_jump_stats.hop_census` 의
    `per_ion_max_A.p90` 를 제곱 · 그 런 자기 상자의 (d/2)² 대비 초과분 · 창을 고르지 않는다 (전부). 기록 전용 — 판정 아님.
    창 = [k·50, (k+1)·50] ps (양끝 포함 · `aimd_jump_stats.py --t_from_ps --t_to_ps` 와 같은 `slice_window`) ·
    창 수 = 선언된 prod_ps / 50 (aimd_results.json). ⛔ 프레임 수로 세지 않는다 — 드라이버는 equilib 뒤 첫 관측을
    한 간격 뒤에 찍어 400 ps 가 **4000 프레임 (0–399.9 ps)** 이라 `(n−1)·dt/50` 은 7 창이 된다 (v2 마감 기록은 8 창 ·
    2026-10-14 결과 전에 잡음). prod_ps 를 모를 때만 프레임 수로 세고 그 사실을 적는다."""
    import numpy as np
    import aimd_jump_stats as J
    sym, pos, cells = J.read_traj(str(traj))
    dt = float(save_fs) / 1000.0
    li = np.where(sym == "Li")[0]
    c0 = cells[0]
    off = float(np.abs(c0 - np.diag(np.diag(c0))).max())
    diag = np.diag(c0)
    cubic = off < 1e-6 and float(diag.max() - diag.min()) < 1e-6
    ref = (float(diag.min()) / 2.0) ** 2
    span = len(pos) * dt                     # 프레임 수 × 간격 = 생산 길이 (첫 프레임이 한 간격 뒤라서)
    if prod_ps:
        n_win = int(round(float(prod_ps) / win_ps))
        if span < float(prod_ps) - 2 * dt:
            return {"status": f"궤적이 선언된 prod 보다 짧다 (프레임 {len(pos)} × {dt} ps = {span:.1f} < {prod_ps} ps) — 못 냈다"}
    else:
        n_win = int(math.floor(span / win_ps + 1e-9))
    vals = []
    for k in range(n_win):
        p, c, _, _ = J.slice_window(pos, cells, dt, k * win_ps, (k + 1) * win_ps)
        hc = J.hop_census(J.unwrap(p[:, li, :], c[0]), dt, lag_ps, min_dist)
        vals.append(round(hc["per_ion_max_A"]["p90"] ** 2, 2))
    if not vals:
        return {"status": f"50 ps 창이 하나도 없다 (프레임 {len(pos)} · dt {dt} ps)"}
    return {"window_ps": win_ps, "lag_ps": lag_ps, "min_dist_A": min_dist, "n_windows": len(vals), "p90sq_A2": vals,
            "n_windows_from": "prod_ps" if prod_ps else "프레임 수 (prod_ps 모름)", "n_frames": int(len(pos)),
            "box_L_A": [round(float(x), 4) for x in diag],
            "half_box_sq_A2": round(ref, 2), "cell_cubic": cubic, "excess_A2": [round(x - ref, 2) for x in vals],
            "n_windows_over": sum(1 for x in vals if x > ref), "median_A2": round(statistics.median(vals), 2),
            "max_A2": max(vals), "⚠": "기록 전용 — 판정과 무관 · (d/2)² 는 상자 짧은 변 기준"}


def control_msd_path(root, sd, temp=CONTROL_T) -> pathlib.Path:
    return pathlib.Path(root) / f"seed{sd}" / f"T{temp}" / "d0.00_cfg0" / f"T{temp}" / "msd.json"


def collect_control(root, n_li, n_boot=400, framework=True, p90=True, temp=CONTROL_T):
    """ROOT/seed<S>/T<temp>/d0.00_cfg0/T<temp>/msd.json 다섯 → ({seed: rec}, 빠진 런). 런마다 카드 §5 기록 열
    (N_eff · 생산 T · p90²) 을 더한다 — 판정에는 안 쓴다. temp 기본 600 (대조 계) · B 650 K 카드는 650 (2026-10-19)."""
    import msd_diffusive_check as M
    root = pathlib.Path(root)
    runs, missing = {}, []
    mq = None
    if framework:
        import quench_ss_event as Q
        mq = Q._load_mq(str(HERE))
    for sd in SEEDS:
        jp = control_msd_path(root, sd, temp)
        if not jp.is_file():
            missing.append(str(jp))
            continue
        print(f"  … {root} seed{sd} ({CONTROL_MACHINE[sd]})", flush=True)
        r = read_run(jp, n_boot=n_boot, framework=framework, mq=mq)
        d = json.loads(jp.read_text(encoding="utf-8"))
        #: N_eff 는 `msd_diffusive_check.rsd_report` 한 곳에서 낸다 — 옛 기록 (msd_max_A2 없음) 은 msd_Li_A2 배열의
        #  max 로 되살리는 경로가 거기 있다 (같은 규칙을 여기 다시 쓰지 않는다)
        rr = M.rsd_report({"n_Li": n_li, "msd_max_A2": d.get("msd_max_A2"), "msd_Li_A2": d.get("msd_Li_A2")})
        r["N_eff_he2018"] = rr.get("n_eff_he2018")
        r["N_eff_inputs"] = {"n_Li": n_li, "site_distance_A": rr.get("site_distance_A"),
                             "msd_max_from": ("msd_max_A2" if d.get("msd_max_A2") is not None
                                              else ("msd_Li_A2 배열 max (옛 기록 꼴)" if d.get("msd_Li_A2") else "없음")),
                             "⚠": "He 2018 식 (8) · max(MSD) 는 궤적 전체 · 귀무모형 — 판정 아님"}
        eq = None
        try:
            eq = json.loads((jp.parents[2] / "run_meta.json").read_text(encoding="utf-8")).get("equilib_ps")
        except (OSError, ValueError):
            pass
        r["T_prod"] = prod_temperature(jp.parent / "md.log", float(eq) if eq is not None else 5.0)
        r["T_prod_equilib_assumed_5ps"] = eq is None
        if p90:
            try:
                pp = json.loads((jp.parent / "aimd_results.json").read_text(encoding="utf-8")).get("prod_ps")
            except (OSError, ValueError):
                pp = None
            try:
                r["p90sq_5ps_lag"] = p90sq_windows(jp.parent / "traj.xyz", r.get("save_fs") or 100.0, prod_ps=pp)
            except (Exception, SystemExit) as e:                       # 기록을 못 낸 것은 판정 보류가 아니라 '못 냈다'
                r["p90sq_5ps_lag"] = {"status": f"못 냈다 ({type(e).__name__}: {e})"}
        runs[sd] = r
    return runs, missing


V2_CLOSED = REPO / "db" / "properties" / "lpscl_smallcell_glass_md_v2_closed_2026_10_05.json"
V2_D_SPREAD_KEY = ("1_확정", "D_시드간_상대산포_보고량", "600K", "D_over_median_정렬")
V2_P90_KEY = ("4_기록_남길_것", "p90²_5ps_lag", "✅_측정_2026_10_05", "런별")


def spread_ctrl(vals) -> dict:
    """카드 §1 보고량 ③ — 시드 간 상대 산포 (`rel_spread` 그대로: IQR/중앙값 · max/min · D/중앙값) + ln D 의 표본 SD
    (척도 없는 양 · 카드 §4 결과 전 모의의 σ_ln 과 같은 정의 — A 600 K 다섯이면 0.0935). 기록이다 — 검출한계 모의의
    어느 행을 쓸지 고르지 않는다 (c1b 문장은 기준 행 + B 두 배 행을 늘 같이 적는다)."""
    v = [x for x in vals if x is not None and x > 0]
    out = rel_spread(v)
    if out is None:
        return {"n": len(v), "status": f"시드가 둘 미만 ({len(v)}) — 산포를 못 낸다"}
    out["sd_ln"] = round(statistics.stdev([math.log(x) for x in v]), 4)
    return out


def a_reproduces_v2(runs_a, path=V2_CLOSED, tol_d=1.5e-4, tol_p90=0.051) -> dict:
    """대조 잡 (결과 전 · 2026-10-14) — A 600 K 다섯을 지금 도구로 다시 읽어 v2 마감에 박힌 값과 맞춘다.
    ① D/중앙값 정렬 다섯 (v2 판독 fa729b30 의 600 K 상대 산포 · 넷째 자리) ② 창별 p90² (`aimd_jump_stats.py` CLI 로 잰
    10-05 측정 · 첫째 자리 → 허용 0.051). ①이 어긋나면 R 의 A 쪽을 믿을 수 없다 → 판정 보류 (호출부) ·
    ②가 어긋나면 B 의 p90² 를 같은 잣대로 읽지 않는다 (기록 열 · 갈래와 무관). 마감 파일을 못 읽으면 '못 봄' — 같다고 하지 않는다."""
    try:
        d = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        ref_d = d
        for k in V2_D_SPREAD_KEY:
            ref_d = ref_d[k]
        ref_p = d
        for k in V2_P90_KEY:
            ref_p = ref_p[k]
    except (OSError, ValueError, KeyError, TypeError) as e:
        return {"status": f"v2 마감을 못 읽었다 ({type(e).__name__}) — 대조 못 봄", "D_same": None, "p90_same": None}
    got = rel_spread([(runs_a.get(sd) or {}).get("_D_slope") for sd in SEEDS])
    got_d = (got or {}).get("D_over_median") or []
    d_diff = (max(abs(a - b) for a, b in zip(got_d, ref_d)) if len(got_d) == len(ref_d) and got_d else None)
    p90 = {}
    for sd in SEEDS:
        want = (ref_p.get(f"T{CONTROL_T}_seed{sd}") or {}).get("창_p90²_Å²")
        have = ((runs_a.get(sd) or {}).get("p90sq_5ps_lag") or {}).get("p90sq_A2")
        if not want or not have:
            p90[sd] = {"same": None, "status": "한쪽이 없다 — 못 봄"}
            continue
        mx = max(abs(a - b) for a, b in zip(have, want)) if len(have) == len(want) else None
        p90[sd] = {"n_windows_tool": len(have), "n_windows_v2": len(want),
                   "max_abs_diff_A2": round(mx, 3) if mx is not None else None,
                   "same": mx is not None and mx <= tol_p90}
    flags = [x["same"] for x in p90.values()]
    return {"D_over_median_tool": got_d, "D_over_median_v2": ref_d,
            "D_max_abs_diff": round(d_diff, 5) if d_diff is not None else None,
            "D_same": d_diff is not None and d_diff <= tol_d,
            "p90": p90, "p90_same": (None if any(f is None for f in flags) else all(flags)),
            "tol": {"D_over_median": tol_d, "p90sq_A2": tol_p90},
            "⚠": "대조 잡 — A 의 파일·판독 경로가 10-04/05 와 같은지 본다 (결과 전 박음 · 판정 규칙이 아니다)"}


def control_detect_limit_pre(path=CONTROL_CARD):
    """카드 §4 '검출한계_결과_전_모의' 를 그대로 싣는다 (c1b 문장에 붙이는 결과 전 숫자 · 회신 CR Q-CR-3)."""
    try:
        d = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        return d["4_판정_결과_보기_전에_정한다"]["검출한계_결과_전_모의"]
    except (OSError, ValueError, KeyError) as e:
        return {"status": f"카드에서 못 읽었다 ({type(e).__name__})"}


def _control_system(name, runs, errs):
    """계 하나 — 런별 행 · N (C1 ∧ 최종 C2) · R 집합 (N ∧ 골격 통과) · 상대 산포. 오류 · 결측 · 골격 못 잰 런은 errs 에 더한다.
    → (계 출력, R 집합 D, N 집합 D) — D 는 호출부가 비 · 산포로만 쓰고 버린다. `control_aggregate` 와 B 650 K ① 단계
    (`bmeas_stage_b`) 가 같이 쓴다 (2026-10-19 · control_aggregate 본문을 그대로 옮김 — 600 K 출력이 같은지 결과 전 대조)."""
    rows, D, DN = [], [], []
    for sd in SEEDS:
        r = runs.get(sd)
        if r is None:
            errs.append(f"{name} seed{sd}: 런 없음")
            rows.append({"seed": sd, "machine": CONTROL_MACHINE[sd], "status": "런 없음"})
            continue
        if r.get("error"):
            errs.append(f"{name} seed{sd}: {r['error']}")
        sk = skeleton_gate(r)
        if sk["pass"] is None:
            errs.append(f"{name} seed{sd}: 골격 판정 못 함 ({sk.get('status')})")
        ok = run_pass(r)
        c2 = r.get("C2") or {}
        b_sto, b_mto = r.get("beta_STO"), r.get("beta_MTO")
        fw = r.get("framework") or {}
        rows.append({"seed": sd, "machine": CONTROL_MACHINE[sd], "C1_pass": r.get("C1_pass"),
                     "C1_msd_at_50_mto_A2": r.get("C1_msd_at_50_mto_A2"), "beta_MTO": b_mto,
                     "C2_final": c2.get("final_verdict"), "n_sigma_end": c2.get("n_sigma_end_signed"),
                     "n_sigma_prev": c2.get("n_sigma_prev_signed"), "b_end": c2.get("b_end"), "b_prev": c2.get("b_prev"),
                     "counts_in_N": ok, "skeleton": sk, "in_R_set": bool(ok and sk["pass"]),
                     "record": {"beta_STO": b_sto,
                                "STO_minus_MTO": (b_sto - b_mto) if b_sto is not None and b_mto is not None else None,
                                "aux_50_200": r.get("aux_50_200"), "C2_common_b": r.get("C2_common_b"),
                                "N_eff_he2018": r.get("N_eff_he2018"), "T_prod": r.get("T_prod"),
                                "p90sq_5ps_lag": r.get("p90sq_5ps_lag"),
                                "skeleton_literal": fw.get("literal"),
                                "skeleton_literal_moved": fw.get("literal_framework_moved"),
                                "SS_at_first_frame": fw.get("SS_at_first_frame")}})
        if ok and sk["pass"]:
            D.append(r.get("_D_slope"))
        if ok:
            DN.append(r.get("_D_slope"))
    out = {"N": sum(1 for x in rows if x.get("counts_in_N")), "of": len(SEEDS),
           "D_relative_spread_R_set": spread_ctrl(D),
           "D_relative_spread_N_set_record": spread_ctrl(DN),
           "R_set_seeds": [x["seed"] for x in rows if x.get("in_R_set")],
           "skeleton_moved_seeds": [x["seed"] for x in rows if (x.get("skeleton") or {}).get("pass") is False],
           "rows": rows}
    return out, D, DN


def control_aggregate(runs_a, runs_b, detect_pre=None, n_boot_r=10000, v2_closed=V2_CLOSED) -> dict:
    """카드 §4 — 계별 N (C1 ∧ 최종 C2) · R 집합 (N ∧ 골격 통과) · 골격 이동 수 → 갈래.
    오류 · 결측 · 골격을 못 잰 런이 하나라도 있으면 갈래를 내지 않는다 (판정 보류). ⛔ D 절대값을 남기지 않는다 (R 은 비)."""
    sys_out, errs, D = {}, [], {}
    for name, runs in (("A", runs_a), ("B", runs_b)):
        sys_out[name], D[name], _ = _control_system(name, runs, errs)
    a_chk = (a_reproduces_v2(runs_a, v2_closed) if v2_closed is not None
             else {"status": "안 봄 (v2_closed=None · selftest 전용)", "D_same": None, "p90_same": None})
    if v2_closed is not None and a_chk.get("D_same") is not True:
        errs.append(f"A: v2 마감의 D 상대 산포를 재현하지 못했다 ({a_chk.get('status') or a_chk.get('D_max_abs_diff')}) — "
                    "A 쪽 R 을 믿을 수 없다 (파일 · 도구 확인)")
    R = None
    if errs:
        br = (f"판정 보류 — 오류 · 결측 · 골격 못 잰 런 · 대조 잡 실패 {len(errs)} 개 (통과도 미통과도 아니다 · "
              "런 유효성 위반은 판독 전 재실행 · 카드 §4)")
    else:
        nb = sys_out["B"]["N"]
        na_r, nb_r = len(sys_out["A"]["R_set_seeds"]), len(sys_out["B"]["R_set_seeds"])
        if nb <= N_B_MIN - 1:
            br = (f"c2 (N_B = {nb} ≤ {N_B_MIN - 1}) — R 을 내지 않는다 · '같은 게이트 · 같은 온도에서 B 가 통과하지 못했다' 를 "
                  "1차 관측으로 적는다 · 다음 = B 측정 가능 온도 (새 카드)")
        elif na_r >= MIN_SEEDS_FOR_R and nb_r >= MIN_SEEDS_FOR_R:
            R = ratio_boot(D["A"], D["B"], n_boot=n_boot_r)
            if "R" not in R:
                br = f"판정 보류 — R 을 못 냈다 ({R.get('status')})"
            elif R["excludes_1"]:
                br = (f"c1a (N_B = {nb} · R 집합 A {na_r} · B {nb_r} · 95 % 구간이 1 밖) — 방향 "
                      f"({'A 의 D 가 크다' if R['R'] > 1 else 'B 의 D 가 크다'}) + R")
            else:
                br = (f"c1b (N_B = {nb} · R 집합 A {na_r} · B {nb_r} · 95 % 구간이 1 을 포함) — 결과 전 검출한계와 함께 "
                      "'구분되지 않았다' ('같다' 가 아니다)")
        else:
            br = (f"c1c (N_B = {nb} ≥ {N_B_MIN} · R 집합 A {na_r} · B {nb_r} — 한쪽이 {MIN_SEEDS_FOR_R} 미만) — "
                  "R 을 내지 않는다 · N 과 골격 이동 수를 적는다")
    return {"T_K": CONTROL_T, "systems": sys_out, "branch": br, "R": R, "errors": errs,
            "A_reproduces_v2_closure": a_chk,
            "detect_limit_pre_results": detect_pre,
            "rules": {"N_B_min": N_B_MIN, "min_R_set": MIN_SEEDS_FOR_R, "skeleton_gate": SKELETON_GATE,
                      "C1_min_A2": C1_MIN_A2, "C2": "β_MTO 2–50 ps ∈ [0.8, 1.2] · 2σ · 끝 두 b (400 ps → b 256 · 192)",
                      "R": "median D_A / median D_B · R 집합만 · 계 안 시드 부트스트랩 95 % 백분위"},
            "⛔": "갈래는 카드 §4 의 기계적 적용이다 — 확정 · 해석은 외부 1저자 · D 절대값은 싣지 않는다 (R 은 비)"}


def _control_row_line(x) -> str:
    """런 한 줄 (control_show · bmeas_show 가 같이 쓴다 — 2026-10-19 control_show 에서 그대로 옮김)."""
    if x.get("status"):
        return f"   seed{x['seed']} {x['machine']:5s} ⛔ {x['status']}"
    sk, rec = x["skeleton"], x["record"]
    v = sk.get("values") or {}
    p9 = rec.get("p90sq_5ps_lag") or {}
    tp = rec.get("T_prod") or {}
    return (f"   seed{x['seed']} {x['machine']:5s} C1 {'통과' if x['C1_pass'] else '미달'} "
            f"({(x['C1_msd_at_50_mto_A2'] or float('nan')):.1f} Å²) · β_MTO {(x['beta_MTO'] or float('nan')):.4f} · "
            f"σ 거리 끝 b{x['b_end']} {x['n_sigma_end']} · 앞 b{x['b_prev']} {x['n_sigma_prev']} → **{x['C2_final']}** | "
            f"골격 {'통과' if sk['pass'] else ('이동' if sk['pass'] is False else '못 잼')} "
            f"(① {v.get('①_P_frac')} · ② {v.get('②_S_moved')} · ③ {v.get('③_SS_new')} · ④ {v.get('④_S_transient')}) | "
            f"N_eff {round(rec['N_eff_he2018']) if rec.get('N_eff_he2018') else '—'} · "
            f"T {tp.get('mean_K', '—')}±{tp.get('sd_K', '—')} K · "
            f"p90² 중앙 {p9.get('median_A2', '—')} · 최대 {p9.get('max_A2', '—')} · (d/2)² {p9.get('half_box_sq_A2', '—')} "
            f"· 초과 창 {p9.get('n_windows_over', '—')}/{p9.get('n_windows', '—')}")


def control_show(agg) -> list[str]:
    L = []
    for name in ("A", "B"):
        sy = agg["systems"][name]
        L.append(f"■ {name} {CONTROL_T} K — N = {sy['N']}/{sy['of']} (C1 ∧ 최종 C2) · R 집합 {sy['R_set_seeds']} · "
                 f"골격 이동 {sy['skeleton_moved_seeds']}")
        L.extend(_control_row_line(x) for x in sy["rows"])
    for name in ("A", "B"):
        sp = agg["systems"][name].get("D_relative_spread_R_set") or {}
        spn = agg["systems"][name].get("D_relative_spread_N_set_record") or {}
        L.append(f"   {name} 시드 간 상대 산포 (R 집합 · 보고량 ③) n {sp.get('n')} · IQR/중앙 {sp.get('IQR_over_median', '—')} · "
                 f"max/min {sp.get('max_over_min', '—')} · sd(ln D) {sp.get('sd_ln', '—')} · D/중앙 {sp.get('D_over_median', '—')}"
                 f" | N 집합 (기록) n {spn.get('n')} · IQR/중앙 {spn.get('IQR_over_median', '—')} · max/min {spn.get('max_over_min', '—')}")
    ac = agg.get("A_reproduces_v2_closure") or {}
    if ac.get("status"):
        L.append(f"   대조 잡 (A ↔ v2 마감): ⛔ {ac['status']}")
    else:
        bad = [sd for sd, x in (ac.get("p90") or {}).items() if x.get("same") is not True]
        L.append(f"   대조 잡 (A ↔ v2 마감): D/중앙 {'같음' if ac.get('D_same') else '⛔ 다름'} (최대 차 {ac.get('D_max_abs_diff')}) · "
                 f"p90² {'5/5 같음' if ac.get('p90_same') else '⛔ 다르거나 못 봄 ' + str(bad) + ' — B p90² 를 같은 잣대로 읽지 않는다'}")
    L.append(f"→ 갈래 (규칙 적용): {agg['branch']}")
    if agg.get("R") and "R" in agg["R"]:
        r = agg["R"]
        L.append(f"   R = {r['R']:.3f} · 95 % [{r['lo']:.3f}, {r['hi']:.3f}] · R 집합 A {r['n_a']} · B {r['n_b']} · 부트 {r['n_boot']}")
    if agg.get("errors"):
        L.extend("   ⛔ " + e for e in agg["errors"])
    return L


# ── B 측정 가능 조건 카드 ① 단계 — B 650 K 만 (카드 lpscl_smallcell_glass_control_bmeasurable_estimand_2026_10_14
#    §1b · §4 · 개정 CX 2026-10-19 · 결과 전 커밋) ──
BMEAS_CARD = REPO / "db" / "properties" / "lpscl_smallcell_glass_control_bmeasurable_estimand_2026_10_14.json"
BMEAS_AMEND = REPO / "db" / "properties" / "lpscl_smallcell_glass_control_bmeasurable_amendment_cx_2026_10_19.json"
BMEAS_T = 650                # 카드 §1b — 한 점 · 결과를 보고 온도를 더 고르지 않는다 (CLI 로 못 바꾼다)
#: 10-14 대조 계 판독 기록 (A · B 600 K · 도구 sha16 097c8a8092e011e7 · n_boot 400) — B 600 K 네 지표 · N 을 나란히 싣고,
#  A 600 K 를 지금 도구로 다시 읽은 행이 이 기록과 같은지 본다 (대조 잡 ② · 도구를 바꿨으니)
READOUT_600 = (REPO / "db" / "raw" / "lpscl_glass_control_li3ps4_2026_10_05" / "readout_control_2026_10_14"
               / "readout_control.json")
SKEL_KEYS = {"①_P_frac": "①_P_frac_frames_changed_max", "②_S_moved": "②_S_moved_max", "③_SS_new": "③_SS_new_pairs_max",
             "④_S_transient": "④_S_transient_max"}
#: 대조 계 카드 §4 결과 전 모의의 기준 행 σ_ln (A 600 K 다섯 · 표본 SD) — ② 단계 검출한계의 A 쪽 가정
SIGMA_LN_A600 = 0.0935
ROW_SAME_EXACT = ("C1_pass", "C2_final", "n_sigma_end", "n_sigma_prev", "b_end", "b_prev", "counts_in_N", "in_R_set")
ROW_SAME_FLOAT = ("C1_msd_at_50_mto_A2", "beta_MTO")


def skeleton_distribution(rows) -> dict:
    """골격 네 지표 — **모든 런** (통과 포함) 의 런별 값 · 범위 · 중앙 · 문턱 초과 수 (개정 CX §4 · 650 K 의 첫 눈금).
    기록 전용 — 게이트는 `skeleton_gate` 다. 못 잰 런은 값이 None 이고 n 에 안 든다 (0 으로 그리지 않는다)."""
    good = [x for x in rows if not x.get("status")]
    out = {}
    for k, gk in SKEL_KEYS.items():
        per = {x["seed"]: ((x.get("skeleton") or {}).get("values") or {}).get(k) for x in good}
        v = [y for y in per.values() if y is not None]
        thr = SKELETON_GATE[gk]
        out[k] = {"per_seed": per, "n": len(v), "min": min(v) if v else None,
                  "median": statistics.median(v) if v else None, "max": max(v) if v else None,
                  "gate": thr, "n_over_gate": sum(1 for y in v if y > thr)}
    out["seeds_counting_in_N"] = [x["seed"] for x in good if x.get("counts_in_N")]
    return out


def p90_saturation(rows) -> dict:
    """5 ps lag p90² 창 초과 — 런별 초과 창 / 창 수 · 포화 (전 창 초과) 런 수 (개정 CX §4 · 기록 전용 · 650 K 는 포화를
    예상한다 → R(650) 에 붙는 유한크기 단서가 600 K 보다 강하다). ⛔ 게이트가 아니다."""
    per = {}
    for x in rows:
        p9 = (x.get("record") or {}).get("p90sq_5ps_lag") or {}
        if x.get("status") or not p9.get("n_windows"):
            per[x["seed"]] = {"status": x.get("status") or p9.get("status") or "p90² 기록이 없다"}
            continue
        per[x["seed"]] = {"over": p9.get("n_windows_over"), "of": p9["n_windows"],
                          "saturated": p9.get("n_windows_over") == p9["n_windows"], "median_A2": p9.get("median_A2"),
                          "max_A2": p9.get("max_A2"), "half_box_sq_A2": p9.get("half_box_sq_A2")}
    ok = [y for y in per.values() if "of" in y]
    return {"per_seed": per, "n_runs": len(ok), "n_saturated": sum(1 for y in ok if y["saturated"]),
            "⚠": "기록 전용 — 포화를 게이트로 쓰지 않는다 · 편입은 C1 · C2 로만 (회신 CH) · 포화면 R(650) 의 유한크기 단서가 강해진다"}


def readout600(path=READOUT_600) -> dict:
    """10-14 대조 계 판독 기록 → A · B 행 · N · n_boot · 도구 sha16. 못 읽으면 status (지어내지 않는다)."""
    try:
        d = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        sy = d["aggregate"]["systems"]
        return {"A": sy["A"]["rows"], "B": sy["B"]["rows"], "N": {"A": sy["A"]["N"], "B": sy["B"]["N"]},
                "n_boot": d.get("n_boot"), "tool_sha16": (d.get("tool_sha16") or {}).get("glass_v2_readout.py")}
    except (OSError, ValueError, KeyError, TypeError) as e:
        return {"status": f"10-14 판독 기록을 못 읽었다 ({type(e).__name__})"}


def a600_reproduces_readout(rows_now, n_boot, rec) -> dict:
    """대조 잡 ② (2026-10-19 · 도구를 바꿨으니 — 회신 CX Q-CX-2 ③ 상시 절차) — A 600 K 를 지금 도구로 다시 읽은 행이
    10-14 판독 기록의 행과 같은가: C1 · C1 값 · β_MTO (1e-9) · 최종 C2 · σ 거리 둘 · 끝 두 b · N · R 집합 · 골격 네 값
    (그대로) · p90² 창 (0.01). 다르면 B 650 K 를 600 K 와 같은 잣대로 읽는다고 할 수 없다 → 판정 보류 (호출부).
    기록을 못 읽거나 n_boot 가 기록과 다르면 '못 봄' (같다고 하지 않는다)."""
    if rec.get("status"):
        return {"same": None, "status": rec["status"]}
    if rec.get("n_boot") != n_boot:
        return {"same": None, "status": f"n_boot 가 기록 ({rec.get('n_boot')}) 과 다르다 ({n_boot}) — σ 가 달라 못 봄"}
    old = {x.get("seed"): x for x in rec["A"]}
    diffs = []
    for x in rows_now:
        sd = x["seed"]
        y = old.get(sd)
        if y is None or x.get("status") or y.get("status"):
            diffs.append(f"seed{sd}: 한쪽 행이 없다 ({x.get('status') or (y or {}).get('status') or '기록에 없음'})")
            continue
        for k in ROW_SAME_EXACT:
            if x.get(k) != y.get(k):
                diffs.append(f"seed{sd} {k}: 기록 {y.get(k)} · 지금 {x.get(k)}")
        for k in ROW_SAME_FLOAT:
            u, w = x.get(k), y.get(k)
            if u is None or w is None or abs(u - w) > 1e-9:
                diffs.append(f"seed{sd} {k}: 기록 {w} · 지금 {u}")
        va, vb = (x.get("skeleton") or {}).get("values"), (y.get("skeleton") or {}).get("values")
        if va != vb:
            diffs.append(f"seed{sd} 골격 네 값: 기록 {vb} · 지금 {va}")
        pa = ((x.get("record") or {}).get("p90sq_5ps_lag") or {}).get("p90sq_A2")
        pb = ((y.get("record") or {}).get("p90sq_5ps_lag") or {}).get("p90sq_A2")
        if not pa or not pb or len(pa) != len(pb) or max(abs(u - w) for u, w in zip(pa, pb)) > 0.01 + 1e-9:
            diffs.append(f"seed{sd} p90² 창: 기록 {pb} · 지금 {pa}")
    if len(rows_now) != len(old):
        diffs.append(f"행 수: 기록 {len(old)} · 지금 {len(rows_now)}")
    return {"same": not diffs, "diffs": diffs, "n_boot": n_boot, "record_tool_sha16": rec.get("tool_sha16"),
            "⚠": "대조 잡 — 판정 규칙이 아니다 · 도구 무결성 확인 (결과 전 박음)"}


def bmeas_stage_b(runs_a600, runs_b, n_boot=400, v2_closed=V2_CLOSED, ref600=READOUT_600, detect_n_sim=2000) -> dict:
    """B 측정 가능 조건 카드 ① 단계 — B 650 K 다섯만 판독 (A 650 K 없음 · R 없음).
    · B: 런별 C1 · 최종 C2 · 골격 네 기준 (대조 계 카드 §4 와 같은 함수 · 같은 숫자 — `_control_system`) → N_B · R 집합 ·
      골격 이동. 최종 C2 가 빈 런 (오류 없이) 도 판정 보류다 — 미통과로 조용히 세지 않는다.
    · 대조 잡 (상시 · 개정 CX §7): ① A 600 K ↔ v2 마감 (`a_reproduces_v2`) ② A 600 K ↔ 10-14 판독 기록 (도구를 바꿨으니) —
      어느 쪽이든 다르거나 못 봤으면 판정 보류.
    · 기록 (개정 CX §4): 골격 네 지표 분포 — B 650 K (모든 런) · A 600 K (지금 다시 읽음) · B 600 K (10-14 기록) ·
      p90² 창 초과 · 포화 런 수 (세 묶음).
    · 갈래 (카드 §4 · 개정 CX §3): b1 (N_B ≤ 2 → A 650 K 를 돌리지 않고 닫는다) · b2 (N_B ≥ 3 → ② 단계 A 650 K · 새 GPU
      공존 결정). b2 인데 B R 집합 < 4 면 ② 를 돌려도 R 이 없다 (b2c 로 정해짐) — 그 사실만 적고 A 실행은 외부 1저자
      확인으로 남긴다. b2 · B R 집합 ≥ 4 면 ② 단계 검출한계를 A 650 K 결과 전에 낸다 (카드 §4 회신 CS 덧붙임 — B 650 K
      실측 σ_ln · A 는 600 K 기준 0.0935 가정 · 대조 계 카드의 기준 행 · B 두 배 행과 병기).
    · 허용 문장 (카드 §1a · 개정 CX §8 — 단서를 문장 안에: N_B · 경계 · 미통과 · C1 · 골격 이동이 있으면 그 수).
    ⛔ R 을 내지 않는다 (A 650 K 가 없다 · 600 K 런은 650 K R 에 섞지 않는다 — 카드 §4) · D 절대값을 남기지 않는다 ·
       갈래를 확정하지 않는다 (외부 1저자)."""
    errs = []
    sys_a, _, _ = _control_system("A", runs_a600, errs)
    sys_b, d_r, _ = _control_system("B", runs_b, errs)
    for sd in SEEDS:
        r = runs_b.get(sd)
        if r is not None and not r.get("error") and (r.get("C2") or {}).get("final_verdict") is None:
            errs.append(f"B seed{sd}: 최종 C2 가 비었다 — 판정 못 함 (미통과로 세지 않는다)")
    a_chk = (a_reproduces_v2(runs_a600, v2_closed) if v2_closed is not None
             else {"status": "안 봄 (v2_closed=None · selftest 전용)", "D_same": None, "p90_same": None})
    if v2_closed is not None and a_chk.get("D_same") is not True:
        errs.append(f"대조 잡 ① A 600 K 가 v2 마감의 D 상대 산포를 재현하지 못했다 "
                    f"({a_chk.get('status') or a_chk.get('D_max_abs_diff')}) — 판독 경로를 믿을 수 없다")
    rec = readout600(ref600) if ref600 is not None else {"status": "안 봄 (ref600=None · selftest 전용)"}
    r_chk = a600_reproduces_readout(sys_a["rows"], n_boot, rec)
    if ref600 is not None and r_chk.get("same") is not True:
        errs.append(f"대조 잡 ② A 600 K 가 10-14 판독 기록을 재현하지 못했다 "
                    f"({r_chk.get('status') or ' ; '.join(r_chk.get('diffs', [])[:3])}) — 바뀐 도구를 믿을 수 없다")
    rows_b = sys_b["rows"]
    present = [x for x in rows_b if not x.get("status")]
    fin = [str(x.get("C2_final") or "") for x in present]
    tally = {"통과": sum(1 for f in fin if f == "통과"), "경계": sum(1 for f in fin if f.startswith("경계")),
             "미통과": sum(1 for f in fin if f == "미통과")}
    c1 = sum(1 for x in present if x.get("C1_pass"))
    nb, nbr, moved = sys_b["N"], len(sys_b["R_set_seeds"]), sys_b["skeleton_moved_seeds"]
    n600 = (rec.get("N") or {}).get("B")
    cav = f"N_B = {nb}/{len(SEEDS)} · 경계 {tally['경계']} · 미통과 {tally['미통과']} · C1 {c1}/{len(SEEDS)}"
    if moved:
        cav += f" · 골격 이동 {len(moved)}"
    sent, nxt, dl = None, None, None
    if errs:
        br = (f"판정 보류 — 오류 · 결측 · 골격 못 잰 런 · 빈 C2 · 대조 잡 실패 {len(errs)} 개 (통과도 미통과도 아니다 · "
              "런 유효성 위반은 판독 전 재실행 · 카드 §4 · §7)")
    elif nb <= N_B_MIN - 1:
        br = f"b1 (N_B = {nb}/{len(SEEDS)} ≤ {N_B_MIN - 1}) — A 650 K 를 돌리지 않고 닫는다 (카드 §1b · 개정 CX §3) · R 없음"
        sent = (f"「A 와 같은 게이트로 a-Li₃PS₄ 유리는 650 K 에서도 과반이 통과하지 못했다 ({cav}) — 이 120 원자 셀 · "
                "프로토콜에서 B 의 측정 가능 온도는 650 K 보다 위다. A 650 K 는 돌리지 않았고 두 유리의 D 는 비교하지 않는다.」")
        nxt = ("닫는다 — A 650 K 안 돌림 · 카드 마감 (lpscl_smallcell_glass_control_bmeasurable_closed_<날짜>.json) → "
               "트랙 마감 (lpscl_smallcell_glass_track_closed_<날짜>.json) → 결과 편지 (외부 1저자 · 갈래 확정)")
    else:
        br = (f"b2 (N_B = {nb}/{len(SEEDS)} ≥ {N_B_MIN}) — ② 단계 A 650 K × 5 (카드 §1b · 새 GPU 공존 결정 · 예외 (7) 은 소멸) · "
              f"B R 집합 {nbr}")
        sent = (f"「같은 게이트로 a-Li₃PS₄ 유리는 650 K 에서 측정 가능했다 ({cav} · 600 K 는 "
                f"{n600 if n600 is not None else '기록 못 읽음'}/{len(SEEDS)}) — 이 셀 · 프로토콜에서 B 의 측정 가능 온도는 "
                "600 K 와 650 K 사이다.」")
        if nbr < MIN_SEEDS_FOR_R:
            br += f" · ⚠ B R 집합 {nbr} < {MIN_SEEDS_FOR_R} — ② 를 돌려도 R 은 없다 (b2c 로 정해짐)"
            nxt = (f"B R 집합 {nbr} < {MIN_SEEDS_FOR_R} 라 ② 단계의 목적 (R) 이 이미 불가 — 카드 문자 규칙은 'N_B ≥ 3 → A 650 K' 다 · "
                   "A 650 K 실행 여부는 결과 편지로 외부 1저자 확인 (새 GPU 공존 결정도 필요)")
        else:
            nxt = ("② A 650 K × 5 — 새 GPU 공존 결정 (사용자) · 시드–기계 대응 같음 · --seed 2000 + 시드 · "
                   "② 단계 판독 경로 (A · B 650 K · R · b2a/b2b/b2c) 는 A 결과 전에 도구에 넣는다")
            sp = spread_ctrl(d_r)
            if sp.get("sd_ln") is None:
                dl = {"status": f"B 650 K σ_ln 을 못 냈다 ({sp.get('status')})"}
            else:
                pre = control_detect_limit_pre()
                card_rows = {k: {kk: (pre.get("결과", {}).get(k) or {}).get(kk) for kk in ("σ_ln_A", "σ_ln_B", "R50", "R80")}
                             for k in ("σ_표본SD_0.094", "B_산포_2배")} if isinstance(pre, dict) else None
                dl = {**ratio_detect_limit(SIGMA_LN_A600, n_a=len(SEEDS), n_b=len(d_r), sigma_b=sp["sd_ln"], n_sim=detect_n_sim),
                      "card_rows_pre": card_rows,
                      "⚠": ("② 단계 결과 전 (A 650 K 전) — B = 650 K 실측 σ_ln (R 집합) · A = 600 K 기준 0.0935 가정 · n_A 5 가정 · "
                            "카드 §4 (회신 CS 덧붙임) · 대조 계 카드의 기준 행 · B 두 배 행과 병기 (어느 행을 쓸지 고르지 않는다)")}
    rec_b = rec.get("B") or []
    return {"stage": f"① B {BMEAS_T} K 만 (카드 §1b · 개정 CX §3 — A {BMEAS_T} K 없음 · R 없음)", "T_K_B": BMEAS_T,
            "B": {"N": nb, "of": len(SEEDS), "C2_tally": tally, "C1_pass": c1, "R_set_seeds": sys_b["R_set_seeds"],
                  "skeleton_moved_seeds": moved, "D_relative_spread_R_set": sys_b["D_relative_spread_R_set"],
                  "D_relative_spread_N_set_record": sys_b["D_relative_spread_N_set_record"], "rows": rows_b},
            "A600_now": {"N": sys_a["N"], "R_set_seeds": sys_a["R_set_seeds"], "rows": sys_a["rows"],
                         "⚠": "대조 잡 전용 — 650 K R · 판정에 쓰지 않는다 (카드 §4)"},
            "skeleton_distribution": {"B650": skeleton_distribution(rows_b), "A600_now": skeleton_distribution(sys_a["rows"]),
                                      "B600_record_1014": (skeleton_distribution(rec_b) if rec_b
                                                           else {"status": rec.get("status", "기록 없음")})},
            "p90_saturation": {"B650": p90_saturation(rows_b), "A600_now": p90_saturation(sys_a["rows"]),
                               "B600_record_1014": p90_saturation(rec_b) if rec_b else {"status": rec.get("status", "기록 없음")},
                               "A600_p90_matches_v2": a_chk.get("p90_same")},
            "control_jobs": {"①_A600_vs_v2_closure": a_chk, "②_A600_vs_readout_1014": r_chk},
            "branch": br, "sentence": sent,
            "sentence_⛔": ("문장 안의 괄호 (단서) 를 떼고 인용하지 않는다 (회신 CX) · 600 K c2 문장을 바꾸지 않는다 · 'LiCl 이 Li 수송을 "
                            "빠르게/느리게 한다' 를 650 K · 이 셀 밖으로 넓히지 않는다 · 기구 · Tg 탓을 말하지 않는다 · 'B 에서 확산하지 "
                            "않는다' 로 쓰지 않는다 (C1 은 따로 본다) · b2 를 'B 의 측정 가능 온도 = 650 K' 로 쓰지 않는다 (카드 §1a)"),
            "next": nxt, "detect_limit_stage2_pre": dl, "errors": errs,
            "N_eff_⛔": "두 계 N_eff 의 비는 사실상 MSD 의 비다 (N_eff ∝ n_Li × max MSD · Li 48 대 45) — D 의 비처럼 읽지 않는다 (회신 CX)",
            "rules": {"N_B_min": N_B_MIN, "C1_min_A2": C1_MIN_A2,
                      "C2": "β_MTO 2–50 ps ∈ [0.8, 1.2] · 2σ · 끝 두 b (400 ps → b 256 · 192)",
                      "skeleton_gate": SKELETON_GATE,
                      "skeleton_gate_scale": "① 5 % · ④ 5 는 A 600 K 눈금 — 650 K 눈금은 없다 (마감에 적는다 · 개정 CX §4)",
                      "Tg_distance": "R(650) 을 낼 때만 그 문장에 싣는다 — ① 단계에는 R 이 없다 (개정 CX §2)",
                      "sequential": "b1 → A 650 K 안 돌림 · b2 → A 650 K (새 GPU 결정) (카드 §1b · 개정 CX §3)",
                      "card": str(BMEAS_CARD.relative_to(REPO)), "amendment": str(BMEAS_AMEND.relative_to(REPO))},
            "⛔": "갈래는 카드 §4 의 기계적 적용이다 — 확정 · 해석은 외부 1저자 · R · D 절대값은 싣지 않는다"}


def _fmt_dist(dd) -> str:
    if not dd or dd.get("n") in (None, 0):
        return "—"
    per = " ".join(f"s{k}:{v}" for k, v in dd["per_seed"].items())
    return f"[{per}] 범위 {dd['min']}–{dd['max']} · 중앙 {dd['median']} · 문턱 초과 {dd['n_over_gate']}"


def bmeas_show(o) -> list[str]:
    b, t = o["B"], o["B"]["C2_tally"]
    L = [f"■ B {BMEAS_T} K — N_B = {b['N']}/{b['of']} (C1 ∧ 최종 C2) · C2 통과 {t['통과']} · 경계 {t['경계']} · 미통과 {t['미통과']} · "
         f"C1 {b['C1_pass']}/{b['of']} · R 집합 {b['R_set_seeds']} · 골격 이동 {b['skeleton_moved_seeds']}"]
    L.extend(_control_row_line(x) for x in b["rows"])
    L.append(f"   ⛔ {o['N_eff_⛔']}")
    sp = b.get("D_relative_spread_R_set") or {}
    L.append(f"   B 시드 간 상대 산포 (R 집합 · 기록) n {sp.get('n')} · IQR/중앙 {sp.get('IQR_over_median', '—')} · "
             f"max/min {sp.get('max_over_min', '—')} · sd(ln D) {sp.get('sd_ln', '—')}")
    L.append(f"■ 골격 네 지표 분포 — 모든 런 (통과 포함 · 개정 CX §4) · B {BMEAS_T} K | A {CONTROL_T} K (지금 다시 읽음) | "
             f"B {CONTROL_T} K (10-14 기록)")
    sd_ = o["skeleton_distribution"]
    for k in SKEL_KEYS:
        L.append(f"   {k} (문턱 {SKELETON_GATE[SKEL_KEYS[k]]}): B{BMEAS_T} {_fmt_dist(sd_['B650'].get(k))} | "
                 f"A{CONTROL_T} {_fmt_dist(sd_['A600_now'].get(k))} | B{CONTROL_T} {_fmt_dist((sd_['B600_record_1014'] or {}).get(k))}")
    ps = o["p90_saturation"]

    def p9(x):
        if "per_seed" not in x:
            return f"— ({x.get('status')})"
        per = " ".join(f"s{k}:{v['over']}/{v['of']}" if "of" in v else f"s{k}:—" for k, v in x["per_seed"].items())
        return f"[{per}] 포화 {x['n_saturated']}/{x['n_runs']}"
    L.append(f"■ p90² 창 초과 (기록 · 게이트 아님 · {BMEAS_T} K 는 포화 예상): B{BMEAS_T} {p9(ps['B650'])} | "
             f"A{CONTROL_T} {p9(ps['A600_now'])} | B{CONTROL_T} {p9(ps['B600_record_1014'])}")
    c1, c2 = o["control_jobs"]["①_A600_vs_v2_closure"], o["control_jobs"]["②_A600_vs_readout_1014"]
    if c1.get("status"):
        L.append(f"   대조 잡 ① A {CONTROL_T} K ↔ v2 마감: ⛔ {c1['status']}")
    else:
        L.append(f"   대조 잡 ① A {CONTROL_T} K ↔ v2 마감: D/중앙 {'같음' if c1.get('D_same') else '⛔ 다름'} "
                 f"(최대 차 {c1.get('D_max_abs_diff')}) · p90² {'5/5 같음' if c1.get('p90_same') else '⛔ 다르거나 못 봄'}")
    if c2.get("status"):
        L.append(f"   대조 잡 ② A {CONTROL_T} K ↔ 10-14 판독 기록: ⛔ 못 봄 — {c2['status']}")
    else:
        L.append(f"   대조 잡 ② A {CONTROL_T} K ↔ 10-14 판독 기록 (n_boot {c2.get('n_boot')}): "
                 + ("같음 (C1 · β · C2 · σ 거리 · 골격 네 값 · p90² 창)" if c2.get("same") else
                    "⛔ 다름 — " + " ; ".join(c2.get("diffs", [])[:4])))
    L.append(f"→ 갈래 (규칙 적용 · 확정은 외부 1저자): {o['branch']}")
    if o.get("sentence"):
        L.append(f"   문장 (단서 안): {o['sentence']}")
    if o.get("next"):
        L.append(f"   다음: {o['next']}")
    dl = o.get("detect_limit_stage2_pre")
    if dl:
        if dl.get("status"):
            L.append(f"   ② 단계 결과 전 검출한계: ⛔ {dl['status']}")
        else:
            L.append(f"   ② 단계 결과 전 검출한계 (B 실측 σ_ln {dl['sigma_ln_B']} · A {dl['sigma_ln_A']} 가정 · n {dl['n_a']}/{dl['n_b']}): "
                     f"R₅₀ {dl['R50']} · R₈₀ {dl['R80']} · R=1 오검출 {dl['false_detect_at_R1']} | 카드 행 {dl.get('card_rows_pre')}")
    L.extend("   ⛔ " + e for e in o.get("errors", []))
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

    # ── 대조 계 R · 검출한계 (회신 CR) ──
    same = ratio_boot([1.0, 1.1, 0.9, 1.05, 0.95], [1.0, 1.1, 0.9, 1.05, 0.95], n_boot=2000)
    ck("R: 같은 표본이면 R = 1 · 구간이 1 을 포함한다", abs(same.get("R", 0) - 1.0) < 1e-12 and not same["excludes_1"])
    twice = ratio_boot([2.0, 2.2, 1.8, 2.1, 1.9], [1.0, 1.1, 0.9, 1.05, 0.95], n_boot=2000)
    ck("R: A 가 두 배면 R = 2 · 구간이 1 밖", abs(twice.get("R", 0) - 2.0) < 1e-12 and twice["lo"] > 1.0)
    ck("R: 같은 입력·같은 난수면 같은 구간 (재현)", ratio_boot([2.0, 2.2, 1.8, 2.1, 1.9], [1.0, 1.1, 0.9, 1.05, 0.95],
                                                     n_boot=2000) == twice)
    ck("⛔음성 R: B 통과 시드 3 이면 R 을 내지 않는다 (둘 다 ≥ 4 · 회신 CR)",
       "R" not in ratio_boot([1.0, 1.1, 0.9, 1.05, 0.95], [1.0, 1.1, 0.9]))
    ck("⛔음성 R: A 쪽이 3 이어도 내지 않는다", "R" not in ratio_boot([1.0, 1.1, None, 0.9, None], [1.0, 1.1, 0.9, 1.0]))
    ck("⛔음성 R: D ≤ 0 이 있으면 내지 않는다", "R" not in ratio_boot([1.0, 1.1, 0.0, 0.9, 1.2], [1.0, 1.1, 0.9, 1.0]))
    ck("R: 결과에 D 가 없다 (비·구간·시드 수만)", set(twice) <= {"R", "lo", "hi", "excludes_1", "n_a", "n_b", "n_boot", "seed"})
    dl = ratio_detect_limit(0.10, r_grid=(1.0, 1.2, 3.0), n_sim=300, n_boot=400, seed=11)
    p = {r: q for r, q in dl["rows"]}
    ck("검출한계: 참 비 3 이면 거의 늘 검출 (σ_ln 0.10 · n 5/5)", p[3.0] >= 0.95)
    ck("검출한계: 비가 클수록 검출 확률이 크다 (1 ≤ 1.2 ≤ 3)", p[1.0] <= p[1.2] <= p[3.0])
    ck("⛔음성 검출한계: R = 1 의 오검출률이 0.3 을 넘지 않는다 (넘으면 구간 절차가 깨진 것)", p[1.0] <= 0.30)
    big = ratio_detect_limit(0.40, r_grid=(1.0, 1.1, 1.2), n_sim=200, n_boot=300, seed=12)
    ck("⛔음성 검출한계: 산포가 크고 격자가 짧으면 R₈₀ 이 없다 (None — 지어내지 않는다)", big["R80"] is None)

    # ── 대조 판독 모드 (카드 §4 · 2026-10-14 · 결과 전) ──
    def cfake(final="통과", c1=True, D=1.0, P=0.0, Sm=0, SS=0, St=0, err=None):
        r = fake(final, c1=c1, D=D)
        r["framework"] = {"P": {"frac_frames_any_P_changed_vs_first": P}, "S_moved": Sm, "SS_new": SS, "S_transient": St,
                          "framework_moved": False, "literal_framework_moved": False}
        if err:
            r["error"] = err
        return r
    ck("골격 ④: 일시 변화 5 는 통과 · 6 은 이동 (회신 CR Q-CR-4 · 문턱 5)",
       skeleton_gate(cfake(St=5))["pass"] is True and skeleton_gate(cfake(St=6))["pass"] is False)
    ck("골격 ①: 5 % 는 통과 · 5.1 % 는 이동", skeleton_gate(cfake(P=0.05))["pass"] is True
       and skeleton_gate(cfake(P=0.051))["pass"] is False)
    ck("골격 ② ③: 하나라도 있으면 이동", skeleton_gate(cfake(Sm=1))["pass"] is False and skeleton_gate(cfake(SS=1))["pass"] is False)
    ck("⛔음성 골격을 못 쟀으면 pass None (이동도 통과도 아니다)",
       skeleton_gate({"framework": {"status": "못 쟀다"}})["pass"] is None and skeleton_gate({})["pass"] is None)
    A5 = {sd: cfake(D=1.0 + 0.0213 * sd) for sd in SEEDS}
    Bh = {sd: cfake(D=0.5123457 + 0.0111111 * sd) for sd in SEEDS}
    ag = control_aggregate(A5, {sd: cfake(final="통과" if sd <= 2 else "미통과", D=0.5) for sd in SEEDS}, v2_closed=None)
    ck("c2: N_B 2 → R 을 내지 않는다", ag["branch"].startswith("c2") and ag["R"] is None and ag["systems"]["B"]["N"] == 2)
    ag = control_aggregate(A5, Bh, v2_closed=None)
    ck("c1a: A 가 B 의 두 배 남짓 → 구간이 1 밖 · 방향 'A 의 D 가 크다'",
       ag["branch"].startswith("c1a") and "A 의 D 가 크다" in ag["branch"] and 1.8 < ag["R"]["R"] < 2.3)
    ck("기계 대응: seed1 · 3 kgy · 2 · 4 · 5 gabia (회신 CR Q-CR-6)",
       [x["machine"] for x in ag["systems"]["B"]["rows"]] == ["kgy", "gabia", "kgy", "gabia", "gabia"])
    _js = json.dumps(ag, ensure_ascii=False, default=str)
    ck("⛔ 대조 산출물에 D 가 없다 (_D_slope · 심은 D 값이 안 보인다)",
       "_D_slope" not in _js and not any(repr(0.5123457 + 0.0111111 * sd) in _js for sd in SEEDS)
       and not any(repr(1.0 + 0.0213 * sd) in _js for sd in SEEDS))
    Bs = {sd: cfake(D=1.0 + 0.0213 * ((sd * 3) % 5 + 1)) for sd in SEEDS}
    ag = control_aggregate(A5, Bs, v2_closed=None)
    ck("c1b: 같은 분포 → R = 1 · 구간이 1 을 포함", ag["branch"].startswith("c1b") and abs(ag["R"]["R"] - 1.0) < 1e-12)
    Bk = dict(Bh); Bk[1] = cfake(D=0.5, St=6); Bk[2] = cfake(D=0.5, SS=1)
    ag = control_aggregate(A5, Bk, v2_closed=None)
    ck("c1c: B 골격 이동 둘 → R 집합 3 < 4 · N_B 는 C1 · C2 그대로 5 · 이동 시드 [1, 2]",
       ag["branch"].startswith("c1c") and ag["systems"]["B"]["N"] == 5 and ag["systems"]["B"]["skeleton_moved_seeds"] == [1, 2]
       and ag["R"] is None)
    Ak = dict(A5); Ak[3] = cfake(D=1.0, P=0.2)
    ag = control_aggregate(Ak, Bh, v2_closed=None)
    ck("R 집합 A 4 · B 5 → c1 (둘 다 ≥ 4) · A 의 이동 시드는 R 에서만 빠진다",
       ag["branch"].startswith("c1a") and ag["R"]["n_a"] == 4 and ag["systems"]["A"]["N"] == 5)
    Be = dict(Bh); Be[3] = cfake(err="traj.xyz 를 못 읽었다")
    ck("⛔음성 오류 런 하나 → 판정 보류 (갈래 없음)", control_aggregate(A5, Be, v2_closed=None)["branch"].startswith("판정 보류"))
    Bm = dict(Bh); Bm.pop(4)
    ck("⛔음성 런 하나 빠짐 → 판정 보류", control_aggregate(A5, Bm, v2_closed=None)["branch"].startswith("판정 보류"))
    Bn = dict(Bh); Bn[5] = dict(Bh[5], framework={"status": "못 쟀다"})
    ck("⛔음성 골격 못 잰 런 → 판정 보류 (이동으로도 통과로도 세지 않는다)", control_aggregate(A5, Bn, v2_closed=None)["branch"].startswith("판정 보류"))
    ck("⛔음성 N_B 3 이어도 R 집합이 모자라면 c1c — R 을 지어내지 않는다",
       control_aggregate(A5, {sd: cfake(final="통과" if sd <= 3 else "미통과", D=0.5) for sd in SEEDS}, v2_closed=None)["branch"].startswith("c1c"))
    dl = control_detect_limit_pre()
    ck("카드의 결과 전 검출한계를 그대로 싣는다 (없으면 '못 읽었다')",
       isinstance(dl, dict) and "status" not in dl and "status" in control_detect_limit_pre("/nonexistent.json"))
    ck("생산 T: 헤더가 없으면 None (지어내지 않는다)", prod_temperature("/nonexistent/md.log", 5.0) is None)

    # ── 보고량 ③ 산포 · 대조 잡 A ↔ v2 마감 (2026-10-14 · 결과 전) ──
    card_A = [0.9552, 0.9698, 1.0, 1.0042, 1.2039]          # 카드 §4 모의 입력 = v2 마감 600 K D/중앙값
    ck("산포: 카드 모의의 A 다섯 → sd(ln D) 0.0935 (표본 SD · 넷째 자리 입력이라 ±2e-4 · 모집단 SD 면 0.084) · "
       "max/min 1.2604 (v2 마감)",
       abs(spread_ctrl(card_A)["sd_ln"] - 0.0935) <= 2e-4 and spread_ctrl(card_A)["max_over_min"] == 1.2604)
    _sb = control_aggregate(A5, Bk, v2_closed=None)["systems"]["B"]
    ck("산포: R 집합은 골격 이동 시드를 뺀다 (B 3) · N 집합 기록은 C1·C2 그대로 (B 5)",
       _sb["D_relative_spread_R_set"]["n"] == 3 and _sb["D_relative_spread_N_set_record"]["n"] == 5)
    ck("⛔음성 산포: 시드가 하나 · 없음이면 '못 낸다' (지어내지 않는다)",
       "status" in spread_ctrl([1.0]) and "status" in spread_ctrl([]) and "status" in spread_ctrl([None, 1.0]))
    with tempfile.TemporaryDirectory() as td2:
        def _closure(dvals, p90s, name):
            f = pathlib.Path(td2) / name
            f.write_text(json.dumps({"1_확정": {"D_시드간_상대산포_보고량": {"600K": {"D_over_median_정렬": dvals}}},
                                     "4_기록_남길_것": {"p90²_5ps_lag": {"✅_측정_2026_10_05": {"런별": {
                                         f"T600_seed{sd}": {"창_p90²_Å²": p90s} for sd in SEEDS}}}}},
                                    ensure_ascii=False), encoding="utf-8")
            return f
        A5p = {sd: dict(A5[sd], p90sq_5ps_lag={"p90sq_A2": [55.0, 60.0]}) for sd in SEEDS}
        a_dm = rel_spread([A5[sd]["_D_slope"] for sd in SEEDS])["D_over_median"]
        ag = control_aggregate(A5p, Bh, v2_closed=_closure(a_dm, [55.04, 59.96], "good.json"))
        ac = ag["A_reproduces_v2_closure"]
        ck("대조 잡: A 가 v2 마감을 재현하면 (D/중앙 같음 · p90² 차 ≤ 0.05) 갈래를 그대로 낸다",
           ac["D_same"] is True and ac["p90_same"] is True and ag["branch"].startswith("c1a"))
        ck("⛔음성 대조 잡: A 의 D/중앙이 마감과 다르면 판정 보류 (A 쪽 R 을 믿을 수 없다)",
           control_aggregate(A5p, Bh, v2_closed=_closure([0.9, 1.0, 1.0, 1.1, 1.2], [55.0, 60.0], "bad_d.json"))
           ["branch"].startswith("판정 보류"))
        agp = control_aggregate(A5p, Bh, v2_closed=_closure(a_dm, [55.2, 60.0], "bad_p.json"))
        ck("⛔음성 대조 잡: p90² 만 다르면 갈래는 그대로 · p90_same False (B p90² 를 같은 잣대로 안 읽는다)",
           agp["branch"].startswith("c1a") and agp["A_reproduces_v2_closure"]["p90_same"] is False)
        agw = control_aggregate(A5p, Bh, v2_closed=_closure(a_dm, [55.0, 60.0, 58.0], "bad_n.json"))
        ck("⛔음성 대조 잡: p90² 창 수가 다르면 (2 대 3) 같다고 하지 않는다",
           agw["A_reproduces_v2_closure"]["p90_same"] is False)
        ck("⛔음성 대조 잡: 마감 파일이 없으면 '못 봄' → 판정 보류 (같다고 하지 않는다)",
           control_aggregate(A5p, Bh, v2_closed=pathlib.Path(td2) / "none.json")["branch"].startswith("판정 보류"))
    _real = a_reproduces_v2(A5p)
    ck("대조 잡: 실제 v2 마감에서 키를 읽는다 (D/중앙 다섯 = 카드 모의 입력 · p90² 다섯 시드 × 8 창)",
       "status" not in _real and _real["D_over_median_v2"] == card_A
       and all(x.get("n_windows_v2") == 8 for x in _real["p90"].values()))

    # ── B 측정 가능 조건 카드 ① 단계 (B 650 K 만 · 2026-10-19 · 결과 전) ──
    def bfake(final="통과", c1=True, D=0.5, P=0.0, Sm=0, SS=0, St=0, err=None, over=8, nwin=8):
        r = cfake(final=final, c1=c1, D=D, P=P, Sm=Sm, SS=SS, St=St, err=err)
        r["p90sq_5ps_lag"] = {"p90sq_A2": [60.0] * nwin, "n_windows": nwin, "n_windows_over": over, "median_A2": 60.0,
                              "max_A2": 60.0, "half_box_sq_A2": 50.0}
        return r
    dB = {sd: 0.5137291 + 0.0011 * sd for sd in SEEDS}
    B1 = {1: bfake(D=dB[1]), 2: bfake(D=dB[2]), 3: bfake("경계 · 구분 불가", D=dB[3]),
          4: bfake("경계 · 끝 두 b 갈림", D=dB[4], P=0.012, St=3), 5: bfake("미통과", D=dB[5], over=6)}
    o = bmeas_stage_b(A5, B1, v2_closed=None, ref600=None, detect_n_sim=20)
    ck("b1: N_B 2 → A 650 K 를 돌리지 않고 닫는다 · 문장 안에 단서 (경계 2 · 미통과 1 · C1 5/5)",
       o["branch"].startswith("b1") and "(N_B = 2/5 · 경계 2 · 미통과 1 · C1 5/5)" in (o["sentence"] or "")
       and "A 650 K 는 돌리지 않았고" in o["sentence"] and o["errors"] == [])
    def _allkeys(x):
        if isinstance(x, dict):
            for k, v in x.items():
                yield k
                yield from _allkeys(v)
        elif isinstance(x, list):
            for v in x:
                yield from _allkeys(v)
    ck("⛔ ① 단계는 R 을 내지 않는다 (어느 깊이에도 R · excludes_1 키가 없다 · 검출한계도 b1 이면 없다)",
       not ({"R", "excludes_1", "lo", "hi"} & set(_allkeys(o))) and o["detect_limit_stage2_pre"] is None)
    _sd = o["skeleton_distribution"]["B650"]
    ck("네 지표 분포: 통과 런 (seed1 · 2) 도 싣는다 · 다섯 런 · ① 최대 0.012 · 중앙 0.0 · ④ 최대 3 · 문턱 초과 0",
       set(_sd["①_P_frac"]["per_seed"]) == set(SEEDS) and _sd["①_P_frac"]["n"] == 5 and _sd["①_P_frac"]["max"] == 0.012
       and _sd["①_P_frac"]["median"] == 0.0 and _sd["④_S_transient"]["max"] == 3 and _sd["④_S_transient"]["n_over_gate"] == 0
       and _sd["seeds_counting_in_N"] == [1, 2])
    ck("p90² 포화: 8/8 넷 · 6/8 하나 → 포화 4/5 (기록 · 갈래와 무관)",
       o["p90_saturation"]["B650"]["n_saturated"] == 4 and o["p90_saturation"]["B650"]["n_runs"] == 5)
    _jo = json.dumps(o, ensure_ascii=False, default=str)
    ck("⛔ ① 단계 산출물에 D 가 없다 (_D_slope · 심은 D 값이 안 보인다)",
       "_D_slope" not in _jo and not any(repr(v) in _jo for v in dB.values()))
    B2r = {sd: bfake(final="통과" if sd <= 4 else "경계 · 구분 불가", D=dB[sd]) for sd in SEEDS}
    o = bmeas_stage_b(A5, B2r, v2_closed=None, ref600=None, detect_n_sim=40)
    _dl = o["detect_limit_stage2_pre"] or {}
    ck("b2 · B R 집합 4: ② 단계 검출한계를 A 650 K 전에 낸다 (B 실측 σ_ln · A 0.0935 가정 · n 5/4 · 카드 기준 행 병기)",
       o["branch"].startswith("b2") and "B R 집합 4" in o["branch"] and "측정 가능했다" in (o["sentence"] or "")
       and _dl.get("sigma_ln_B") == spread_ctrl([dB[sd] for sd in (1, 2, 3, 4)])["sd_ln"] and _dl.get("sigma_ln_A") == 0.0935
       and _dl.get("n_a") == 5 and _dl.get("n_b") == 4
       and (_dl.get("card_rows_pre") or {}).get("σ_표본SD_0.094", {}).get("R50") == 1.2
       and (_dl.get("card_rows_pre") or {}).get("B_산포_2배", {}).get("R80") == 1.5)
    ck("⛔ b2 문장은 '사이' 로 쓴다 · '= 650 K' 금지가 같이 실린다", "600 K 와 650 K 사이다" in o["sentence"]
       and "'B 의 측정 가능 온도 = 650 K' 로 쓰지 않는다" in o["sentence_⛔"])
    o = bmeas_stage_b(A5, {sd: bfake(final="통과" if sd <= 3 else "미통과", D=dB[sd]) for sd in SEEDS}, v2_closed=None, ref600=None, detect_n_sim=20)
    ck("⛔ b2 · N_B 3 → R 집합 3 < 4: ② 를 돌려도 R 이 없다고 적고 A 실행은 외부 1저자 확인 (검출한계 안 냄)",
       o["branch"].startswith("b2") and "R 은 없다 (b2c 로 정해짐)" in o["branch"] and o["detect_limit_stage2_pre"] is None
       and "외부 1저자" in (o["next"] or ""))
    Bmv = dict(B2r); Bmv[2] = bfake(D=dB[2], St=6)
    o = bmeas_stage_b(A5, Bmv, v2_closed=None, ref600=None, detect_n_sim=20)
    ck("골격 이동 하나 → N_B 4 그대로 · R 집합 3 · 문장 안에 '골격 이동 1'",
       o["B"]["N"] == 4 and o["B"]["R_set_seeds"] == [1, 3, 4] and "· C1 5/5 · 골격 이동 1 ·" in o["sentence"]
       and "R 은 없다" in o["branch"])
    for nm, bb in (("오류 런", {**B1, 3: bfake(err="traj.xyz 를 못 읽었다")}),
                   ("런 하나 빠짐", {sd: B1[sd] for sd in (1, 2, 3, 5)}),
                   ("골격 못 잰 런", {**B1, 5: dict(B1[5], framework={"status": "못 쟀다"})}),
                   ("최종 C2 가 빈 런 (오류 없이)", {**B1, 4: bfake(final=None, D=dB[4])})):
        o = bmeas_stage_b(A5, bb, v2_closed=None, ref600=None, detect_n_sim=20)
        ck(f"⛔음성 ① 단계 {nm} → 판정 보류 (문장 · 다음 없음)",
           o["branch"].startswith("판정 보류") and o["sentence"] is None and o["next"] is None and o["errors"])
    o = bmeas_stage_b({**A5, 2: cfake(err="msd 를 못 읽었다")}, B1, v2_closed=None, ref600=None, detect_n_sim=20)
    ck("⛔음성 대조 잡 쪽 A 600 K 런이 오류면 판정 보류", o["branch"].startswith("판정 보류"))
    rd600 = readout600()
    _s6b, _s6a = skeleton_distribution(rd600.get("B", [])), skeleton_distribution(rd600.get("A", []))
    ck("10-14 기록 (실파일): B 600 K N 1 · 네 지표 ① 최대 0.003 · ④ 최대 1 · p90² 포화 1/5 | A ① 최대 0.006 · ④ 최대 2",
       rd600.get("N") == {"A": 5, "B": 1} and rd600.get("n_boot") == 400 and _s6b["①_P_frac"]["max"] == 0.003
       and _s6b["④_S_transient"]["max"] == 1 and p90_saturation(rd600["B"])["n_saturated"] == 1
       and _s6a["①_P_frac"]["max"] == 0.006 and _s6a["④_S_transient"]["max"] == 2)
    ck("대조 잡 ② (실파일): 기록의 A 행을 그대로 넣으면 같다 (n_boot 400)",
       a600_reproduces_readout(json.loads(json.dumps(rd600["A"])), 400, rd600)["same"] is True)
    ck("⛔음성 대조 잡 ②: n_boot 가 기록과 다르면 '못 봄' (같다고 하지 않는다)",
       a600_reproduces_readout(rd600["A"], 200, rd600)["same"] is None)
    ck("⛔음성 대조 잡 ②: 기록 파일이 없으면 '못 봄'", a600_reproduces_readout(rd600["A"], 400, readout600("/nonexistent.json"))["same"] is None)
    with tempfile.TemporaryDirectory() as td3:
        A5q = {sd: bfake(D=1.0 + 0.0213 * sd) for sd in SEEDS}          # p90² 창이 있는 A (대조 잡 ② 는 창까지 본다)
        rows_a = json.loads(json.dumps(_control_system("A", A5q, [])[0]["rows"], default=str))
        rows_b6 = json.loads(json.dumps(_control_system("B", {sd: bfake(final="통과" if sd == 2 else "경계 · 구분 불가")
                                                              for sd in SEEDS}, [])[0]["rows"], default=str))

        def _rec(rows, name, nb=400):
            f = pathlib.Path(td3) / name
            f.write_text(json.dumps({"aggregate": {"systems": {"A": {"rows": rows, "N": 5}, "B": {"rows": rows_b6, "N": 1}}},
                                     "n_boot": nb, "tool_sha16": {"glass_v2_readout.py": "x"}}, ensure_ascii=False), encoding="utf-8")
            return f
        o = bmeas_stage_b(A5q, B2r, v2_closed=None, ref600=_rec(rows_a, "same.json"), detect_n_sim=20)
        ck("대조 잡 ②: A 600 K 행이 기록과 같으면 갈래를 그대로 낸다 · b2 문장에 '600 K 는 1/5'",
           o["control_jobs"]["②_A600_vs_readout_1014"]["same"] is True and o["branch"].startswith("b2")
           and "600 K 는 1/5" in o["sentence"] and o["skeleton_distribution"]["B600_record_1014"]["①_P_frac"]["n"] == 5)
        bad = json.loads(json.dumps(rows_a)); bad[2]["skeleton"]["values"]["④_S_transient"] = 1
        o = bmeas_stage_b(A5q, B2r, v2_closed=None, ref600=_rec(bad, "bad_sk.json"), detect_n_sim=20)
        ck("⛔음성 대조 잡 ②: A 골격 값 하나가 기록과 다르면 판정 보류",
           o["branch"].startswith("판정 보류") and o["control_jobs"]["②_A600_vs_readout_1014"]["same"] is False)
        bad = json.loads(json.dumps(rows_a)); bad[0]["beta_MTO"] += 1e-6
        ck("⛔음성 대조 잡 ②: β_MTO 가 1e-6 다르면 판정 보류",
           bmeas_stage_b(A5q, B2r, v2_closed=None, ref600=_rec(bad, "bad_b.json"), detect_n_sim=20)["branch"].startswith("판정 보류"))
        bad = json.loads(json.dumps(rows_a)); bad[3]["record"]["p90sq_5ps_lag"]["p90sq_A2"][5] += 0.02
        ok01 = json.loads(json.dumps(rows_a)); ok01[3]["record"]["p90sq_5ps_lag"]["p90sq_A2"][5] += 0.01
        ck("대조 잡 ②: p90² 창 하나가 0.01 (둘째 자리 반올림 한 칸) 다르면 같다 · 0.02 면 판정 보류",
           a600_reproduces_readout(rows_a, 400, readout600(_rec(ok01, "p01.json")))["same"] is True
           and bmeas_stage_b(A5q, B2r, v2_closed=None, ref600=_rec(bad, "p02.json"), detect_n_sim=20)["branch"].startswith("판정 보류"))
        ck("⛔음성 대조 잡 ②: 기록 n_boot 가 다르면 판정 보류",
           bmeas_stage_b(A5q, B2r, v2_closed=None, ref600=_rec(rows_a, "nb.json", nb=200), detect_n_sim=20)["branch"].startswith("판정 보류"))
        ck("⛔음성 대조 잡 ②: 기록이 없으면 판정 보류",
           bmeas_stage_b(A5q, B2r, v2_closed=None, ref600=pathlib.Path(td3) / "none.json", detect_n_sim=20)["branch"].startswith("판정 보류"))
        cl = pathlib.Path(td3) / "v2bad.json"
        cl.write_text(json.dumps({"1_확정": {"D_시드간_상대산포_보고량": {"600K": {"D_over_median_정렬": [0.9, 1.0, 1.0, 1.1, 1.2]}}},
                                  "4_기록_남길_것": {"p90²_5ps_lag": {"✅_측정_2026_10_05": {"런별": {}}}}}), encoding="utf-8")
        ck("⛔음성 대조 잡 ①: A 600 K 가 v2 마감 D/중앙을 재현 못 하면 판정 보류 (상시 · 개정 CX §7)",
           bmeas_stage_b(A5q, B2r, v2_closed=cl, ref600=_rec(rows_a, "same2.json"), detect_n_sim=20)["branch"].startswith("판정 보류"))
        import subprocess
        e1, e2 = pathlib.Path(td3) / "ra", pathlib.Path(td3) / "rb"
        e1.mkdir(); e2.mkdir()
        cp = subprocess.run([sys.executable, str(HERE / "glass_v2_readout.py"), "--bmeas_b", "--root_a", str(e1), "--root_b", str(e2)],
                            capture_output=True, text=True)
        ck("⛔음성 CLI --bmeas_b: 런이 없으면 아무 것도 안 읽고 종료 2 · A 는 T600 · B 는 T650 경로 다섯씩",
           cp.returncode == 2 and cp.stdout.count("/T600/msd.json") == 5 and cp.stdout.count("/T650/msd.json") == 5
           and "판독 · B 650 K" not in cp.stdout)

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
        (rd / "md.log").write_text("Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]\n" + "".join(
            f"{0.5 * i:8.4f} -1.0 -1.0 0.1 {600 + (10 if i % 2 else -10):6.1f}\n" for i in range(40)))
        (rd.parents[1] / "run_meta.json").write_text(json.dumps({"equilib_ps": 5.0}))
        dd = json.loads(js.read_text()); dd["msd_max_A2"] = 50.0; js.write_text(json.dumps(dd))
        cr, cm = collect_control(pathlib.Path(td), N_LI["B"], n_boot=10)
        p9 = (cr.get(1) or {}).get("p90sq_5ps_lag") or {}
        ck("대조 수집: seed1 만 있으면 넷이 missing · N_eff = 45 × 50 / a² · 생산 T 평균 600 (t ≥ 5 ps · 30 줄)",
           len(cm) == 4 and 1 in cr and abs(cr[1]["N_eff_he2018"] - M.he2018_neff(45, 50.0)) < 1e-9
           and cr[1]["T_prod"]["mean_K"] == 600.0 and cr[1]["T_prod"]["n_rows"] == 30 and cr[1]["T_prod_equilib_assumed_5ps"] is False)
        ck("대조 수집: p90² — 110 ps 궤적에 50 ps 창 2 개 · (d/2)² = (12/2)² = 36 · 창마다 값",
           p9.get("n_windows") == 2 and p9.get("half_box_sq_A2") == 36.0 and len(p9.get("p90sq_A2", [])) == 2 and p9.get("cell_cubic") is True)
        # 창 수 — 드라이버 꼴 (첫 관측이 한 간격 뒤 · prod 100 ps = 1000 프레임) 에서 (n−1)·dt/50 은 1 창이 된다
        from ase.io import read as _aread
        tr = pathlib.Path(td) / "t1000.xyz"
        write(str(tr), _aread(str(rd / "traj.xyz"), index=":1000"), format="extxyz")
        w2 = p90sq_windows(tr, 100.0, prod_ps=100.0)
        ck("p90² 창 수: 1000 프레임 · prod 100 ps → 2 창 (선언된 prod 로 센다 · 프레임 수 식이면 1 창)",
           w2.get("n_windows") == 2 and w2.get("n_windows_from") == "prod_ps" and w2.get("n_frames") == 1000)
        ck("⛔음성 p90²: 궤적이 선언된 prod 보다 짧으면 '못 냈다' (빈 창을 지어내지 않는다)",
           "status" in p90sq_windows(tr, 100.0, prod_ps=110.0))
        import subprocess
        cli = subprocess.run([sys.executable, str(HERE / "aimd_jump_stats.py"), "--traj", str(tr), "--label", "w1",
                              "--out_dir", str(pathlib.Path(td) / "cli"), "--save_fs", "100", "--t_from_ps", "50",
                              "--t_to_ps", "100", "--hop_census_lag_ps", "5.0", "--hop_min_dist", "2.0"],
                             capture_output=True, text=True)
        try:
            hc = json.loads((pathlib.Path(td) / "cli" / "w1_hop_census.json").read_text(encoding="utf-8"))
            p_cli = round(hc["per_ion_max_A"]["p90"] ** 2, 2)
        except (OSError, ValueError, KeyError):
            p_cli = None
        ck(f"p90²: 둘째 창 [50, 100] 이 v2 기록을 낸 CLI (aimd_jump_stats.py --t_from_ps 50 --t_to_ps 100) 와 같다 "
           f"({w2.get('p90sq_A2', [None, None])[1]} vs {p_cli} · rc {cli.returncode})",
           p_cli is not None and w2.get("p90sq_A2") and abs(w2["p90sq_A2"][1] - p_cli) < 1e-9)
        dd = json.loads(js.read_text()); dd.pop("msd_max_A2", None)
        dd["msd_Li_A2"][7] = 99.0                               # 배열 최댓값을 심는다 (창끝 값이 아니다)
        js.write_text(json.dumps(dd))
        cr2, _ = collect_control(pathlib.Path(td), N_LI["A"], n_boot=10, framework=False, p90=False)
        ck("⛔음성 N_eff: msd_max_A2 가 없는 옛 기록은 msd_Li_A2 배열 max 로 되살린다 (rsd_report 한 곳 · 48 × 99 / a²)",
           abs(cr2[1]["N_eff_he2018"] - M.he2018_neff(48, 99.0)) < 1e-9
           and cr2[1]["N_eff_inputs"]["msd_max_from"].startswith("msd_Li_A2"))
        _, cm650 = collect_control(pathlib.Path(td), N_LI["B"], n_boot=10, framework=False, p90=False, temp=BMEAS_T)
        ck("⛔음성 온도 인자: T600 만 있는 루트를 650 K 로 읽으면 다섯 다 결측 (600 K 런을 650 K 로 읽지 않는다)",
           len(cm650) == 5 and all("/T650/" in m and "/T600/" not in m for m in cm650))
        import shutil
        r650 = pathlib.Path(td) / "r650" / "seed1" / "T650" / "d0.00_cfg0" / "T650"
        shutil.copytree(rd, r650)
        cr650, cm650 = collect_control(pathlib.Path(td) / "r650", N_LI["B"], n_boot=10, framework=False, p90=False, temp=BMEAS_T)
        ck("온도 인자: T650 트리를 읽는다 (seed1 · msd_json 이 T650 · 나머지 넷 결측) · 기본값은 그대로 T600",
           1 in cr650 and "/T650/" in cr650[1]["msd_json"] and len(cm650) == 4
           and "/T600/" in str(control_msd_path(td, 1)) and "/T650/" in str(control_msd_path(td, 1, BMEAS_T)))
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
    ap.add_argument("--detect_limit", action="store_true",
                    help="대조 계 카드 (회신 CR): R 의 설계 검출한계 모의 — 결과 전에 낸다")
    ap.add_argument("--sigma_ln", type=float, nargs="+", default=None, help="A 의 시드 간 ln D 표준편차 (여럿이면 차례로)")
    ap.add_argument("--sigma_ln_b", type=float, default=None, help="B 의 σ_ln (기본 = A 와 같음 · 가정)")
    ap.add_argument("--n_a", type=int, default=5)
    ap.add_argument("--n_b", type=int, default=5)
    ap.add_argument("--n_sim", type=int, default=2000)
    ap.add_argument("--control", action="store_true", help="대조 계 판독 (카드 §4 · A 600 K 다섯 대 B 600 K 다섯)")
    ap.add_argument("--root_a", help="--control: A (v2) 600 K 루트 — seed<S>/T600/d0.00_cfg0/T600/msd.json")
    ap.add_argument("--root_b", help="--control: B (Li₃PS₄) 600 K 루트 — 같은 꼴 · --bmeas_b: B 650 K 루트 (T650)")
    ap.add_argument("--bmeas_b", action="store_true",
                    help="B 측정 가능 조건 카드 ① 단계 — B 650 K 다섯만 판독 (--root_b) · A 600 K (--root_a) 는 대조 잡")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.bmeas_b:
        if a.control:
            ap.error("--control 과 --bmeas_b 는 같이 쓰지 않는다")
        if not (a.root_a and a.root_b):
            ap.error("--bmeas_b 에는 --root_a (A 600 K · 대조 잡) 와 --root_b (B 650 K) 가 둘 다 필요하다")
        try:
            sys.stdout.reconfigure(line_buffering=True)
        except Exception:
            pass
        #: 읽기 전에 경로부터 — 런이 빠졌으면 아무 것도 안 읽고 멈춘다 (B 경로가 틀렸는데 A 를 다 읽고서야 알지 않게)
        miss = [str(p) for root, T in ((a.root_a, CONTROL_T), (a.root_b, BMEAS_T)) for sd in SEEDS
                for p in [control_msd_path(root, sd, T)] if not p.is_file()]
        if miss:
            print(f"⛔ msd.json 이 없는 런 {len(miss)} 개 — 읽지 않는다 (카드: 점 · 시드를 빼지 않는다):")
            for m in miss:
                print("   ·", m)
            return 2
        import hashlib
        sha = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest()[:16]
               for f in ("glass_v2_readout.py", "msd_diffusive_check.py", "quench_ss_event.py", "aimd_jump_stats.py",
                         "melt_quench_uma.py", "../modelc_v3/disorder_ensemble_diffusion.py")}
        print(f"li2s B 측정 가능 조건 카드 ① 단계 판독 · B {BMEAS_T} K {a.root_b} · 대조 잡 A {CONTROL_T} K {a.root_a} · "
              f"n_boot {a.n_boot} · 골격 네 기준 {SKELETON_GATE}")
        print("도구 sha16 · " + " · ".join(f"{pathlib.Path(k).name} {v}" for k, v in sha.items()))
        ra, ma = collect_control(a.root_a, N_LI["A"], n_boot=a.n_boot)
        rb, mb = collect_control(a.root_b, N_LI["B"], n_boot=a.n_boot, temp=BMEAS_T)
        if ma or mb:
            print(f"⛔ 읽는 사이에 msd.json 이 사라진 런 {len(ma) + len(mb)} 개 — 판독하지 않는다")
            return 2
        o = bmeas_stage_b(ra, rb, n_boot=a.n_boot)
        print("\n".join(bmeas_show(o)))
        if a.out:
            out = {"what": f"li2s B 측정 가능 조건 카드 ① 단계 판독 (B {BMEAS_T} K 만 · 결과 전 커밋 도구)", "tool_sha16": sha,
                   "stage_b": o, "runs_B650": strip_D(rb), "runs_A600_control_job": strip_D(ra), "n_boot": a.n_boot}
            pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
            print(f"-> {a.out}")
        return 3 if o["errors"] else 0
    if a.control:
        if not (a.root_a and a.root_b):
            ap.error("--control 에는 --root_a 와 --root_b 가 둘 다 필요하다")
        try:
            sys.stdout.reconfigure(line_buffering=True)
        except Exception:
            pass
        import hashlib
        #: 판독에 들어가는 파일 전부 — 골격은 melt_quench_uma 의 컷오프를 빌리고 (quench_ss_event._load_mq) ·
        #  selftest 의 합성 MTO 는 드라이버 함수로 만든다 (v2 판독 기록과 같은 목록 + aimd_jump_stats) · 로그 머리에 찍는다
        sha = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest()[:16]
               for f in ("glass_v2_readout.py", "msd_diffusive_check.py", "quench_ss_event.py", "aimd_jump_stats.py",
                         "melt_quench_uma.py", "../modelc_v3/disorder_ensemble_diffusion.py")}
        print(f"li2s 대조 판독 · A {a.root_a} · B {a.root_b} · n_boot {a.n_boot} · {CONTROL_T} K · 골격 네 기준 {SKELETON_GATE}")
        print("도구 sha16 · " + " · ".join(f"{pathlib.Path(k).name} {v}" for k, v in sha.items()))
        ra, ma = collect_control(a.root_a, N_LI["A"], n_boot=a.n_boot)
        rb, mb = collect_control(a.root_b, N_LI["B"], n_boot=a.n_boot)
        if ma or mb:
            print(f"⛔ msd.json 이 없는 런 {len(ma) + len(mb)} 개 — 판독하지 않는다 (카드: 점 · 시드를 빼지 않는다):")
            for m in ma + mb:
                print("   ·", m)
            return 2
        agg = control_aggregate(ra, rb, detect_pre=control_detect_limit_pre())
        print("\n".join(control_show(agg)))
        if a.out:
            out = {"what": "li2s 대조 계 판독 (카드 §4 · 결과 전 커밋 도구)", "tool_sha16": sha, "aggregate": agg,
                   "runs_A": strip_D(ra), "runs_B": strip_D(rb), "n_boot": a.n_boot}
            pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
            print(f"-> {a.out}")
        return 3 if agg["errors"] else 0
    if a.detect_limit:
        if not a.sigma_ln:
            ap.error("--detect_limit 에는 --sigma_ln 이 필요하다 (눈금을 지어내지 않는다)")
        res = []
        for s in a.sigma_ln:
            d = ratio_detect_limit(s, n_a=a.n_a, n_b=a.n_b, sigma_b=a.sigma_ln_b, n_sim=a.n_sim)
            res.append(d)
            print(f"σ_ln A {s:.4f} · B {d['sigma_ln_B']:.4f} · n {a.n_a}/{a.n_b} · 모의 {d['n_sim']} · 부트 {d['n_boot']} → "
                  f"R₅₀ {d['R50']} · R₈₀ {d['R80']} · R=1 오검출 {d['false_detect_at_R1']:.3f}")
            print("   " + " · ".join(f"{r:g}:{q:.2f}" for r, q in d["rows"]))
        if a.out:
            pathlib.Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            print(f"-> {a.out}")
        return 0
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
