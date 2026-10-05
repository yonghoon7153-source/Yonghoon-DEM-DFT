#!/usr/bin/env python3
"""judge_eprime.py — E′ 파일럿 **판정**. 카드 v5.2 §2 집계식을 코드에 둔다.

    python3 tools/doping/judge_eprime.py --out_root ~/runs/eprime_2026_09_14
    python3 tools/doping/judge_eprime.py --out_root ... --ignore_eligibility   # ⛔ 인용금지
    python3 tools/doping/judge_eprime.py --selftest
    python3 tools/doping/judge_eprime.py --card v6 --out_root ~/work/runs/cascade_v6_40run_0921   # 카드 v6 (부모 10 · 600 K · t(n−1))
    python3 tools/doping/judge_eprime.py --probe <PROBE_ROOT>                     # 카드 v7 + 개정 CP 탐침 (T* 선택 · D 안 찍음)
    python3 tools/doping/judge_eprime.py --card v7 --probe_json <PROBE_ROOT>/cascade_v7_probe.json --out_root <MAIN_ROOT>

무엇을 하나
  ① 런마다 `msd_diffusive_check.aggregation_eligible(t, y, events_per_run)` 로 **자격** 판정
  ② 자격 통과 런만으로 카드 §2 집계식:
       D̄_{p,k} = 시드 2 산술평균 (600 K) · R_k = D̄_P1/D̄_P2 · L_k = ln R_k
       L̄ = (L_A+L_B)/2 · SE = |L_A−L_B|/2 · 95 % 구간 = L̄ ± 12.706·SE (t, df 1)
       판정 = **구간의 위치** 3 갈래 (δ = ln 1.5)
  ③ 2차: (p,k) 마다 600/800/1000 K × 시드 2 = 6 점 겉보기 아레니우스 →
       a_k = Ea(P1_k) − Ea(P2_k) [meV] · ā · SE_a · 구간 ± 12.706·SE_a · δ_Ea = 30 meV

v6 (카드 cascade_estimand_card_v6_10parents_2026_09_19 §4 — v5.2 df 1 식의 일반형)
  · 부모 목록 = db/properties/cascade_v6_parents_2026_09_19.json 의 4_parents (코드에 안 박는다) · 600 K 만 · 2차 ΔEa 없음
  · L̄ = mean(L_k) · SE = sd(L_k)/√n (표본 sd) · 95 % 구간 = L̄ ± t(0.975, n−1)·SE · n = 유효 부모 수 · δ = ln 1.5
  · ⛔ 40 런(부모 × 처방 × 시드)의 msd.json 이 하나라도 없으면 **집계하지 않는다** (카드 §4 'n=10 을 다 채우기 전에 집계하지 않는다')
    — 있는데 자격 미달·실패인 런은 결과다(결측 규칙으로 n 이 준다). --allow_partial 은 ⛔ 인용·판정 금지 표시를 단다.
  · ⭐ MSD·D·사건 수는 **궤적(traj.xyz)에서 카드 정의대로** 낸다 (`card_curve_from_run`) — 카드 v4 §2 (v5 '그대로' · v6 §3 승계):
      기준계 = 비-Li 골격 COM(질량 가중)을 매 프레임 뺀다 (Li COM 은 안 뺀다)
      MSD   = 분수좌표 unwrap → 실공간 → 골격 COM 제거 → 시간원점 평균 (겹치는 원점 허용)
      D     = 창 2–50 ps 에서 MSD = c + 6Dt 최소제곱 · D = 기울기/6 · c 보고
      사건  = 같은 좌표에서 |r_i(t) − r_i(t_ref)| > 2.5 Å 첫 발생 → 1, t_ref 갱신 (원점 중복 없음)
    ⛔⛔ 2026-10-01 — **첫 v6 판독(commit a9e123ab5)은 이걸 안 했다.** msd.json 의 `times_ps`·`msd_Li_A2`·
      `D_Li_cm2_s` 를 읽었는데, 그건 드라이버의 옛 정의(**단일 시간원점 · 실험실 좌표 · 골격 COM 미제거**)다
      (`disorder_ensemble_diffusion.li_diffusion_from_frames` — '이미 나간 값 재현' 을 위해 바꾸지 않는 곡선).
      카드는 선언했고 판독기는 다른 곡선을 쟀다 — 오류 없이 (조용히 틀린 경로). 그 판독은 자격 0/40 · D 값 표시 없이 끝났다.
      msd.json 의 D 는 이제 `D_legacy_sto_lab` 이름으로 **감사용으로만** 기록한다 (집계에 안 쓴다).

⛔ 이 도구가 **하지 못하는 것**
  · **사건 수를 만들어내지 못한다.** `--save_traj` 없이 돈 라운드에는 궤적이 없고,
    그러면 `events_per_run=None` 이라 카드가 **'검사 불가 = 자격 없음'** 으로 정한다.
    None 을 '통과' 로 바꾸지 않는다 (2026-09-19 실측: 그래서 30 런 전부 자격 미달).
  · 잔류 평균압 P̄ 를 msd.json 에서 못 읽는다 — 카드 §2 가 모든 D·Ea 에 붙이라고 한
    'V = 4066.48 Å³ · P̄ = <실측>' 중 P̄ 를 **결측으로 보고**한다.
  · 결측 (p,k) 를 메우지 않는다. 시드 하나가 빠지면 그 (p,k) 는 결측이다 (카드 §2 결측 규칙).
  · 판정 문턱을 정하지 않는다. δ_lnD = ln 1.5 · δ_Ea = 30 meV 는 **카드가 정했다**.
  · 절대값을 인용 가능하게 만들지 않는다 (1저자 인용정책 2026-09-18 — 상대차만).
  · ⚠ **v5.2 경로(`main`)는 여전히 msd.json 의 옛 정의(단일 원점·실험실 좌표) D 를 읽는다.** v5 라운드는 궤적이 없어
    카드 정의로 다시 낼 수 없다 — 그 라운드의 가정계산 값(부모 A 0.688 · B 1.381)은 이 정의 차이도 같이 안고 있다.
  · v6 경로는 궤적이 잘렸거나(프레임 수가 aimd_results.json·msd.json 과 다름) save_fs·창이 카드와 다르면 그 런을
    **계산하지 않는다** (검사 불가 = 자격 없음 → 결측 규칙). 메우거나 msd.json 값으로 대체하지 않는다.
  · 골격 COM 은 **전역 1 개**다 — 국소 골격 재배열은 못 지운다 (그건 골격 경보의 몫).
  · (v7 탐침 · 회신 CP P0-1 2026-10-03) 온도·생산길이·시간간격 결속(`protocol_binding_errors`)은 **기록끼리의 일치**다 —
    궤적이 실제로 그 온도로 돌았는지(md.log 의 T[K])는 안 본다. 그 문턱은 카드가 정해야 한다.
  · v6 경로(`judge_runs_card`)에는 그 결속을 **안 건다** — 봉인된 v6 마감·판정을 그대로 두기 위해서다 (회신 CP).
    v7 본 라운드가 v6 경로를 그대로 쓰면 이 구멍도 따라간다 → 연결 여부는 v7 개정에서 정한다.
  · 골격 경보(`framework_alarm`)는 **거부권뿐**이다 — 통과(ok·framework_static)가 골격 보존 인증이 아니다 (회신 CP P1:
    첫↔마지막 프레임만 비교해서 중간에 갔다 돌아온 이동을 못 보고, n < 8 인 종(예: Al₂·O₃)은 판정에서 빠진다).
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "ionic"))

#: 카드 §2 집계식 — 전부 **카드가 정한 값**이다. 여기서 바꾸면 새 라운드다.
T_DF1 = 12.706          # t(0.975, df=1), NIST
DELTA_LND = math.log(1.5)
DELTA_EA_MEV = 30.0
PRIMARY_T = 600
TEMPS = (600, 800, 1000)
SEEDS = (1, 2)
KB_EV = 8.617333262e-5
V_COMMON_A3 = 4066.479695
PAIRS = {"A": ("P1_Al2O3_A", "P2_Al2S3_A"), "B": ("P1_Al2O3_B", "P2_Al2S3_B")}
#: t(0.975, df) — NIST 표 (df 1–30). 카드 v6 §4 의 일반 n 용. 표 밖이면 판정하지 않는다.
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
        21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042}
V6_PARENTS = REPO / "db" / "properties" / "cascade_v6_parents_2026_09_19.json"
#: 카드 v4 §2 (v5·v6 승계) 의 MSD 창 [ps]. 런의 msd.json `fit_window_ps` 가 이것과 다르면 그 런을 **거부**한다.
CARD_WINDOW_PS = (2.0, 50.0)
#: 카드 v4 §2 `독립_홉_사건` 의 변위 문턱 [Å] (런당 하한 50 은 `msd_diffusive_check.EVENTS_MIN_PER_RUN`).
EVENT_D_HOP_A = 2.5
#: 한 프레임 간격의 최소상 변위가 셀의 이 비율을 넘으면 unwrap 이 모호하다 → 그 런을 거부한다.
#: 100 fs 에 Li 가 셀 높이(~10 Å)의 40 % 를 가는 일은 물리적으로 없다 — 걸리면 저장 간격·궤적 이상이다.
UNWRAP_STEP_MAX_FRAC = 0.40


def load_v6_pairs(path=V6_PARENTS):
    """카드 v6 부모 목록 → {부모: (P1 구조, P2 구조)}. 원장의 P1_xyz/P2_xyz 파일 이름과 맞는지 확인한다 (어긋나면 거부)."""
    d = json.load(open(path, encoding="utf-8"))
    out = {}
    for e in d["4_parents"]:
        k = e["parent"]
        p1, p2 = f"P1_Al2O3_{k}", f"P2_Al2S3_{k}"
        if Path(e["P1_xyz"]).stem != p1 or Path(e["P2_xyz"]).stem != p2:
            raise SystemExit(f"⛔ 부모 {k} 의 구조 이름이 원장과 다르다 ({e['P1_xyz']} · {e['P2_xyz']})")
        out[k] = (p1, p2)
    return out


def missing_runs(runs, pairs, T=PRIMARY_T, seeds=SEEDS):
    """카드 v6 §4 완결성 — 있어야 할 (구조, T, 시드) 중 msd.json 이 **없는** 것. 있는데 실패한 런은 여기 안 든다 (그건 결과다)."""
    return [(st, T, sd) for k in sorted(pairs) for st in pairs[k] for sd in seeds if (st, T, sd) not in runs]


def aggregate_n(j, pairs, T=PRIMARY_T):
    """카드 v6 §4 — 부모 n 개 일반형. 유효 부모가 2 미만이거나 t 표 밖이면 **구간 판정을 만들지 않는다**."""
    res = {"primary": {"T_K": T, "delta_lnD": round(DELTA_LND, 6), "n_parents_declared": len(pairs)}, "parents": {}}
    Ls = {}
    for k, (p1, p2) in sorted(pairs.items()):
        d1, d2 = dbar(j, p1, T), dbar(j, p2, T)
        row = {"D_bar_P1": d1, "D_bar_P2": d2}
        if d1 and d2:
            row["R"] = d1 / d2; row["lnR"] = math.log(row["R"]); Ls[k] = row["lnR"]
        else:
            row["⛔"] = "결측 — 시드 하나라도 실패·자격 미달이면 그 부모는 빠진다 (대체 금지 · 카드 §3)"
        res["parents"][k] = row
    n = len(Ls)
    res["primary"]["n_valid"] = n
    if n < 2 or (n - 1) not in T975:
        res["primary"]["⛔"] = f"유효 부모 {n} — 구간 판정 없음 (n ≥ 2 · df ≤ 30 이어야 한다)"
        return res
    v = list(Ls.values())
    Lb = sum(v) / n
    sd = math.sqrt(sum((x - Lb) ** 2 for x in v) / (n - 1))
    se, t = sd / math.sqrt(n), T975[n - 1]
    lo, hi = Lb - t * se, Lb + t * se
    pos = sum(1 for x in v if x > 0)
    res["primary"].update({"L_bar": Lb, "sd": sd, "SE": se, "t": t, "df": n - 1, "ci_ln": [lo, hi],
                           "ratio": math.exp(Lb), "ci_ratio": [math.exp(lo), math.exp(hi)],
                           "verdict": verdict_interval(lo, hi, DELTA_LND),
                           "sign_count": f"L_k > 0 : {pos}/{n} · < 0 : {sum(1 for x in v if x < 0)}/{n}"})
    return res


def parse_tag(tag: str):
    """md/<tag>/ 에서 (구조, 시드). 속도시험 태그 `X__T600__s1` 도 같은 규칙으로 읽는다."""
    m = re.match(r"^(.*?)(?:__T\d+)?__s(\d+)$", tag)
    return (m.group(1), int(m.group(2))) if m else (None, None)


def scan(out_root):
    """out_root/md/**/T*/msd.json → {(구조, 온도, 시드): 기록}. ⛔ 고르지 않는다 — 전부 담는다."""
    runs = {}
    for f in sorted(glob.glob(os.path.join(out_root, "md", "*", "*", "T*", "msd.json"))):
        tag = Path(f).relative_to(Path(out_root) / "md").parts[0]
        st, sd = parse_tag(tag)
        if st is None:
            continue
        d = json.load(open(f))
        runs[(st, int(d["T_K"]), sd)] = {
            "path": f, "tag": tag, "D": float(d["D_Li_cm2_s"]),
            "t": d["times_ps"], "y": d["msd_Li_A2"],
            "n_Li": d.get("n_Li"), "fit_window_ps": d.get("fit_window_ps"),
            "t_end_ps": (d["times_ps"][-1] if d.get("times_ps") else None)}
    return runs


def count_events(run_dir, d_hop=2.5):
    """궤적에서 **선언한 변위 사건 수**(2.5 Å 카운터). 궤적이 없으면 **None** — 0 이 아니다.

    ⛔ None 과 0 을 섞지 않는다. None = '못 셌다'(자격 없음) · 0 = '세었는데 없었다'.
    """
    for name in ("traj.xyz", "prod.traj", "traj.extxyz"):
        p = Path(run_dir) / name
        if p.exists():
            try:
                from ase.io import read as aread
                import numpy as _np
                fr = aread(str(p), index=":")
                if len(fr) < 2:
                    return None
                sym = _np.array(fr[0].get_chemical_symbols())
                li = _np.where(sym == "Li")[0]
                p0 = fr[0].get_positions()[li]
                n = 0
                for a in fr[1:]:
                    dd = _np.linalg.norm(a.get_positions()[li] - p0, axis=1)
                    hit = dd >= d_hop
                    n += int(hit.sum())
                    p0[hit] = a.get_positions()[li][hit]
                return n
            except Exception:
                return None
    return None


_MTO = None


def _msd_multi_origin():
    """드라이버의 `msd_multi_origin` 을 **빌려 쓴다** — 복사하면 규약이 갈라진다 (`mto_from_traj` 와 같은 방식)."""
    global _MTO
    if _MTO is None:
        import importlib.util
        src = REPO / "tools" / "modelc_v3" / "disorder_ensemble_diffusion.py"
        spec = importlib.util.spec_from_file_location("_ded_judge", src)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MTO = mod.msd_multi_origin
    return _MTO


def card_curve_arrays(spos, cell, symbols, masses, save_fs, window=CARD_WINDOW_PS, d_hop=EVENT_D_HOP_A):
    """카드 정의(위 docstring v6 ⭐)의 MSD·D·사건 수를 배열에서 낸다 — **순수 함수** (selftest 대상).

    spos (T, N, 3) 분수좌표(감겼든 안 감겼든) · cell (3, 3) 고정(NVT) · symbols · masses (N,) · save_fs [fs].
    → {"t","y": 시간원점 평균 MSD (골격 COM 기준), "D" [cm²/s] (창을 못 맞추면 None), "c_A2", "R2", "events", …}
       또는 {"error": 사유}.  ⛔ error 는 '자격 없음' 이지 0 이 아니다.
    """
    import numpy as np
    from msd_diffusive_check import lin_fit
    spos = np.asarray(spos, dtype=float)
    if spos.ndim != 3 or spos.shape[0] < 8:
        return {"error": f"프레임이 모자란다 ({spos.shape[0] if spos.ndim == 3 else '?'}) — MSD 를 못 만든다"}
    sym = np.asarray(symbols)
    m = np.asarray(masses, dtype=float)
    li = sym == "Li"
    fw = ~li
    if not li.any():
        return {"error": "Li 가 없다"}
    if not fw.any():
        return {"error": "골격(비-Li) 원자가 없다 — 기준계를 못 세운다"}
    d = np.diff(spos, axis=0)
    d -= np.round(d)                                         # 최소상 (분수좌표)
    step = float(np.abs(d).max()) if d.size else 0.0
    if step > UNWRAP_STEP_MAX_FRAC:
        return {"error": f"한 프레임 변위가 셀의 {step:.2f} — unwrap(최소상)이 모호하다 (문턱 {UNWRAP_STEP_MAX_FRAC})"}
    cart = np.concatenate([spos[:1], spos[:1] + np.cumsum(d, axis=0)], axis=0) @ np.asarray(cell, dtype=float)
    com = (cart[:, fw] * m[fw][None, :, None]).sum(axis=1) / m[fw].sum()    # 비-Li 골격 COM (질량 가중)
    rl = (cart - com[:, None, :])[:, li]                                  # Li, 골격 COM 기준
    tau, msd, norig = _msd_multi_origin()(rl, save_fs / 1000.0)
    ev, p0 = 0, rl[0].copy()
    for k in range(1, rl.shape[0]):
        hit = np.linalg.norm(rl[k] - p0, axis=1) > d_hop
        if hit.any():
            ev += int(hit.sum())
            p0[hit] = rl[k][hit]
    out = {"t": [float(x) for x in tau], "y": [float(x) for x in msd],
           "n_origins_min": (int(min(norig)) if norig else None), "events": ev,
           "n_frames": int(spos.shape[0]), "n_Li": int(li.sum()), "n_framework": int(fw.sum()),
           "max_step_frac": step, "fit_window_ps": list(window), "save_fs": float(save_fs)}
    fit = lin_fit(out["t"], out["y"], window[0], window[1])
    if fit is None:
        out.update({"D": None, "c_A2": None, "R2": None,
                    "why_no_D": f"창 {list(window)} ps 를 못 맞춘다 (곡선이 창 끝에 못 닿거나 점 부족)"})
    else:
        slope, icpt, r2 = fit
        out.update({"D": slope / 6.0 * 1e-4, "c_A2": icpt, "R2": r2})    # Å²/ps → cm²/s
    return out


def _ase_read_all(path):
    from ase.io import read as aread
    return aread(str(path), index=":")


def card_curve_from_run(run_dir, times_ps, fit_window_ps, reader=None):
    """런 폴더의 traj.xyz → `card_curve_arrays`. 읽기 전에 **교차확인**하고 하나라도 어긋나면 계산하지 않는다.

      ① traj.xyz · aimd_results.json 이 있다  ② msd.json 창 = 카드 [2, 50] ps
      ③ save_fs(aimd_results) = msd.json 시간축 간격  ④ 프레임 수 = aimd_results n_frames = msd.json 점 수
      ⑤ 셀·원소가 프레임마다 같다 (NVT)
    ⛔ 어긋나면 {"error": …} — 잘린 궤적이나 다른 런의 궤적으로 D 를 내지 않는다.
    """
    import numpy as np
    run_dir = Path(run_dir)
    traj, side = run_dir / "traj.xyz", run_dir / "aimd_results.json"
    if not traj.exists():
        return {"error": "traj.xyz 없음 — 카드 정의의 MSD·사건 수를 못 낸다 (검사 불가 = 자격 없음)"}
    if not side.exists():
        return {"error": "aimd_results.json 없음 — save_fs·프레임 수를 교차확인할 수 없다"}
    try:
        meta = json.loads(side.read_text())
        save_fs, n_meta = float(meta["save_fs"]), int(meta["n_frames"])
    except (OSError, ValueError, KeyError, TypeError) as e:
        return {"error": f"aimd_results.json 을 못 읽는다 ({type(e).__name__})"}
    try:
        fw_ok = fit_window_ps is not None and [float(x) for x in fit_window_ps] == list(CARD_WINDOW_PS)
    except (TypeError, ValueError):
        fw_ok = False
    if not fw_ok:
        return {"error": f"msd.json 창 {fit_window_ps} ≠ 카드 {list(CARD_WINDOW_PS)} ps — 다른 프로토콜의 런"}
    if not times_ps or len(times_ps) < 2:
        return {"error": "msd.json 시간축이 비었다 — 교차확인 불가"}
    dt_fs = (float(times_ps[1]) - float(times_ps[0])) * 1000.0
    if abs(dt_fs - save_fs) > 1e-6 * max(1.0, save_fs):
        return {"error": f"save_fs 불일치 — aimd_results {save_fs:g} fs · msd.json 간격 {dt_fs:g} fs"}
    try:
        frames = (reader or _ase_read_all)(traj)
    except Exception as e:
        return {"error": f"traj.xyz 를 못 읽는다 ({type(e).__name__}: {e})"}
    if len(frames) != n_meta or len(frames) != len(times_ps):
        return {"error": f"프레임 수 불일치 — traj {len(frames)} · aimd_results {n_meta} · msd.json {len(times_ps)} "
                         "(잘렸거나 다른 런의 궤적)"}
    sym0, cell0 = frames[0].get_chemical_symbols(), np.array(frames[0].cell)
    for f in frames[1:]:
        if f.get_chemical_symbols() != sym0 or not np.allclose(np.array(f.cell), cell0, atol=1e-6):
            return {"error": "프레임마다 셀·원소가 같지 않다 — NVT 고정셀 궤적이 아니다"}
    spos = np.array([f.get_scaled_positions(wrap=True) for f in frames])
    return card_curve_arrays(spos, cell0, sym0, frames[0].get_masses(), save_fs)


def judge_runs_card(runs, ignore_eligibility=False, say=print, binding=None, alarm=False):
    """v6 — 런마다 **카드 정의 곡선**으로 자격 판정. msd.json 의 옛 D 는 `D_legacy_sto_lab` 으로만 남긴다.

    v7 본 라운드 (개정 CP · 2026-10-03 사용자 결정 '결속 + 경보 거부권'):
      binding = {"ladder": (T*,), "protocol": V7_PROTOCOL} 이면 곡선 **전에** 온도·길이·간격 결속을 건다.
      alarm = True 이면 자격 통과 런에 골격 경보 **거부권**을 건다 — 경보 통과는 골격 보존 인증이 아니다 (회신 CP P1).
    ⛔ v6 판독은 둘 다 끈 채(기본값)로 부른다 — 봉인된 v6 마감·판정을 그대로 재현한다 (회신 CP).
    """
    from msd_diffusive_check import aggregation_eligible, framework_alarm
    out, n = {}, len(runs)
    for i, (k, r) in enumerate(sorted(runs.items()), 1):
        be = protocol_binding_errors(r, **binding) if binding else []
        if be:
            cc = {"error": "프로토콜 결속 실패 — " + " · ".join(be)}
        else:
            cc = card_curve_from_run(Path(r["path"]).parent, r.get("t"), r.get("fit_window_ps"))
        fa = None
        if "error" in cc:
            ok, why, det = False, [f"⛔ 검사 불가 — {cc['error']}"], {"error": cc["error"]}
            D, t, y, ev = None, [], [], None
        else:
            ok, why, det = aggregation_eligible(cc["t"], cc["y"], cc["events"])
            why = list(why)
            if cc["D"] is None:
                ok = False
                why.append(cc["why_no_D"])
            if alarm and ok:
                try:
                    fa = (framework_alarm(str(Path(r["path"])), save_fs=cc["save_fs"]) or {}).get("state", "unavailable")
                except Exception as e:          # 못 재면 '경보 없음' 이 아니다
                    fa = f"unavailable ({type(e).__name__})"
                if fa not in ("ok", "framework_static"):
                    ok = False
                    why.append(f"⛔ 골격 경보 {fa} — 거부권 (경보 통과는 인증이 아니다 · 회신 CP P1)")
            D, t, y, ev = cc["D"], cc["t"], cc["y"], cc["events"]
        out[k] = {**r, "D": D, "t": t, "y": y, "events_per_run": ev, "D_legacy_sto_lab": r["D"], "framework_alarm": fa,
                  "card_curve": {kk: v for kk, v in cc.items() if kk not in ("t", "y")},
                  "eligible": bool(ok), "reasons": why, "detail": det, "used": bool(ok or ignore_eligibility),
                  "t_end_ps": (t[-1] if t else None)}
        say(f"  [{i:2d}/{n}] {r['tag']:22s} 프레임 {cc.get('n_frames', '—')} · Li {cc.get('n_Li', '—')} · "
            f"사건 {cc.get('events', '—')} · 자격 {'통과' if ok else '미달'}" + (f" · ⛔ {cc['error']}" if "error" in cc else ""))
    return out


def reason_tally(j):
    """기준별 미달 런 수 (한 런이 여럿에 걸릴 수 있다 — 겹침 있음). 판정에 안 쓰고 **보고만** 한다."""
    from msd_diffusive_check import NO_VALUE, SUB_RATIO_OK, EVENTS_MIN_PER_RUN
    c = {"검사불가": 0, "①_D_inc_plateau": 0, "②_부창_기울기비": 0, "③_사건수": 0}
    evs = []
    for r in j.values():
        det = r.get("detail") or {}
        if "error" in det:
            c["검사불가"] += 1
            continue
        if det.get("run_verdict") == NO_VALUE:
            c["①_D_inc_plateau"] += 1
        rs = det.get("sub_window_ratios")
        if rs is None or any(not (SUB_RATIO_OK[0] <= x <= SUB_RATIO_OK[1]) for x in rs):
            c["②_부창_기울기비"] += 1
        ev = det.get("events_per_run")
        if ev is None or ev < EVENTS_MIN_PER_RUN:
            c["③_사건수"] += 1
        if ev is not None:
            evs.append(ev)
    evs.sort()
    c["사건수_최소_중앙_최대"] = ([evs[0], evs[len(evs) // 2], evs[-1]] if evs else None)
    return c


def _git_state():
    """판독 도구의 커밋·더러움 — 카드가 '실행 시 git 해시를 기록' 하라고 했다."""
    import subprocess
    try:
        h = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=no"],
                               capture_output=True, text=True, timeout=20).stdout.strip()
        return {"commit": h or None, "dirty": bool(dirty)}
    except Exception as e:
        return {"commit": None, "dirty": None, "why": f"{type(e).__name__}"}


#: ── 카드 v7 탐침 (2026-10-01 · 초안 `cascade_estimand_card_v7_probe_2026_10_01.json`) ──────────────
#  무도핑 H0 만 돌려 **조건(온도)을 고른다** — 처방(P1/P2) 비교는 탐침에서 보지 않는다.
#  T* = 사다리에서 **가장 낮은** 온도 중, 지정 시드 **전부**가 v6 와 같은 자격(aggregation_eligible ·
#  카드 정의 곡선)을 통과하고 골격 경보(alarm)가 없는 온도. 사다리·시드·문턱은 카드가 정했다.
V7_LADDER_K = (800, 1000)
V7_SEEDS = (1, 2)
V7_PROBE_STRUCT = "H0_host"
#: 카드 v7 프로토콜 — 런의 사이드카(aimd_results.json)가 이 값과 같아야 한다 (`protocol_binding_errors`).
#: 회신 CP P0-1 (2026-10-03): 종전 탐침은 사이드카의 save_fs·프레임 수만 읽고 **T_K 를 안 봤다**
#: (msd.json 800 K · aimd_results 600 K 인 합성 런이 eligible=True).
#: 개정 CP (2026-10-03 · 사용자 결정 '생산 400 ps 로 늘림' · 회신 CP P0-2): 생산 200 → **400 ps**. 같은 10 % 기준·같은 창에서
#: 합성 브라운 null 탈락이 22 % → ≈1 % (`cascade_estimand_card_v7_probe_amendment_cp_2026_10_03.json` §2 · 실제 상관된 Li 의
#: 보정값은 아니다). dt 2 fs · save 100 fs 는 v6 그대로. 여기서 바꾸면 새 카드다.
V7_PROTOCOL = {"prod_ps": 400.0, "dt_fs": 2.0, "save_fs": 100.0}
#: 개정 CP (회신 CP P0-3 · 사용자 결정 '다음 사다리 온도로' · '제외 · 탐침 전용 시드'): H0 통과만으로 본 라운드를 열지 않는다.
#: **같은 온도에서** 대표 부모 1 개의 P1·P2 × 탐침 전용 속도 시드 2 = 4 런의 자격을 D 봉인으로 먼저 본다.
#: 부모 = C — random.Random(20261003).choice(C–J) · v5 에서 값이 나온 A·B 제외 · 결과 전 추첨 (개정 §3).
#: 탐침 시드 3·4 의 런은 최종 집계에서 **제외**한다 — 본 라운드는 시드 1·2 를 새로 돈다 (선택 효과를 집계에 안 들인다).
V7_PAIR_PARENT = "C"
V7_PAIR_SEEDS = (3, 4)
V7_MAIN_SEEDS = (1, 2)
#: 한 사다리 온도에서 볼 런 — H0 두 시드 → 대표 쌍 네 런. **전부** 자격 통과여야 그 온도가 T* 다.
V7_PROBE_PLAN = (("H0_host", 1), ("H0_host", 2),
                 (f"P1_Al2O3_{V7_PAIR_PARENT}", 3), (f"P2_Al2S3_{V7_PAIR_PARENT}", 3),
                 (f"P1_Al2O3_{V7_PAIR_PARENT}", 4), (f"P2_Al2S3_{V7_PAIR_PARENT}", 4))
_TAG_T = re.compile(r"__T(\d+)__s\d+$")


def _same(a, b, rel=1e-6):
    try:
        return abs(float(a) - float(b)) <= rel * max(1.0, abs(float(b)))
    except (TypeError, ValueError):
        return False


def protocol_binding_errors(r, ladder=V7_LADDER_K, protocol=V7_PROTOCOL, require_tag_T=True):
    """회신 CP P0-1 (2026-10-03) — 런 하나의 **온도·생산길이·시간간격**을 일곱 곳에서 결속한다.
    → 오류 문장 목록 (빈 목록 = 결속됨).

      ① msd.json T_K  ② aimd_results.json T_K  ③ 런 폴더 이름 `T<NNN>`  ④ 태그 `__T<NNN>__` (탐침 태그는 필수)
      ⑤ 요청 온도 = 사다리 안의 값  ⑥ 사이드카 prod_ps · dt_fs · save_fs = 카드 값
      ⑦ msd.json 시간축 끝 ≈ prod_ps (저장 간격 하나 안)
    ⛔ 키가 없거나 못 읽으면 '확인 못 함' 이지 통과가 아니다 → 오류로 돌린다.
    ⛔ 못 하는 것: 궤적이 **실제로** 그 온도로 돌았는지(md.log T[K])는 안 본다 — 기록끼리의 일치만 본다.
    """
    msd_path = Path(r["path"])
    run_dir = msd_path.parent
    try:
        md = json.loads(msd_path.read_text())
        T = float(md["T_K"])
    except (OSError, ValueError, KeyError, TypeError) as e:
        return [f"msd.json 의 T_K 를 못 읽는다 ({type(e).__name__}) — 온도를 결속할 수 없다"]
    try:
        side = json.loads((run_dir / "aimd_results.json").read_text())
        if not isinstance(side, dict):
            raise ValueError("not a dict")
    except (OSError, ValueError) as e:
        return [f"aimd_results.json 을 못 읽는다 ({type(e).__name__}) — 온도·길이를 결속할 수 없다"]
    errs = []
    if side.get("T_K") is None:
        errs.append("aimd_results.json 에 T_K 가 없다 — 사이드카 온도를 확인 못 함")
    elif not _same(side["T_K"], T):
        errs.append(f"T_K 불일치 — msd.json {T:g} K · aimd_results {side['T_K']} K")
    if run_dir.name != f"T{T:g}":
        errs.append(f"런 폴더 이름 '{run_dir.name}' ≠ T{T:g} — 다른 온도의 폴더")
    m = _TAG_T.search(str(r.get("tag") or ""))
    if m is None:
        if require_tag_T:
            errs.append(f"태그 '{r.get('tag')}' 에 __T<NNN>__ 가 없다 — 요청 온도를 확인 못 함")
    elif not _same(m.group(1), T):
        errs.append(f"태그 온도 {m.group(1)} K ≠ msd.json {T:g} K")
    if ladder is not None and not any(_same(T, x) for x in ladder):
        errs.append(f"온도 {T:g} K 가 요청 사다리 {list(ladder)} K 밖이다")
    for k in ("prod_ps", "dt_fs", "save_fs"):
        v = side.get(k)
        if v is None:
            errs.append(f"aimd_results.json 에 {k} 가 없다 — 카드 값과 대조 못 함")
        elif not _same(v, protocol[k]):
            errs.append(f"{k} {v} ≠ 카드 {protocol[k]:g}")
    ts = md.get("times_ps")
    if not ts:
        errs.append("msd.json 시간축이 없다 — 생산 길이를 확인 못 함")
    else:
        try:
            t_end = float(ts[-1])
            if abs(t_end - float(protocol["prod_ps"])) > float(protocol["save_fs"]) / 1000.0 + 1e-9:
                errs.append(f"msd.json 시간축 끝 {t_end:g} ps ≠ 생산 {float(protocol['prod_ps']):g} ps "
                            "(저장 간격 하나 안이어야 한다 — 잘렸거나 다른 길이)")
        except (TypeError, ValueError):
            errs.append("msd.json 시간축을 못 읽는다")
    return errs


#: 골격 경보의 역할 — 출력에 같이 싣는다 (회신 CP P1 · 2026-10-03).
FRAMEWORK_ALARM_ROLE = ("보조 지표 (거부권만) — 통과(ok·framework_static)는 골격 보존 인증이 아니다 · "
                        "첫↔마지막 프레임 비교라 중간 이동을 못 보고 n < 8 인 종은 판정에서 빠진다 (회신 CP P1)")


def probe_run(r, ladder=V7_LADDER_K, protocol=V7_PROTOCOL):
    """탐침 한 런 (scan() 기록) → 자격 · 모양 · 골격 경보. ⛔ **D 값은 돌려주지 않는다** — 탐침은 조건 선택용이다.

    회신 CP P0-1 (2026-10-03): 궤적을 읽기 **전에** 온도·생산길이·시간간격을 결속한다
    (`protocol_binding_errors`). 하나라도 어긋나면 자격 없음 — 곡선을 계산하지 않는다.
    """
    from msd_diffusive_check import aggregation_eligible, framework_alarm
    run_dir = Path(r["path"]).parent
    out = {"tag": r.get("tag"), "run_dir": str(run_dir)}
    be = protocol_binding_errors(r, ladder=ladder, protocol=protocol)
    if be:
        return {**out, "eligible": False, "error": "프로토콜 결속 실패 — " + " · ".join(be), "binding_errors": be}
    cc = card_curve_from_run(run_dir, r.get("t"), r.get("fit_window_ps"))
    if "error" in cc:
        return {**out, "eligible": False, "error": cc["error"]}
    ok, why, det = aggregation_eligible(cc["t"], cc["y"], cc["events"])
    try:
        fa = (framework_alarm(str(Path(r["path"])), save_fs=cc["save_fs"]) or {}).get("state", "unavailable")
    except Exception as e:                      # 경보를 못 재면 '경보 없음' 이 아니다
        fa = f"unavailable ({type(e).__name__})"
    #: 골격 경보는 **잰 결과가 ok·framework_static 일 때만** 통과 — 못 쟀으면(unavailable) 통과가 아니다
    return {**out, "eligible": bool(ok) and fa in ("ok", "framework_static"), "aggregation_eligible": bool(ok),
            "framework_alarm": fa, "framework_alarm_role": FRAMEWORK_ALARM_ROLE, "run_verdict": det.get("run_verdict"),
            "sub_window_ratios": det.get("sub_window_ratios"), "events": cc["events"],
            "n_frames": cc["n_frames"], "reasons": list(why)}


def select_probe_temperature(results, ladder=V7_LADDER_K, plan=V7_PROBE_PLAN):
    """{(T, 구조, 시드): probe 결과} → (T* 또는 None, 사유, 다음에 돌릴 (T, 구조, 시드) 또는 None).

    개정 CP (2026-10-03 · 사용자 결정): 한 사다리 온도에서 `plan` (H0 두 시드 → 대표 쌍 네 런) 이 **전부** 자격 통과여야 T* 다.
    · 그 온도에서 돌린 계획 런이 **하나라도 불통과**면 그 온도는 탈락 → 다음 사다리 (부모를 바꾸지 않는다)
    · 돌린 런이 전부 통과인데 **안 돌린 계획 런이 남았으면** 멈추고 plan 순서의 첫 빈칸을 다음으로 지정한다
      (일부 통과로 T* 를 정하지 않는다 · 더 높은 온도로 건너뛰지 않는다)
    · 계획 밖의 런(다른 부모 · 다른 시드)은 세지 않는다 — 대체 금지
    · 사다리 전부 탈락 → v7 을 열지 않는다
    """
    for T in ladder:
        done = {(st, sd): results[(T, st, sd)] for st, sd in plan if (T, st, sd) in results}
        if any(not d.get("eligible") for d in done.values()):
            continue
        left = [(st, sd) for st, sd in plan if (st, sd) not in done]
        if left:
            st, sd = left[0]
            return None, f"{T} K: 계획 {len(plan)} 런 중 {len(done)} 런 통과 · 남은 {len(left)} — 전부 통과해야 T* 다", (T, st, sd)
        return T, (f"{T} K: H0 두 시드 · 대표 쌍(부모 {V7_PAIR_PARENT} · 시드 {list(V7_PAIR_SEEDS)}) 네 런 전부 자격 통과 · "
                   f"골격 경보 없음 → T* = {T} K"), None
    return None, f"사다리 {list(ladder)} K 전부 불통과 — v7 본 라운드를 열지 않는다", None


def main_probe(a) -> int:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    plan = set(V7_PROBE_PLAN)
    allr = scan(a.probe)
    runs = {k: v for k, v in allr.items() if (k[0], k[2]) in plan}
    off = sorted(k for k in allr if (k[0], k[2]) not in plan)
    print(f"v7 탐침 (개정 CP) · 사다리 {list(V7_LADDER_K)} K · 계획 {len(V7_PROBE_PLAN)} 런/온도 (H0 시드 {list(V7_SEEDS)} → "
          f"부모 {V7_PAIR_PARENT} 쌍 시드 {list(V7_PAIR_SEEDS)}) · 프로토콜 {V7_PROTOCOL} · 런 {len(runs)} 개 · {a.probe}")
    if off:
        print(f"  ⚠ 계획 밖 런 {len(off)} 개 — 판정에 안 쓴다 (대체 금지): {off[:6]}")
    res = {}
    for (st, T, sd), r in sorted(runs.items()):
        pr = probe_run(r); res[(T, st, sd)] = pr
        print(f"  {T} K {st} seed {sd}: 자격 {'통과' if pr['eligible'] else '미달'} · 골격 {pr.get('framework_alarm', '—')} · "
              f"부창비 {[round(x, 2) for x in (pr.get('sub_window_ratios') or [])]} · 사건 {pr.get('events', '—')}"
              + (f" · ⛔ {pr['error']}" if "error" in pr else ""))
    T_star, why, nxt = select_probe_temperature(res)
    print(f"→ {why}" + (f" · 다음: {nxt[0]} K {nxt[1]} seed {nxt[2]}" if nxt else ""))
    q = Path(a.out_json or Path(a.probe) / "cascade_v7_probe.json")
    q.write_text(json.dumps({"card": "db/properties/cascade_estimand_card_v7_probe_2026_10_01.json",
                             "amendment": "db/properties/cascade_estimand_card_v7_probe_amendment_cp_2026_10_03.json",
                             "ladder_K": list(V7_LADDER_K), "seeds": list(V7_SEEDS), "protocol": V7_PROTOCOL,
                             "pair_parent": V7_PAIR_PARENT, "pair_seeds": list(V7_PAIR_SEEDS),
                             "plan": [list(x) for x in V7_PROBE_PLAN], "off_plan_runs": [list(x) for x in off],
                             "binding": "온도(msd·aimd·폴더·태그·사다리)·prod_ps·dt_fs·save_fs·시간축 끝 결속 (회신 CP P0-1)",
                             "T_star_K": T_star,
                             "why": why, "next": nxt, "tool": _git_state(),
                             "⛔": "D 값은 싣지 않는다 — 탐침은 조건 선택용이다",
                             "runs": [{"T_K": T, "structure": st, "seed": sd, **pr} for (T, st, sd), pr in sorted(res.items())]},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {q}")
    return 0


def judge_runs(runs, ignore_eligibility=False):
    """런마다 자격 판정. → {key: {...}}  ⛔ events_per_run=None 은 **통과가 아니다**."""
    from msd_diffusive_check import aggregation_eligible
    out = {}
    for k, r in runs.items():
        ev = count_events(Path(r["path"]).parent)
        ok, why, det = aggregation_eligible(r["t"], r["y"], ev)
        out[k] = {**r, "events_per_run": ev, "eligible": bool(ok),
                  "reasons": why, "detail": det,
                  "used": bool(ok or ignore_eligibility)}
    return out


def dbar(j, struct, T):
    """시드 2 산술평균. **시드 하나라도 빠지면 None** (카드 §2 결측 규칙 — 대체 금지)."""
    vs = []
    for sd in SEEDS:
        r = j.get((struct, T, sd))
        if r is None or not r["used"] or not (r["D"] > 0) or not math.isfinite(r["D"]):
            return None
        vs.append(r["D"])
    return sum(vs) / len(vs)


def ea_mev(j, struct):
    """6 점 겉보기 아레니우스 기울기 → Ea [meV]. 한 점이라도 빠지면 None."""
    xs, ys = [], []
    for T in TEMPS:
        for sd in SEEDS:
            r = j.get((struct, T, sd))
            if r is None or not r["used"] or not (r["D"] > 0):
                return None
            xs.append(1.0 / T); ys.append(math.log(r["D"]))
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx <= 0:
        return None
    return -(sxy / sxx) * KB_EV * 1000.0


def verdict_interval(lo, hi, delta):
    """카드 §2-5 — 판정은 **구간의 위치**로 3 갈래."""
    if lo > delta or hi < -delta:
        return "실질_차이_지지"
    if -delta <= lo and hi <= delta:
        return "실질_동등_지지"
    return "미결"


def aggregate(j):
    """카드 §2 집계식. → dict. 유효 부모가 2 미만이면 **구간 판정을 만들지 않는다**."""
    res = {"primary": {"T_K": PRIMARY_T, "delta_lnD": round(DELTA_LND, 6)}, "parents": {}}
    Ls = {}
    for k, (p1, p2) in PAIRS.items():
        d1, d2 = dbar(j, p1, PRIMARY_T), dbar(j, p2, PRIMARY_T)
        row = {"D_bar_P1": d1, "D_bar_P2": d2}
        if d1 and d2:
            row["R"] = d1 / d2; row["lnR"] = math.log(row["R"]); Ls[k] = row["lnR"]
        else:
            row["⛔"] = "결측 — 비율·로그를 만들지 않는다 (카드 §2 결측 규칙)"
        res["parents"][k] = row
    if len(Ls) == 2:
        a, b = Ls["A"], Ls["B"]
        Lb, se = (a + b) / 2, abs(a - b) / 2
        lo, hi = Lb - T_DF1 * se, Lb + T_DF1 * se
        res["primary"].update({
            "L_bar": Lb, "SE": se, "ci_ln": [lo, hi],
            "ratio": math.exp(Lb), "ci_ratio": [math.exp(lo), math.exp(hi)],
            "verdict": verdict_interval(lo, hi, DELTA_LND),
            "⚠_부호": ("두 부모의 부호가 **반대**다" if a * b < 0 else "두 부모 부호 일치")})
    else:
        res["primary"]["⛔"] = (f"유효 부모 {len(Ls)} — A/B 평균·df 1 구간 판정 없음 "
                               f"(카드 §2 실패_전파_규칙 4항)")
    # 2차 ΔEa
    ea, a_k = {}, {}
    for k, (p1, p2) in PAIRS.items():
        e1, e2 = ea_mev(j, p1), ea_mev(j, p2)
        ea[k] = {"Ea_P1_meV": e1, "Ea_P2_meV": e2}
        if e1 is not None and e2 is not None:
            a_k[k] = e1 - e2; ea[k]["a_meV"] = a_k[k]
    res["secondary"] = {"delta_Ea_meV": DELTA_EA_MEV, "per_parent": ea}
    if len(a_k) == 2:
        aa, bb = a_k["A"], a_k["B"]
        ab, sea = (aa + bb) / 2, abs(aa - bb) / 2
        lo, hi = ab - T_DF1 * sea, ab + T_DF1 * sea
        res["secondary"].update({
            "a_bar_meV": ab, "SE_meV": sea, "ci_meV": [lo, hi],
            "verdict": verdict_interval(lo, hi, DELTA_EA_MEV),
            "⚠_부호": ("두 부모의 부호가 **반대**다" if aa * bb < 0 else "두 부모 부호 일치")})
    else:
        res["secondary"]["⛔"] = "두 부모의 ΔEa 가 **모두** 유효해야 한다 (카드 §2 2차)"
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="E′ 파일럿 판정 (카드 v5.2 §2)")
    ap.add_argument("--out_root", default=str(Path.home() / "work/runs/eprime_pilot"))
    ap.add_argument("--out_json", default=None)
    ap.add_argument("--ignore_eligibility", action="store_true",
                    help="⛔ 자격 게이트를 무시하고 집계한다. **인용 금지** — "
                         "'배선을 고쳐 다시 돌리면 결론이 바뀌나' 만 보는 가정 계산이다")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--card", choices=["v5.2", "v6", "v7"], default="v5.2",
                    help="v6 = 부모 10 · 600 K · t(n−1) 일반형 (카드 v6 §4) · v7 = T* (탐침 산출물) · 결속 + 골격 경보 거부권")
    ap.add_argument("--probe_json", default=None, help="v7: 탐침 산출물 cascade_v7_probe.json — T* 는 여기서만 온다")
    ap.add_argument("--allow_partial", action="store_true", help="⛔ v6: 40 런이 다 없어도 집계 (중간 집계 — 인용·판정 금지 표시)")
    ap.add_argument("--probe", metavar="OUT_ROOT", default=None,
                    help="카드 v7 탐침 판정 — H0 런의 자격·모양·골격 경보와 T* 선택 (D 값 안 찍음)")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.probe:
        return main_probe(a)
    if a.card == "v6":
        return main_v6(a)
    if a.card == "v7":
        return main_v7(a)

    runs = scan(a.out_root)
    print(f"런 {len(runs)} 개 · out_root {a.out_root}")
    if not runs:
        print("⛔ msd.json 을 하나도 못 찾았다 — 경로를 확인할 것"); return 2
    j = judge_runs(runs, ignore_eligibility=a.ignore_eligibility)
    ok = sum(1 for r in j.values() if r["eligible"])
    print(f"자격 통과 {ok}/{len(j)}" + ("  ⛔ **자격 무시 모드**" if a.ignore_eligibility else ""))
    noev = [k for k, r in j.items() if r["events_per_run"] is None]
    if noev:
        print(f"  ⛔ 사건 수를 못 센 런 {len(noev)} 개 — 궤적이 없다 (--save_traj 미사용). "
              f"None 은 통과가 아니라 **검사 불가**다")
    res = aggregate(j)
    res["⚠_부피_조건"] = f"V = {V_COMMON_A3} Å³ · P̄ = **결측** (msd.json 에 없다 — 카드 §2 요구사항 미충족)"
    res["⚠_인용정책"] = "1저자 2026-09-18 — σ·D·Ea 전부 **계 간 상대차로만**. 절대값 인용 금지"
    res["eligibility"] = {"n_runs": len(j), "n_eligible": ok,
                          "ignore_eligibility": bool(a.ignore_eligibility),
                          "n_events_uncountable": len(noev)}
    p = res["primary"]
    if "ratio" in p:
        print(f"\n1차 D_rel(P1/P2; 600 K) — A {res['parents']['A'].get('R'):.3f} · "
              f"B {res['parents']['B'].get('R'):.3f}")
        print(f"  대표 {p['ratio']:.3f} · 95 % 구간 [{p['ci_ratio'][0]:.4f}, {p['ci_ratio'][1]:.1f}]"
              f" · **{p['verdict']}**  ({p['⚠_부호']})")
    else:
        print(f"\n1차: {p['⛔']}")
    s = res["secondary"]
    if "a_bar_meV" in s:
        print(f"2차 ΔEa — A {res['secondary']['per_parent']['A']['a_meV']:+.1f} · "
              f"B {res['secondary']['per_parent']['B']['a_meV']:+.1f} meV")
        print(f"  ā {s['a_bar_meV']:+.1f} · 구간 [{s['ci_meV'][0]:+.0f}, {s['ci_meV'][1]:+.0f}] meV"
              f" · **{s['verdict']}**  ({s['⚠_부호']})")
    else:
        print(f"2차: {s['⛔']}")
    q = a.out_json or os.path.join(a.out_root, "eprime_judgement.json")
    res["rows"] = [{"structure": k[0], "T_K": k[1], "seed": k[2], "D": r["D"],
                    "eligible": r["eligible"], "events_per_run": r["events_per_run"],
                    "t_end_ps": r["t_end_ps"], "reasons": r["reasons"]}
                   for k, r in sorted(j.items())]
    Path(q).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {q}")
    if a.ignore_eligibility:
        print("⛔ 이 산출물은 **인용 금지**다 (자격 게이트를 무시했다)")
    return 0


def v7_main_runs(runs_all, T):
    """본 라운드 판정 대상 = T* 의 **시드 1·2** 런만. 탐침 전용 시드(3·4) 런은 집계에서 뺀다 (개정 CP · 사용자 결정 '제외').
    → (대상 {키: 기록}, 제외한 탐침 시드 런 키 목록)."""
    runs = {k: v for k, v in runs_all.items() if _same(k[1], T) and k[2] in V7_MAIN_SEEDS}
    probe_only = sorted(k for k in runs_all if k[2] in V7_PAIR_SEEDS)
    return runs, probe_only


def v7_probe_t_star(probe_json):
    """탐침 산출물(cascade_v7_probe.json) → (T*, 사유). T* 는 **여기서만** 온다 — 자유 인자로 받지 않는다.
    프로토콜·대표 부모가 이 판독기와 다르면 거부 (다른 카드의 탐침)."""
    try:
        pj = json.loads(Path(probe_json).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as e:
        return None, f"탐침 산출물을 못 읽는다 ({type(e).__name__})"
    T = pj.get("T_star_K")
    if T is None or not any(_same(T, x) for x in V7_LADDER_K):
        return None, f"탐침이 T* 를 정하지 않았다 ({pj.get('why')})"
    if pj.get("protocol") != V7_PROTOCOL or pj.get("pair_parent") != V7_PAIR_PARENT:
        return None, (f"탐침 산출물의 프로토콜·대표 부모({pj.get('protocol')} · {pj.get('pair_parent')})가 "
                      f"이 판독기({V7_PROTOCOL} · {V7_PAIR_PARENT})와 다르다 — 다른 카드의 탐침")
    return int(round(float(T))), pj.get("why")


#: 회신 CP Q-CP-4 권장 문구 (그대로) + P0-3 한계 — v7 판정 산출물에 같이 싣는다.
V7_CLAIM_SCOPE = ("사전 지정된 탐침 규칙으로 선택한 T* K에서, UMA·공통 고정셀·준비 및 자격 조건 아래의 P1/P2 확산 비를 평가했다. "
                  "등가영역 내 판정은 이 조건에 한정하며, 600 K·작동 온도·실제 재료의 동등성을 뜻하지 않는다. "
                  "결론은 전체 배열이 아니라 **자격 통과 집합에 조건부**다 (회신 CP P0-3). "
                  "T* 는 '확산이 시작되는 최저 온도' 가 아니라 지정 사다리·시드에서 운영 기준을 통과한 온도다.")


def main_v7(a) -> int:
    """카드 v7 + 개정 CP — 본 라운드 판정 (부모 10 × 처방 2 × 시드 1·2 = 40 런 · T* · 결속 + 경보 거부권 · v6 §4 집계)."""
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    if not a.probe_json:
        print("⛔ --probe_json (탐침 산출물 cascade_v7_probe.json) 이 없다 — T* 를 자유 인자로 받지 않는다")
        return 2
    T, why = v7_probe_t_star(a.probe_json)
    if T is None:
        print(f"⛔ {why} — 본 라운드를 판정하지 않는다")
        return 4
    pairs = load_v6_pairs()
    runs, probe_only = v7_main_runs(scan(a.out_root), T)
    print(f"카드 v7 + 개정 CP · T* = {T} K (탐침: {why}) · 부모 {len(pairs)} · 시드 {list(V7_MAIN_SEEDS)} · 런 {len(runs)} 개 · "
          f"프로토콜 {V7_PROTOCOL} · out_root {a.out_root}")
    if probe_only:
        print(f"  탐침 전용 시드 런 {len(probe_only)} 개 — 집계에서 제외 (개정 CP · 선택 효과)")
    miss = missing_runs(runs, pairs, T=T, seeds=V7_MAIN_SEEDS)
    if miss:
        print(f"⛔ 있어야 할 런 {len(miss)} 개의 msd.json 이 없다 — 카드 §4: 40 런을 다 채우기 전에 집계하지 않는다")
        for m in miss[:12]:
            print(f"    없음: {m[0]}__T{m[1]}__s{m[2]}")
        if not a.allow_partial:
            return 3
        print("  ⛔ --allow_partial — 아래는 **중간 집계**다. 인용·판정에 쓰지 않는다")
    want = {(st, T, sd) for k in pairs for st in pairs[k] for sd in V7_MAIN_SEEDS}
    jj = judge_runs_card({k: v for k, v in runs.items() if k in want}, ignore_eligibility=a.ignore_eligibility,
                         binding={"ladder": (T,), "protocol": V7_PROTOCOL}, alarm=True)
    ok = sum(1 for r in jj.values() if r["eligible"])
    tally = reason_tally(jj)
    print(f"판정 대상 런 {len(jj)} · 자격 통과 {ok}" + ("  ⛔ **자격 무시 모드**" if a.ignore_eligibility else ""))
    res = aggregate_n(jj, pairs, T=T)
    res["card"] = ("db/properties/cascade_estimand_card_v7_probe_2026_10_01.json + "
                   "db/properties/cascade_estimand_card_v7_probe_amendment_cp_2026_10_03.json (집계 = v6 §4)")
    res["T_star_K"], res["protocol"], res["probe_json"] = T, V7_PROTOCOL, str(a.probe_json)
    res["claim_scope"] = V7_CLAIM_SCOPE
    res["excluded_probe_seed_runs"] = [list(k) for k in probe_only]
    res["tool"] = _git_state()
    res["⚠_인용정책"] = "1저자 2026-09-18 — 계 간 상대차로만. 절대 D 인용 금지 · UMA·표집·부피·T* 조건부"
    res["eligibility"] = {"n_runs": len(jj), "n_eligible": ok, "ignore_eligibility": bool(a.ignore_eligibility),
                          "partial": bool(miss), "reason_tally": tally,
                          "binding": "온도(msd·aimd·폴더·태그·T*)·prod·dt·save·시간축 끝", "framework_alarm": "거부권만"}
    res["rows"] = [{"structure": k[0], "T_K": k[1], "seed": k[2], "tag": r["tag"], "D": r["D"], "eligible": r["eligible"],
                    "framework_alarm": r.get("framework_alarm"), "events_per_run": r["events_per_run"],
                    "reasons": r["reasons"]} for k, r in sorted(jj.items())]
    p = res["primary"]
    print(f"1차: {p.get('verdict', p.get('⛔'))}")
    q = a.out_json or os.path.join(a.out_root, "cascade_v7_judgement.json")
    Path(q).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {q}")
    if a.ignore_eligibility or miss:
        print("⛔ 이 산출물은 **인용 금지**다 (자격 무시 또는 중간 집계)")
    return 0


def main_v6(a) -> int:
    try:
        sys.stdout.reconfigure(line_buffering=True)     # 파일로 보내도 진행 줄이 바로 보이게 (2026-10-01: 30 초 동안 빈 로그)
    except Exception:
        pass
    pairs = load_v6_pairs()
    runs = scan(a.out_root)
    print(f"카드 v6 · 부모 {len(pairs)} ({''.join(sorted(pairs))}) · 600 K · 런 {len(runs)} 개 · out_root {a.out_root}")
    miss = missing_runs(runs, pairs)
    if miss:
        print(f"⛔ 있어야 할 런 {len(miss)} 개의 msd.json 이 없다 — 카드 §4: n=10 을 다 채우기 전에 집계하지 않는다")
        for m in miss[:12]:
            print(f"    없음: {m[0]}__s{m[2]} (T {m[1]})")
        if not a.allow_partial:
            return 3
        print("  ⛔ --allow_partial — 아래는 **중간 집계**다. 인용·판정에 쓰지 않는다")
    want = {(st, PRIMARY_T, sd) for k in pairs for st in pairs[k] for sd in SEEDS}
    print("MSD·D·사건 수 = 궤적에서 카드 정의대로 (골격 COM 제거 · 시간원점 평균 · 2–50 ps 자유절편)")
    jj = judge_runs_card({k: v for k, v in runs.items() if k in want}, ignore_eligibility=a.ignore_eligibility)
    ok = sum(1 for r in jj.values() if r["eligible"])
    noev = [k for k, r in jj.items() if r["events_per_run"] is None]
    tally = reason_tally(jj)
    print(f"판정 대상 런 {len(jj)} · 자격 통과 {ok}" + ("  ⛔ **자격 무시 모드**" if a.ignore_eligibility else "")
          + (f" · 검사 불가 {len(noev)} (궤적·교차확인 = 자격 없음)" if noev else ""))
    print(f"  기준별 미달 (겹침 있음): ① D_inc plateau {tally['①_D_inc_plateau']} · ② 부창 기울기비 {tally['②_부창_기울기비']}"
          f" · ③ 사건 수 {tally['③_사건수']} · 검사 불가 {tally['검사불가']} · 사건 수 최소/중앙/최대 {tally['사건수_최소_중앙_최대']}")
    res = aggregate_n(jj, pairs)
    res["card"] = "db/properties/cascade_estimand_card_v6_10parents_2026_09_19.json §4"
    res["msd_definition"] = ("카드 v4 §2 (v5 '그대로' · v6 §3 승계): 분수좌표 unwrap → 실공간 → 비-Li 골격 COM(질량 가중) 제거 → "
                             "시간원점 평균 · 창 2–50 ps 자유절편 · D = 기울기/6 · 사건 = 같은 좌표에서 |Δr| > 2.5 Å 첫 발생 (t_ref 갱신)")
    res["⚠_판독_이력"] = ("2026-10-01 첫 판독(commit a9e123ab5)은 msd.json 의 옛 곡선(단일 시간원점 · 실험실 좌표 · 골격 COM 미제거)을 "
                       "읽었다 — 카드 정의와 다르다. 그 판독은 자격 0/40 · D 값 표시 없이 끝났다. 이 판독은 카드 정의로 고친 판이다. "
                       "rows 의 D_legacy_sto_lab 은 그 옛 값이다 (감사용 · 집계에 안 쓴다).")
    res["tool"] = _git_state()
    res["⚠_부피_조건"] = f"V = {V_COMMON_A3} Å³ · P̄ = **결측** (msd.json 에 없다)"
    res["⚠_인용정책"] = "1저자 2026-09-18 — 계 간 상대차로만. 절대 D 인용 금지 · UMA·표집·부피 조건부 (카드 1a)"
    res["eligibility"] = {"n_runs": len(jj), "n_eligible": ok, "ignore_eligibility": bool(a.ignore_eligibility),
                          "n_uncheckable": len(noev), "partial": bool(miss), "reason_tally": tally}
    print(f"\n{'부모':4s}{'D̄_P1':>12s}{'D̄_P2':>12s}{'L_k = ln R':>12s}")
    for k, r in res["parents"].items():
        print(f"  {k:2s}{(r['D_bar_P1'] or float('nan')):12.3e}{(r['D_bar_P2'] or float('nan')):12.3e}"
              + (f"{r['lnR']:12.4f}" if "lnR" in r else "        결측"))
    p = res["primary"]
    if "ratio" in p:
        print(f"\n1차 D_rel(P1/P2; 600 K) — n {p['n_valid']}/{p['n_parents_declared']} · L̄ {p['L_bar']:+.4f} · sd {p['sd']:.4f} · "
              f"t({p['df']}) {p['t']} · 95 % [{p['ci_ln'][0]:+.4f}, {p['ci_ln'][1]:+.4f}] (δ ±{DELTA_LND:.4f})")
        print(f"  비율 {p['ratio']:.3f} [{p['ci_ratio'][0]:.3f}, {p['ci_ratio'][1]:.3f}] · **{p['verdict']}** · {p['sign_count']}")
    else:
        print(f"\n1차: {p['⛔']}")
    res["rows"] = [{"structure": k[0], "T_K": k[1], "seed": k[2], "tag": r["tag"], "D": r["D"],
                    "D_legacy_sto_lab": r["D_legacy_sto_lab"], "eligible": r["eligible"],
                    "events_per_run": r["events_per_run"], "t_end_ps": r["t_end_ps"], "reasons": r["reasons"],
                    "detail": {kk: v for kk, v in (r.get("detail") or {}).items() if kk != "⛔"},
                    "card_curve": r.get("card_curve")}
                   for k, r in sorted(jj.items())]
    q = a.out_json or os.path.join(a.out_root, "cascade_v6_judgement.json")
    Path(q).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {q}")
    if a.ignore_eligibility or miss:
        print("⛔ 이 산출물은 **인용 금지**다 (자격 무시 또는 중간 집계)")
    return 0


def _selftest() -> int:
    ok = True
    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m); ok = ok and bool(c)

    chk(parse_tag("P1_Al2O3_A__s1") == ("P1_Al2O3_A", 1), "태그를 (구조, 시드) 로 읽는다")
    chk(parse_tag("H0_host__T600__s1") == ("H0_host", 1),
        "속도시험 태그(__T600__)도 같은 구조·시드로 읽는다")
    chk(parse_tag("garbage") == (None, None), "⛔음성: 모르는 태그는 **None** 이다 (추측하지 않는다)")

    #: 구간 판정 — 위치로만 가른다
    chk(verdict_interval(0.5, 0.9, DELTA_LND) == "실질_차이_지지", "구간 전체가 +δ 위 → 차이 지지")
    chk(verdict_interval(-0.9, -0.5, DELTA_LND) == "실질_차이_지지", "구간 전체가 −δ 아래 → 차이 지지")
    chk(verdict_interval(-0.2, 0.2, DELTA_LND) == "실질_동등_지지", "구간이 등가영역 안 → 동등 지지")
    chk(verdict_interval(-0.2, 0.9, DELTA_LND) == "미결",
        "⛔음성: 걸치면 **미결** — '효과 없음' 으로 읽지 않는다")
    chk(verdict_interval(-5.0, 5.0, DELTA_LND) == "미결", "⛔음성: 아주 넓은 구간도 미결이다")

    def mk(D, used=True):
        return {"D": D, "used": used, "t": [], "y": []}
    base = {}
    for st, d in (("P1_Al2O3_A", 2.5e-6), ("P2_Al2S3_A", 3.6e-6),
                  ("P1_Al2O3_B", 4.2e-6), ("P2_Al2S3_B", 3.0e-6)):
        for T in TEMPS:
            for sd in SEEDS:
                base[(st, T, sd)] = mk(d * (1 + 0.3 * (T - 600) / 200))
    r = aggregate(base)
    chk("ratio" in r["primary"], "[양성] 네 계가 다 있으면 1차 집계가 난다")
    chk(abs(r["parents"]["A"]["R"] - 2.5 / 3.6) < 1e-9,
        f"R_A = D̄_P1/D̄_P2 (기대 {2.5/3.6:.4f}, 실제 {r['parents']['A']['R']:.4f})")
    chk(abs(r["primary"]["ratio"] - math.exp((math.log(2.5/3.6) + math.log(4.2/3.0)) / 2)) < 1e-9,
        "대표 비율은 **기하평균**이다 (산술평균 아님)")
    chk(r["primary"]["⚠_부호"].startswith("두 부모의 부호가 **반대**"),
        f"부모 부호 반대를 집어낸다 ({r['primary']['⚠_부호']})")

    #: ⛔음성 — 시드 하나가 빠지면 그 (p,k) 는 **결측**이고 생존 시드로 대체하지 않는다
    b2 = dict(base); b2[("P1_Al2O3_A", 600, 2)] = mk(2.5e-6, used=False)
    r2 = aggregate(b2)
    chk(r2["parents"]["A"].get("R") is None and "⛔" in r2["parents"]["A"],
        f"⛔음성: 시드 하나 실패 → 그 부모 **결측** ({r2['parents']['A'].get('⛔','')[:30]})")
    chk("ratio" not in r2["primary"] and "⛔" in r2["primary"],
        "⛔음성: 유효 부모가 하나면 **구간 판정을 만들지 않는다**")
    chk("a_bar_meV" not in r2["secondary"],
        "⛔음성: 두 부모의 ΔEa 가 모두 유효해야 2차가 난다")

    #: ⛔음성 — D ≤ 0 은 로그를 만들지 않는다
    b3 = dict(base); b3[("P2_Al2S3_A", 600, 1)] = mk(-1e-9)
    chk(aggregate(b3)["parents"]["A"].get("R") is None,
        "⛔음성: D ≤ 0 이면 비율을 만들지 않는다 (작은 양수로 대체 금지)")

    #: ⛔음성 — 사건 수 None 은 **0 이 아니다**
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        chk(count_events(td) is None,
            "⛔음성: 궤적이 없으면 사건 수가 **None** 이다 (0 이 아니다 — 통과로 읽히면 안 된다)")

    #: Ea 부호 — D 가 T 와 같이 커지면 Ea 는 **양수**다
    flat = {}
    for T in TEMPS:
        for sd in SEEDS:
            flat[("X", T, sd)] = mk(1e-6 * math.exp(-0.25 / (KB_EV * T)) / math.exp(-0.25 / (KB_EV * 600)))
    e = ea_mev(flat, "X")
    chk(e is not None and abs(e - 250.0) < 1.0, f"Ea 를 meV 로 되돌린다 (기대 250, 실제 {e:.1f})")

    #: ── 카드 v6 (부모 n 일반형) ──
    chk(T975[1] == T_DF1 and T975[9] == 2.262 and T975[8] == 2.306, "t 표: df 1 = 12.706 (v5.2 와 같다) · df 9 = 2.262 · df 8 = 2.306")
    pv6 = load_v6_pairs()
    chk(len(pv6) == 10 and sorted(pv6) == list("ABCDEFGHIJ") and pv6["C"] == ("P1_Al2O3_C", "P2_Al2S3_C"),
        f"원장에서 부모 10 개 (A–J) · 이름 규칙 확인 ({sorted(pv6)})")
    import tempfile as _tf
    with _tf.TemporaryDirectory() as td6:
        bad = json.load(open(V6_PARENTS, encoding="utf-8")); bad["4_parents"][2]["P1_xyz"] = "db/structures/cascade_pilot/P1_Al2O3_Z.xyz"
        bp = Path(td6) / "bad_parents.json"; bp.write_text(json.dumps(bad), encoding="utf-8")
        try:
            load_v6_pairs(bp); rej = False
        except SystemExit:
            rej = True
        chk(rej, "⛔음성: 원장의 구조 파일 이름이 규칙과 어긋나면 부모 목록을 거부한다 (조용히 엉뚱한 런을 짝짓지 않는다)")
    Lk = {k: v for k, v in zip("ABCDEFGHIJ", (0.10, -0.20, 0.30, 0.05, -0.10, 0.25, 0.00, 0.15, -0.05, 0.20))}
    j6 = {}
    for k, L in Lk.items():
        for sd in SEEDS:
            j6[(f"P1_Al2O3_{k}", 600, sd)] = mk(1e-6 * math.exp(L))
            j6[(f"P2_Al2S3_{k}", 600, sd)] = mk(1e-6)
    r6 = aggregate_n(j6, pv6)
    v = list(Lk.values()); m = sum(v) / 10; sdv = math.sqrt(sum((x - m) ** 2 for x in v) / 9)
    chk(abs(r6["primary"]["L_bar"] - m) < 1e-9 and abs(r6["primary"]["sd"] - sdv) < 1e-9,
        f"L̄ = 평균 · sd = **표본** sd (n−1) — {r6['primary']['L_bar']:.4f} · {r6['primary']['sd']:.4f}")
    lo_x, hi_x = m - 2.262 * sdv / math.sqrt(10), m + 2.262 * sdv / math.sqrt(10)
    chk(abs(r6["primary"]["ci_ln"][0] - lo_x) < 1e-9 and abs(r6["primary"]["ci_ln"][1] - hi_x) < 1e-9 and r6["primary"]["df"] == 9,
        f"구간 = L̄ ± t(9)·sd/√10 = [{lo_x:+.4f}, {hi_x:+.4f}]")
    chk(r6["primary"]["verdict"] == verdict_interval(lo_x, hi_x, DELTA_LND) == "실질_동등_지지", f"판정 = 구간 위치 ({r6['primary']['verdict']})")
    j6b = dict(j6); j6b[("P1_Al2O3_D", 600, 2)] = mk(1e-6, used=False)
    r6b = aggregate_n(j6b, pv6)
    chk(r6b["primary"]["n_valid"] == 9 and r6b["primary"]["t"] == 2.306 and "⛔" in r6b["parents"]["D"],
        "⛔음성: 시드 하나 실패 → 그 부모 결측 · n 9 · t(8) (대체 안 함)")
    one = {k: j6[k] for k in j6 if k[0].endswith("_A")}
    chk("ratio" not in aggregate_n(one, pv6)["primary"], "⛔음성: 유효 부모 1 개면 구간 판정을 안 만든다")
    have = {k: {} for k in j6}; del have[("P2_Al2S3_J", 600, 1)]
    chk(missing_runs(have, pv6) == [("P2_Al2S3_J", 600, 1)] and missing_runs({k: {} for k in j6}, pv6) == [],
        "⛔음성: msd.json 없는 런을 찾아낸다 (n=10 다 채우기 전 집계 금지 게이트) · 다 있으면 빈 목록")

    #: ── v6 카드 정의 곡선 (궤적에서 · 2026-10-01) ──
    #   합성 궤적: 골격 전체가 **결정적으로 흐르고**(프레임당 Å), Li 는 그 위에서 자기 확산을 한다.
    #   카드 정의(골격 COM 제거)면 D = Li 자기 확산의 D 다. 실험실 좌표로 재면 흐름이 D 를 부풀린다.
    import numpy as np
    from msd_diffusive_check import lin_fit as _lf, NO_VALUE as _NV
    rng = np.random.default_rng(7)
    nT, nfw, nli, sf = 501, 32, 48, 200.0                   # 200 fs × 500 = 100 ps → 시간원점 lag 50 ps 까지
    cell = np.array([[20.0, 0.0, 0.0], [1.5, 19.0, 0.0], [0.8, 0.6, 10.0]])    # 기울어진 셀 — 분수좌표 unwrap 경로
    sym = ["S"] * nfw + ["Li"] * nli
    mass = [32.06] * nfw + [6.94] * nli
    drift = np.outer(np.arange(nT), [0.05, -0.03, 0.02])
    site_fw, site_li = rng.uniform(0, 1, (nfw, 3)) @ cell, rng.uniform(0, 1, (nli, 3)) @ cell
    own = np.cumsum(rng.normal(0, 0.12, (nT, nli, 3)), axis=0)
    cart = np.concatenate([site_fw[None] + drift[:, None, :] + rng.normal(0, 0.02, (nT, nfw, 3)),
                           site_li[None] + own + drift[:, None, :]], axis=1)
    spos = cart @ np.linalg.inv(cell)
    cc = card_curve_arrays(spos, cell, sym, mass, sf)
    to, yo, _ = _msd_multi_origin()(own, sf / 1000.0)
    d_own = _lf(to, yo, *CARD_WINDOW_PS)[0] / 6.0 * 1e-4
    tl, yl, _ = _msd_multi_origin()(cart[:, nfw:], sf / 1000.0)
    d_lab = _lf(tl, yl, *CARD_WINDOW_PS)[0] / 6.0 * 1e-4
    chk("error" not in cc and cc["D"] is not None and abs(cc["D"] / d_own - 1) < 0.01,
        f"카드 정의 D = 골격 기준 Li 자기 확산의 D (흐름 제거 · {cc.get('D', float('nan')):.3e} vs {d_own:.3e})")
    chk(d_lab > 3 * cc["D"], f"⛔음성: 실험실 좌표(COM 미제거)로 재면 흐름이 D 를 부풀린다 ({d_lab / cc['D']:.0f} 배) — 첫 v6 판독이 잰 쪽")
    chk(cc["t"][-1] >= CARD_WINDOW_PS[1] and cc["n_Li"] == nli and cc["n_framework"] == nfw and cc["n_frames"] == nT,
        f"시간원점 곡선이 창 끝({CARD_WINDOW_PS[1]} ps)에 닿는다 · Li {cc['n_Li']} · 골격 {cc['n_framework']} · 프레임 {cc['n_frames']}")
    ccw = card_curve_arrays(spos % 1.0, cell, sym, mass, sf)
    chk("error" not in ccw and abs(ccw["D"] / cc["D"] - 1) < 1e-9 and ccw["events"] == cc["events"],
        "⛔음성: 셀 안으로 감긴 좌표를 줘도 D·사건 수가 같다 (분수좌표 최소상 unwrap)"
        + (f" — ✗ {ccw['error']}" if "error" in ccw else ""))

    #   사건 수: Li 4 개가 프레임 30·70 에서 x 로 3.0 Å 씩 뛴다 + 골격 흐름 프레임당 0.08 Å (100 프레임 = 8 Å).
    #   골격 기준이면 정확히 8 · 실험실 좌표면 흐름만으로 2.5 Å 를 넘어 더 센다.
    nT2 = 101
    flow = np.outer(np.arange(nT2), [0.08, 0.0, 0.0])[:, None, :]
    li2 = np.repeat(site_li[None, :4], nT2, axis=0) + flow
    li2[30:, :, 0] += 3.0
    li2[70:, :, 0] += 3.0
    cart2 = np.concatenate([np.repeat(site_fw[None], nT2, axis=0) + flow, li2], axis=1)
    cc2 = card_curve_arrays(cart2 @ np.linalg.inv(cell), cell, ["S"] * nfw + ["Li"] * 4, [32.06] * nfw + [6.94] * 4, sf)
    lab_ev, p0 = 0, li2[0].copy()
    for k in range(1, nT2):
        hit = np.linalg.norm(li2[k] - p0, axis=1) > EVENT_D_HOP_A
        lab_ev += int(hit.sum()); p0[hit] = li2[k][hit]
    chk(cc2.get("events") == 8 and lab_ev != 8,
        f"사건 = 골격 기준 2.5 Å 첫 발생 · t_ref 갱신 → 정확히 8 (실험실 좌표면 {lab_ev} — 흐름을 사건으로 센다)")
    chk(cc2.get("D") is None and "why_no_D" in cc2,
        "⛔음성: 궤적이 20 ps 뿐이면 창 2–50 ps 를 못 맞춘다 → D = None (잘린 창의 값을 내지 않는다)")
    bad = cart2 @ np.linalg.inv(cell)
    bad[50:, nfw, 2] += 0.45
    chk("unwrap" in card_curve_arrays(bad, cell, ["S"] * nfw + ["Li"] * 4, [32.06] * nfw + [6.94] * 4, sf).get("error", ""),
        "⛔음성: 한 프레임에 셀의 45 % 를 가는 원자가 있으면 unwrap 이 모호하다 → 계산 거부")
    chk("error" in card_curve_arrays(spos, cell, ["S"] * (nfw + nli), mass, sf),
        "⛔음성: Li 가 없으면 거부 (0 이 아니다)")
    #   질량 가중: 무거운 Cl 8 개만 흐르고 가벼운 O 8 개는 서 있다. Li 는 **질량중심**의 흐름을 정확히 따라간다
    #   → 골격 COM 기준으로는 Li 가 안 움직인다 (MSD 0 · 사건 0). 원자수 평균(centroid)이면 남는다.
    v_h = np.array([0.06, 0.0, 0.0])
    m_cl, m_o = 35.45, 15.999
    com_v = 8 * m_cl * v_h / (8 * m_cl + 8 * m_o)
    tt = np.arange(nT2)[:, None, None]
    cart3 = np.concatenate([site_fw[None, :8] + tt * v_h, np.repeat(site_fw[None, 8:16], nT2, axis=0),
                            site_li[None, :4] + tt * com_v], axis=1)
    cc3 = card_curve_arrays(cart3 @ np.linalg.inv(cell), cell, ["Cl"] * 8 + ["O"] * 8 + ["Li"] * 4,
                            [m_cl] * 8 + [m_o] * 8 + [6.94] * 4, sf)
    chk(max(cc3["y"]) < 1e-8 and cc3["events"] == 0,
        f"골격 기준점은 **질량**중심이다 (원자수 평균 아님) — Li 가 COM 을 따라가면 MSD {max(cc3['y']):.1e} · 사건 {cc3['events']}")

    #   읽기 경로 교차확인 — ase 로 진짜 extxyz 를 쓰고 읽는다. ase 가 없으면 **실패**다 (안 잰 것은 통과가 아니다).
    try:
        from ase import Atoms
        from ase.io import write as awrite
        have_ase = True
    except ImportError:
        have_ase = False
    chk(have_ase, "읽기 경로 시험에 ase 가 있다 (없으면 이 시험은 실패로 친다)")
    if have_ase:
        with _tf.TemporaryDirectory() as tdr:
            rd = Path(tdr) / "run"; rd.mkdir()
            awrite(str(rd / "traj.xyz"), [Atoms(symbols=sym, positions=cart[i], cell=cell, pbc=True) for i in range(nT)])
            tps = [i * sf / 1000.0 for i in range(nT)]

            def side(n=nT, s=sf):
                (rd / "aimd_results.json").write_text(json.dumps({"save_fs": s, "n_frames": n}))
            side()
            cr = card_curve_from_run(rd, tps, [2.0, 50.0])
            chk("error" not in cr and abs(cr["D"] / cc["D"] - 1) < 1e-5 and cr["events"] == cc["events"],
                f"traj.xyz → 같은 D·사건 수 (배열 경로와 일치 · {cr.get('error', 'ok')})")
            side(n=nT - 1)
            chk("프레임 수" in card_curve_from_run(rd, tps, [2.0, 50.0]).get("error", ""),
                "⛔음성: aimd_results 프레임 수 ≠ 궤적 → 거부 (잘린 궤적)")
            side()
            chk("save_fs" in card_curve_from_run(rd, [i * 0.1 for i in range(nT)], [2.0, 50.0]).get("error", ""),
                "⛔음성: msd.json 시간 간격 ≠ save_fs → 거부")
            chk("창" in card_curve_from_run(rd, tps, [2.0, 40.0]).get("error", ""),
                "⛔음성: msd.json 창 ≠ 카드 2–50 ps → 거부 (다른 프로토콜의 런)")
            chk("프레임 수" in card_curve_from_run(rd, tps[:-1], [2.0, 50.0]).get("error", ""),
                "⛔음성: msd.json 점 수 ≠ 궤적 프레임 수 → 거부 (다른 런의 궤적)")
            (rd / "aimd_results.json").unlink()
            chk("aimd_results" in card_curve_from_run(rd, tps, [2.0, 50.0]).get("error", ""),
                "⛔음성: aimd_results.json 이 없으면 거부 (save_fs 를 가정하지 않는다)")
            side()
            nd = Path(tdr) / "none"; nd.mkdir()
            runs_t = {("P1_Al2O3_A", 600, 1): {"path": str(rd / "msd.json"), "tag": "P1_Al2O3_A__s1", "D": 9.9e-6,
                                               "t": tps, "fit_window_ps": [2.0, 50.0]},
                      ("P1_Al2O3_A", 600, 2): {"path": str(nd / "msd.json"), "tag": "P1_Al2O3_A__s2", "D": 9.9e-6,
                                               "t": tps, "fit_window_ps": [2.0, 50.0]}}
            jr = judge_runs_card(runs_t, say=lambda s: None)
            g, nn = jr[("P1_Al2O3_A", 600, 1)], jr[("P1_Al2O3_A", 600, 2)]
            chk(g["D"] is not None and abs(g["D"] / cc["D"] - 1) < 1e-5 and g["D_legacy_sto_lab"] == 9.9e-6,
                "집계 D 는 카드 정의 값이다 — msd.json 의 옛 D 는 D_legacy_sto_lab 으로만 남는다")
            chk(nn["D"] is None and not nn["eligible"] and not nn["used"] and nn["reasons"][0].startswith("⛔ 검사 불가"),
                "⛔음성: 궤적 없는 런 → D 없음 · 자격 없음 · 집계 제외 (msd.json 값으로 대체하지 않는다)")
            tl_ = reason_tally(jr)
            chk(tl_["검사불가"] == 1 and dbar(jr, "P1_Al2O3_A", 600) is None,
                f"⛔음성: 시드 하나가 검사 불가면 그 (p,k) 결측 · 집계표 검사불가 {tl_['검사불가']}")
            chk(g["detail"].get("run_verdict") in (_NV, "hold", "citable") and g["events_per_run"] == cc["events"],
                "자격 판정이 카드 곡선·골격 기준 사건 수로 돈다")
    #: ── 카드 v7 탐침 선택 규칙 (2026-10-01) · 개정 CP (2026-10-03): 온도마다 H0 두 시드 + 대표 쌍 네 런 · 사다리 결속 ──
    P, F = {"eligible": True}, {"eligible": False}
    PC1, PC2 = f"P1_Al2O3_{V7_PAIR_PARENT}", f"P2_Al2S3_{V7_PAIR_PARENT}"

    def allp(T, bad=None):
        return {(T, st, sd): (F if (st, sd) == bad else P) for st, sd in V7_PROBE_PLAN}
    chk(select_probe_temperature(allp(800))[0] == 800, "800 K 계획 6 런 전부 통과 → T* = 800")
    t, _, nx = select_probe_temperature({(800, "H0_host", 1): P, (800, "H0_host", 2): P})
    chk(t is None and nx == (800, PC1, 3), "⛔음성(개정 CP): H0 두 시드 통과만으로 T* 를 정하지 않는다 → 다음 = 대표 쌍")
    t, _, nx = select_probe_temperature({(800, "H0_host", 1): P})
    chk(t is None and nx == (800, "H0_host", 2), "⛔음성: H0 한 시드만 통과 → 다음 = 800 K H0 seed 2")
    t, _, nx = select_probe_temperature(allp(800, bad=(PC2, 4)))
    chk(t is None and nx == (1000, "H0_host", 1), "⛔음성: 대표 쌍 한 런 불통과 → 800 탈락 · 다음 = 1000 K H0 seed 1 (부모 그대로)")
    chk(select_probe_temperature({**allp(800, bad=("H0_host", 1)), **allp(1000)})[0] == 1000,
        "800 K 불통과 → 1000 K 계획 6 런 전부 통과 → T* = 1000")
    t, why, nx = select_probe_temperature({**allp(800, bad=(PC1, 3)), **allp(1000, bad=("H0_host", 2))})
    chk(t is None and nx is None and "열지 않는다" in why, "⛔음성: 사다리 전부 불통과 → v7 을 열지 않는다")
    t, _, nx = select_probe_temperature(allp(1000))
    chk(t is None and nx == (800, "H0_host", 1), "⛔음성: 800 K 를 안 돌렸으면 1000 K 결과가 있어도 건너뛰지 않는다")
    sub = {k: v for k, v in allp(800).items() if not (k[1] == PC1 and k[2] == 3)}
    sub[(800, "P1_Al2O3_D", 3)] = P
    t, _, nx = select_probe_temperature(sub)
    chk(t is None and nx == (800, PC1, 3), "⛔음성: 다른 부모(D)의 런은 계획 런을 대신하지 못한다 (부모 교체 금지)")
    sub2 = {k: v for k, v in allp(800).items() if k[2] != 4}
    sub2.update({(800, PC1, 1): P, (800, PC2, 1): P})
    t, _, nx = select_probe_temperature(sub2)
    chk(t is None and nx == (800, PC1, 4), "⛔음성: 본 라운드 시드(1)의 런은 탐침 시드(4)를 대신하지 못한다")
    import random as _rnd
    chk(_rnd.Random(20261003).choice(list("CDEFGHIJ")) == V7_PAIR_PARENT,
        f"대표 부모 = 개정 §3 의 결정론적 추첨 재현 (random.Random(20261003).choice(C–J) = {V7_PAIR_PARENT})")
    chk(V7_PROTOCOL["prod_ps"] == 400.0 and set(V7_PAIR_SEEDS).isdisjoint(V7_MAIN_SEEDS),
        "개정 CP 상수 — 생산 400 ps · 탐침 시드와 본 라운드 시드가 겹치지 않는다")
    ra = {("P1_Al2O3_A", 800, 1): {}, ("P1_Al2O3_A", 800, 2): {}, ("P1_Al2O3_C", 800, 3): {}, ("P1_Al2O3_A", 1000, 1): {}}
    rv, po = v7_main_runs(ra, 800)
    chk(set(rv) == {("P1_Al2O3_A", 800, 1), ("P1_Al2O3_A", 800, 2)} and po == [("P1_Al2O3_C", 800, 3)],
        "⛔음성: 본 라운드 대상 = T* 의 시드 1·2 뿐 · 탐침 시드 3 은 제외 목록 · 다른 온도 런도 안 든다")
    with _tf.TemporaryDirectory() as tdj:
        pjf = Path(tdj) / "cascade_v7_probe.json"

        def wpj(**kw):
            b_ = {"T_star_K": 800, "why": "x", "protocol": V7_PROTOCOL, "pair_parent": V7_PAIR_PARENT}
            b_.update(kw)
            pjf.write_text(json.dumps(b_))
        wpj()
        chk(v7_probe_t_star(pjf)[0] == 800, "본 라운드 T* 는 탐침 산출물에서 읽는다 (800)")
        wpj(T_star_K=None)
        chk(v7_probe_t_star(pjf)[0] is None, "⛔음성: 탐침이 T* 를 못 정했으면 본 라운드 판정 거부")
        wpj(T_star_K=600)
        chk(v7_probe_t_star(pjf)[0] is None, "⛔음성: 사다리 밖 T* (600 K) → 거부")
        wpj(protocol={**V7_PROTOCOL, "prod_ps": 200.0})
        chk(v7_probe_t_star(pjf)[0] is None, "⛔음성: 200 ps 프로토콜로 돈 탐침 → 거부 (개정 전 카드)")
        wpj(pair_parent="D")
        chk(v7_probe_t_star(pjf)[0] is None, "⛔음성: 대표 부모가 다른 탐침 → 거부")
        chk(v7_probe_t_star(Path(tdj) / "none.json")[0] is None, "⛔음성: 탐침 산출물이 없으면 거부")
    import types as _ty
    chk(main_v7(_ty.SimpleNamespace(probe_json=None)) == 2,
        "⛔음성: --probe_json 없이 v7 본 라운드 판정 → 거부 (T* 를 자유 인자로 안 받는다)")
    if have_ase:
        with _tf.TemporaryDirectory() as tdp:
            rd = Path(tdp) / "md" / "H0_host__T800__s1" / "eprime_H0_host_d0.00_c0" / "T800"; rd.mkdir(parents=True)
            awrite(str(rd / "traj.xyz"), [Atoms(symbols=sym, positions=cart[i], cell=cell, pbc=True) for i in range(nT)])
            #: 시험 궤적은 200 fs × 500 = 100 ps 라 카드 프로토콜(200 ps · 100 fs) 대신 **같은 모양의 시험 프로토콜**로 결속한다
            proto_t = {"prod_ps": (nT - 1) * sf / 1000.0, "dt_fs": 2.0, "save_fs": sf}
            sc_ok = {"T_K": 800, "save_fs": sf, "n_frames": nT, "prod_ps": proto_t["prod_ps"], "dt_fs": 2.0}
            (rd / "aimd_results.json").write_text(json.dumps(sc_ok))
            (rd / "msd.json").write_text(json.dumps({"T_K": 800, "D_Li_cm2_s": 1.23e-5, "fit_window_ps": [2.0, 50.0],
                                                     "times_ps": [i * sf / 1000.0 for i in range(nT)], "msd_Li_A2": [0.0] * nT}))
            rr = scan(tdp)
            chk(list(rr) == [("H0_host", 800, 1)], f"탐침 런을 (H0_host, 800, 1) 로 읽는다 ({list(rr)})")
            pr = probe_run(rr[("H0_host", 800, 1)], protocol=proto_t)
            flat = json.dumps(pr)
            chk("error" not in pr and "D" not in pr and "1.23e-05" not in flat and "D_legacy_sto_lab" not in pr,
                "⛔음성: 탐침 출력에 D 값이 없다 (msd.json 의 D 도 안 옮긴다)")
            chk(isinstance(pr.get("eligible"), bool) and pr.get("framework_alarm") is not None,
                f"탐침 런 = 자격 판정 + 골격 경보 상태 ({pr.get('framework_alarm')})")
            import msd_diffusive_check as _mdc
            _oa, _of = _mdc.aggregation_eligible, _mdc.framework_alarm
            r0 = rr[("H0_host", 800, 1)]
            try:      # 자격은 통과로 고정하고 골격 경보 경로만 따로 본다
                _mdc.aggregation_eligible = lambda t, y, ev: (True, [], {"run_verdict": "citable", "sub_window_ratios": [1, 1, 1]})
                _mdc.framework_alarm = lambda *a_, **k_: {"state": "ok"}
                p_ok = probe_run(r0, protocol=proto_t)
                chk(p_ok["eligible"] is True, "자격 통과 + 골격 ok → 탐침 통과")
                chk("인증이 아니다" in p_ok.get("framework_alarm_role", ""),
                    "골격 경보 역할이 출력에 같이 실린다 — 통과는 골격 보존 인증이 아니다 (회신 CP P1)")
                _mdc.framework_alarm = lambda *a_, **k_: {"state": "alarm"}
                chk(probe_run(r0, protocol=proto_t)["eligible"] is False, "⛔음성: 골격 경보(alarm) → 자격 통과여도 탐침 불통과")
                def _boom(*a_, **k_):
                    raise RuntimeError("x")
                _mdc.framework_alarm = _boom
                pz = probe_run(r0, protocol=proto_t)
                chk(pz["eligible"] is False and str(pz["framework_alarm"]).startswith("unavailable"),
                    "⛔음성: 골격 경보를 못 재면 통과가 아니다 (unavailable)")
                #: ── 회신 CP P0-1 (2026-10-03) — 자격·경보를 **통과로 고정한 채** 기록 하나만 깨서 막히는지 본다 ──
                _mdc.framework_alarm = lambda *a_, **k_: {"state": "ok"}
                (rd / "aimd_results.json").write_text(json.dumps({**sc_ok, "T_K": 600}))
                pc = probe_run(r0, protocol=proto_t)
                chk(pc["eligible"] is False and "T_K 불일치" in pc.get("error", "") and pc.get("binding_errors"),
                    "⛔음성(회신 CP 반례 재현): msd.json 800 K · aimd_results 600 K → 자격 통과여도 탐침 불통과")
                (rd / "aimd_results.json").write_text(json.dumps(sc_ok))
                chk(probe_run(r0, protocol=proto_t)["eligible"] is True, "되돌리면 다시 통과 (깬 것만 막혔다)")
                chk(probe_run(r0)["eligible"] is False and "prod_ps" in probe_run(r0).get("error", ""),
                    "⛔음성: 카드 프로토콜(400 ps · 100 fs)로 보면 100 ps 시험 런은 결속 실패")
                #: ── 개정 CP — v7 본 라운드 경로: judge_runs_card(binding, alarm) · v6 기본값은 그대로 ──
                bnd = {"ladder": (800,), "protocol": proto_t}
                kk = ("H0_host", 800, 1)
                _mdc.framework_alarm = lambda *a_, **k_: {"state": "ok"}
                j_ok = judge_runs_card({kk: dict(r0)}, say=lambda s_: None, binding=bnd, alarm=True)[kk]
                chk(j_ok["eligible"] is True and j_ok["framework_alarm"] == "ok",
                    "[양성] 본 라운드 경로 — 결속 맞고 자격·경보 통과 → 자격 통과")
                _mdc.framework_alarm = lambda *a_, **k_: {"state": "alarm"}
                j_al = judge_runs_card({kk: dict(r0)}, say=lambda s_: None, binding=bnd, alarm=True)[kk]
                chk(j_al["eligible"] is False and any("골격 경보" in w for w in j_al["reasons"]),
                    "⛔음성: 본 라운드에서 골격 경보 → 자격 없음 (거부권)")
                j_v6 = judge_runs_card({kk: dict(r0)}, say=lambda s_: None)[kk]
                chk(j_v6["eligible"] is True and j_v6["framework_alarm"] is None,
                    "v6 경로(기본값)는 결속·경보를 안 건다 — 봉인된 v6 판정 그대로")
                (rd / "aimd_results.json").write_text(json.dumps({**sc_ok, "T_K": 600}))
                j_b = judge_runs_card({kk: dict(r0)}, say=lambda s_: None, binding=bnd, alarm=True)[kk]
                chk(j_b["eligible"] is False and "결속" in j_b["reasons"][0],
                    "⛔음성(회신 CP 반례 · 본 라운드 경로): 사이드카 600 K → 자격 없음")
                (rd / "aimd_results.json").write_text(json.dumps(sc_ok))
            finally:
                _mdc.aggregation_eligible, _mdc.framework_alarm = _oa, _of

            def mkrun(folder, tag, T_msd=800, n=nT, msd_T=True, **side_kw):
                d_ = Path(tdp) / "bind" / tag / folder
                d_.mkdir(parents=True, exist_ok=True)
                sc = {k_: v_ for k_, v_ in {**sc_ok, **side_kw}.items() if v_ is not None}
                (d_ / "aimd_results.json").write_text(json.dumps(sc))
                mj = {"fit_window_ps": [2.0, 50.0], "times_ps": [i * sf / 1000.0 for i in range(n)]}
                if msd_T:
                    mj["T_K"] = T_msd
                (d_ / "msd.json").write_text(json.dumps(mj))
                return {"path": str(d_ / "msd.json"), "tag": tag, "t": mj["times_ps"], "fit_window_ps": [2.0, 50.0]}

            def be(rec, **kw):
                return " | ".join(protocol_binding_errors(rec, protocol=proto_t, **kw))
            TG = "H0_host__T800__s1"
            chk(be(mkrun("T800", TG)) == "", "[양성] 기록 일곱 곳이 다 맞으면 결속 오류 0")
            chk("T_K 가 없다" in be(mkrun("T800", TG, T_K=None)), "⛔음성: 사이드카에 T_K 가 없으면 확인 못 함 = 오류")
            chk("T_K 를 못 읽는다" in be(mkrun("T800", TG, msd_T=False)), "⛔음성: msd.json 에 T_K 가 없으면 오류")
            chk("prod_ps" in be(mkrun("T800", TG, prod_ps=50.0)), "⛔음성: 사이드카 생산 길이 ≠ 카드 → 오류")
            chk("dt_fs" in be(mkrun("T800", TG, dt_fs=1.0)), "⛔음성: 사이드카 dt ≠ 카드 → 오류")
            chk("save_fs" in be(mkrun("T800", TG, save_fs=100.0)), "⛔음성: 사이드카 저장 간격 ≠ 카드 → 오류")
            chk("폴더" in be(mkrun("T600", TG)), "⛔음성: 폴더 이름 T600 · msd.json 800 K → 오류 (다른 온도의 폴더)")
            chk("태그 온도" in be(mkrun("T800", "H0_host__T1000__s1")), "⛔음성: 태그 __T1000__ · msd.json 800 K → 오류")
            chk("__T<NNN>__ 가 없다" in be(mkrun("T800", "H0_host__s1")), "⛔음성: 탐침 태그에 온도가 없으면 요청 온도를 확인 못 함")
            chk("사다리" in be(mkrun("T800", TG), ladder=(1000,)), "⛔음성: 요청 사다리 밖의 온도 → 오류")
            chk("시간축 끝" in be(mkrun("T800", TG, n=251)), "⛔음성: msd.json 시간축이 생산 길이보다 짧다 → 오류 (잘린 런)")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
