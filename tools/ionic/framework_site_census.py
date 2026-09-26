#!/usr/bin/env python3
"""framework_site_census.py — C6 골격 게이트의 판정 근거: **원자별 자리 이탈 census** (개정안 §2).

왜 (회신 BL Q3)
  `--framework` 의 β 는 시간창 안의 곡선 모양이라 유계 운동(진동·회전)도 β≈0.45 를 낸다.
  `--framework_com` 의 골격 평균 MSD 는 소수 원자의 이동을 감춘다 (O 9개만 4 Å 움직여도 0.46 Å²).
  둘 다 "원자가 자리를 떠났나" 의 증거가 못 된다 → 원자 하나하나를 **직접 센다**.

규칙 (db/properties/lpsocl_box331_closure_amendment_2026_09_11.json §2 · 결과 보기 전 고정)
  · P 결합 음이온: frame 0 에서 최근접 P 거리가 O ≤ 2.0 / S ≤ 2.6 Å 인 O·S.
    이탈 = **그 P** 와의 거리(MIC)가 O > 2.5 / S > 3.0 Å 를 **≥ 10 ps 연속** 유지.
    회전·진동은 P 에 붙은 채라 잡히지 않는다. 다른 P 로 옮겨 붙어도 원래 P 에서 멀어지므로 잡힌다.
  · 자유 음이온(P 에 안 붙은 S · Cl)과 P: frame 0 위치 대비 변위(골격 전체 평균 병진 제거, unwrap)가
    > 2.0 Å 를 ≥ 10 ps 연속 유지.
  · 런 판정: 이벤트 ≥ 1 → `framework_mobile`, 0 → `framework_rigid`. 원소별 이벤트·원자·시작 시각을 남긴다.

⛔ 이 도구가 못 하는 것
  · Li 는 보지 않는다 — Li 는 확산하는 것이 정상이다.
  · 왜 움직였는지(회전·재배열·확산)를 가르지 않는다 — 자리를 떠났는가만 센다.
  · β 를 계산하지 않고 β 경보를 지우지도 않는다 — 경보는 결과 파일에 보존된다.
  · 문턱을 정하지 않는다 — `--card` 에서 읽는다. 없으면 기본값을 쓰되 화면에 경고를 찍는다.
  · 셀이 변하는 궤적(NPT)은 unwrap 이 frame-0 셀을 쓰므로 정확하지 않다 — NVT 전용. 셀이 변하면 멈춘다.
  · 이탈 문턱 바로 아래(예: O 2.4 Å 유지)는 잡지 않는다 — 그래서 원자별 **최대 지표**를 같이 찍어 여유를 보인다.

  python3 tools/ionic/framework_site_census.py --traj .../T600/traj.xyz --out .../T600/site_census.json \
      --card db/properties/lpsocl_box331_closure_amendment_2026_09_11.json
  python3 tools/ionic/framework_site_census.py --selftest
"""
from __future__ import annotations
import argparse, json, math, os, pathlib, sys, tempfile
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aimd_jump_stats import read_traj, unwrap      # 같은 extxyz 리더 · 같은 unwrap (규약을 복제하지 않는다)

DEFAULTS = {"o_bond_A": 2.0, "s_bond_A": 2.6, "o_escape_A": 2.5, "s_escape_A": 3.0,
            "disp_escape_A": 2.0, "min_ps": 10.0}


def read_thresholds(card):
    d = json.loads(pathlib.Path(card).read_text(encoding="utf-8"))
    m = d["2_C6_분류기_감사_정의_결과_보기_전_고정"]["문턱_기계값"]
    return {k: float(m[k]) for k in DEFAULTS}


def mic_series(d, cells):
    """(T,3) 또는 (T,n,3) 차분에 프레임별 최소상 규약."""
    cinv = np.linalg.inv(cells)                                   # (T,3,3)
    f = np.einsum("t...i,tij->t...j", d, cinv)
    f -= np.round(f)
    return np.einsum("t...j,tji->t...i", f, cells)


def sustained_runs(mask, min_frames):
    """bool 배열에서 길이 ≥ min_frames 인 True 연속 구간 → [(start, length)]."""
    runs, n, i = [], len(mask), 0
    while i < n:
        if mask[i]:
            j = i
            while j < n and mask[j]:
                j += 1
            if j - i >= min_frames:
                runs.append((i, j - i))
            i = j
        else:
            i += 1
    return runs


def census(sym, pos, cells, dt_ps, th=DEFAULTS):
    sym = np.asarray(sym); pos = np.asarray(pos, float); cells = np.asarray(cells, float)
    T, N, _ = pos.shape
    if np.abs(cells - cells[0]).max() > 1e-6:
        raise SystemExit("⛔ 셀이 프레임마다 다르다 — 이 도구는 NVT(고정 셀) 전용이다. 멈춘다.")
    min_frames = max(1, int(round(th["min_ps"] / dt_ps)))
    fw = np.where(sym != "Li")[0]
    P = np.where(sym == "P")[0]
    events, peak = [], {}
    # ── (1) P 결합 음이온: 자기 P 와의 거리 ───────────────────────────────
    bonded = {}
    for a in np.where((sym == "O") | (sym == "S"))[0]:
        if len(P) == 0:
            break
        d0 = np.linalg.norm(mic_series((pos[0, P] - pos[0, a])[None], cells[:1])[0], axis=1)
        k = int(np.argmin(d0))
        bond = th["o_bond_A"] if sym[a] == "O" else th["s_bond_A"]
        if d0[k] <= bond:
            bonded[int(a)] = int(P[k])
    for a, p in bonded.items():
        d = np.linalg.norm(mic_series(pos[:, p] - pos[:, a], cells), axis=1)
        esc = th["o_escape_A"] if sym[a] == "O" else th["s_escape_A"]
        peak[a] = {"elem": str(sym[a]), "kind": "P-bonded", "P": p, "max_dP_A": float(d.max()), "escape_A": esc}
        for s, L in sustained_runs(d > esc, min_frames):
            events.append({"kind": "P-bonded", "elem": str(sym[a]), "atom": a, "P": p,
                           "start_ps": s * dt_ps, "length_ps": L * dt_ps, "peak_dP_A": float(d[s:s + L].max())})
    # ── (2) 자유 음이온·P: 골격 평균 병진 제거 후 변위 ──────────────────────
    free = [int(i) for i in fw if int(i) not in bonded and sym[i] in ("S", "Cl", "P", "O")]
    uw = unwrap(pos[:, fw], cells[0])                             # (T, n_fw, 3)
    disp = uw - uw[0]
    disp = disp - disp.mean(axis=1, keepdims=True)                # 골격 전체 평균 병진 제거
    idx = {int(i): j for j, i in enumerate(fw)}
    for a in free:
        m = np.linalg.norm(disp[:, idx[a]], axis=1)
        peak[a] = {"elem": str(sym[a]), "kind": "free", "max_disp_A": float(m.max()), "escape_A": th["disp_escape_A"]}
        for s, L in sustained_runs(m > th["disp_escape_A"], min_frames):
            events.append({"kind": "free", "elem": str(sym[a]), "atom": a,
                           "start_ps": s * dt_ps, "length_ps": L * dt_ps, "peak_disp_A": float(m[s:s + L].max())})
    by_elem = {}
    for e in events:
        by_elem.setdefault(e["elem"], {"events": 0, "atoms": set()})
        by_elem[e["elem"]]["events"] += 1; by_elem[e["elem"]]["atoms"].add(e["atom"])
    by_elem = {k: {"events": v["events"], "n_atoms": len(v["atoms"]), "atoms": sorted(v["atoms"])} for k, v in by_elem.items()}
    # 원소별 최대 지표 (이벤트 0 이라도 문턱까지 얼마나 갔나)
    margin = {}
    for a, q in peak.items():
        key = f"{q['elem']}/{q['kind']}"
        val = q.get("max_dP_A", q.get("max_disp_A"))
        if key not in margin or val > margin[key]["max_A"]:
            margin[key] = {"max_A": float(val), "escape_A": q["escape_A"], "atom": a}
    return {
        "n_frames": int(T), "dt_ps": dt_ps, "total_ps": T * dt_ps, "min_frames": min_frames,
        "thresholds": dict(th),
        "n_framework": int(len(fw)), "n_P_bonded_anions": len(bonded), "n_free": len(free),
        "verdict": "framework_mobile" if events else "framework_rigid",
        "n_events": len(events), "by_elem": by_elem, "events": events,
        "margin_max_by_elem_kind": margin,
        "⛔": "이 판정은 '자리를 떠났나' 만 본다. β 경보는 지우지 않는다 — 결과 파일에 병기한다.",
    }


def census_file(traj, dt_ps=None, th=DEFAULTS):
    sym, pos, cells = read_traj(traj)
    if dt_ps is None:
        side = pathlib.Path(traj).parent / "aimd_results.json"
        if side.is_file():
            dt_ps = float(json.loads(side.read_text())["save_fs"]) / 1000.0
        else:
            raise SystemExit("⛔ dt 를 모른다 — aimd_results.json 이 없으면 --dt_ps 를 주어라.")
    return census(sym, pos, cells, dt_ps, th)


# ── selftest: 합성 궤적 ──────────────────────────────────────────────────
def _base(T=600):
    L = 12.0
    sym = np.array(["P", "O", "S", "S", "S", "S", "Cl", "Li", "Li"])
    p0 = np.array([[6, 6, 6], [7.5, 6, 6], [6, 8.05, 6], [6, 6, 8.05], [3.95, 6, 6],   # P, O, 3 bonded S
                   [2, 2, 2], [11.8, 2, 2], [9, 9, 3], [3, 9, 9]], float)               # free S, Cl, Li×2
    pos = np.repeat(p0[None], T, axis=0)
    cells = np.repeat((np.eye(3) * L)[None], T, axis=0)
    return sym, pos, cells


def _write_extxyz(path, sym, pos, cells):
    L = cells[0]
    lat = " ".join(f"{v:.4f}" for v in L.reshape(-1))
    with open(path, "w") as f:
        for t in range(len(pos)):
            f.write(f"{len(sym)}\n")
            f.write(f'Lattice="{lat}" Properties=species:S:1:pos:R:3\n')
            w = pos[t] % np.diag(L)                       # wrapped 좌표로 쓴다 (PBC 경로 검사)
            for s, r in zip(sym, w):
                f.write(f"{s} {r[0]:.5f} {r[1]:.5f} {r[2]:.5f}\n")


def _selftest():
    ok = bad = 0
    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += c; bad += (not c)
    dt = 0.1                                   # ps → min_frames = 100 (10 ps)
    sym, pos, cells = _base()
    t = np.arange(len(pos))
    r0 = census(sym, pos, cells, dt)
    chk(r0["verdict"] == "framework_rigid" and r0["n_P_bonded_anions"] == 4 and r0["n_free"] == 3,
        "정지 궤적: rigid · P 결합 음이온 4(O1+S3) · 자유 3(S, Cl, P)")
    # (i) O 진동 0.8 Å → 최대 2.3 < 2.5
    p = pos.copy(); p[:, 1, 0] = 6 + 1.5 + 0.8 * np.sin(2 * np.pi * t / 5.0)
    r = census(sym, p, cells, dt)
    chk(r["n_events"] == 0 and 2.2 < r["margin_max_by_elem_kind"]["O/P-bonded"]["max_A"] < 2.35,
        "⛔음성: 진폭 0.8 Å 진동은 이벤트 0 (최대 2.3 Å 는 여유 지표에 남는다)")
    # (ii) 5 ps 일시 이탈 → 0 · min_ps 0.5 면 1 (지속 필터가 걸러낸 것임을 증명)
    p = pos.copy(); p[200:250, 1, 0] = 6 + 3.0
    chk(census(sym, p, cells, dt)["n_events"] == 0, "⛔음성: 5 ps 일시 이탈(3.0 Å)은 이벤트 0")
    th2 = dict(DEFAULTS); th2["min_ps"] = 0.5
    chk(census(sym, p, cells, dt, th2)["n_events"] == 1, "지속 문턱을 0.5 ps 로 내리면 같은 궤적이 1 이벤트 — 필터가 작동한다")
    # (iii) O 3.5 Å 이동 후 유지 → 1 이벤트 O, 시작 20 ps
    p = pos.copy(); p[200:, 1, 0] = 6 + 3.5
    r = census(sym, p, cells, dt)
    chk(r["n_events"] == 1 and r["by_elem"] == {"O": {"events": 1, "n_atoms": 1, "atoms": [1]}}
        and abs(r["events"][0]["start_ps"] - 20.0) < 1e-9 and r["verdict"] == "framework_mobile",
        "⭕양성: O 가 P 에서 3.5 Å 로 떠나 유지 → 1 이벤트 (O · 시작 20 ps) · mobile")
    # (viii) 결합 S 2.8 Å 유지 → 0 (S 문턱 3.0) — 원소별 문턱이 갈린다
    p = pos.copy(); p[200:, 2, 1] = 6 + 2.8
    chk(census(sym, p, cells, dt)["n_events"] == 0, "⛔음성: 결합 S 가 2.8 Å 로 늘어나 유지해도 S 문턱 3.0 아래라 0")
    p = pos.copy(); p[200:, 2, 1] = 6 + 3.2
    chk(census(sym, p, cells, dt)["by_elem"].get("S", {}).get("events") == 1, "결합 S 3.2 Å 유지 → S 이벤트 1")
    # (iv) 자유 S 3 Å 병진 후 유지 → free 이벤트 1
    p = pos.copy(); p[100:, 5, 0] += 3.0
    r = census(sym, p, cells, dt)
    chk(r["n_events"] == 1 and r["events"][0]["kind"] == "free" and r["events"][0]["elem"] == "S",
        "⭕양성: 자유 S 가 3 Å 옮겨 유지 → free 이벤트 1")
    # (v) 골격 전체 병진 5 Å (COM drift) → 0
    p = pos.copy(); p[:, :, 0] += 5.0 * t[:, None] / len(t)
    chk(census(sym, p, cells, dt)["n_events"] == 0, "⛔음성: 골격 전체가 5 Å 병진(드리프트)해도 COM 제거로 0")
    # (vi) PBC: Cl 이 x=11.8±0.3 으로 경계를 넘나든다 (wrapped 좌표) → 0
    p = pos.copy(); p[:, 6, 0] = 11.8 + 0.3 * np.sin(2 * np.pi * t / 7.0); p = p % 12.0
    chk(census(sym, p, cells, dt)["n_events"] == 0, "⛔음성: 경계를 넘나드는 wrapped 좌표는 unwrap 으로 0")
    # (vii) extxyz 왕복 + 파일 경로 (CLI 가 타는 함수) → (iii) 재현
    p = pos.copy(); p[200:, 1, 0] = 6 + 3.5
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, "traj.xyz"); _write_extxyz(f, sym, p, cells)
        pathlib.Path(td, "aimd_results.json").write_text(json.dumps({"save_fs": 100.0}))
        r = census_file(f)
        chk(r["n_events"] == 1 and r["by_elem"]["O"]["events"] == 1 and abs(r["dt_ps"] - 0.1) < 1e-12,
            "extxyz 파일 경로 + aimd_results.json 의 save_fs 자동 읽기로 (iii) 재현")
        os.remove(os.path.join(td, "aimd_results.json"))
        try:
            census_file(f); ok_dt = False
        except SystemExit as e:
            ok_dt = "dt" in str(e)
        chk(ok_dt, "⛔음성: dt 를 모르면 멈춘다 (아무 값도 가정하지 않는다)")
    # (ix) 셀이 변하면 멈춘다
    c2 = cells.copy(); c2[300:] *= 1.01
    try:
        census(sym, pos, c2, dt); ok_cell = False
    except SystemExit as e:
        ok_cell = "NVT" in str(e)
    chk(ok_cell, "⛔음성: 셀이 프레임마다 다르면 SystemExit (NVT 전용)")
    # (x) 카드 문턱 읽기 = 기본값과 동일 (카드와 코드가 갈라지면 여기서 잡힌다)
    card = pathlib.Path(__file__).resolve().parents[2] / "db/properties/lpsocl_box331_closure_amendment_2026_09_11.json"
    if card.is_file():
        chk(read_thresholds(card) == DEFAULTS, "카드 §2 문턱_기계값 == 도구 기본값 (갈라지면 개정이 필요하다)")
    print(f"selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


# ── 온도별 사건 빈도 집계 (b2o3 사건빈도 카드 §보고량 · 2026-09-26) ─────────────────────────
#: 카드 `db/properties/b2o3_framework_event_rate_prereg_2026_09_23.json` §보고량·§판정_문구_봉인 을 그대로 옮긴다.
#:   원소군 = {P 중심 · 자유 S · Cl} = census 의 kind "free" 중 elem P · S · Cl. P 결합 음이온(kind "P-bonded")·자유 O 는
#:   카드 원소군 밖이라 **따로 기록**만 한다 (섞지 않는다 — PS₄ 깨짐과 P 중심 이동은 다른 사건이다).
#: ⛔ 못 하는 것: 원소군 원자수를 스스로 정하지 않는다 (--group_n 필수 · 카드 값) · 판정어를 만들지 않는다 (봉인 문장 틀에 수만 넣는다) ·
#:   겉보기 활성화는 카드 조건(10 사건 이상 온도 2 개 이상)이 아니면 **맞추지 않는다** · 이온 이동 장벽이라 부르지 않는다.
CARD_GROUPS = (("P_center", "free", "P"), ("S_free", "free", "S"), ("Cl", "free", "Cl"))
EXTRA_GROUPS = (("P-bonded_S", "P-bonded", "S"), ("P-bonded_O", "P-bonded", "O"), ("free_O", "free", "O"))
KB_EV = 8.617333262e-5


def _poisson_ci(n, exposure_ns):
    """정확 포아송(Garwood) 95 % — n > 0 이면 양측, n = 0 이면 단측 95 % 상한 (카드: '≈ 1.5 /ns/셀' @ 2 ns)."""
    from scipy.stats import chi2
    if n == 0:
        return {"lo": 0.0, "hi": float(chi2.ppf(0.95, 2) / 2.0 / exposure_ns), "kind": "one-sided 95 % upper (n = 0)"}
    return {"lo": float(chi2.ppf(0.025, 2 * n) / 2.0 / exposure_ns), "hi": float(chi2.ppf(0.975, 2 * n + 2) / 2.0 / exposure_ns), "kind": "Garwood two-sided 95 %"}


def _median_censored(vals, cap):
    """None = 절단(> cap). 중앙값이 절단 구간에 떨어지면 '> cap' 문자열 (0 이나 cap 으로 적지 않는다)."""
    xs = sorted(vals, key=lambda v: (v is None, v if v is not None else 0.0))
    n = len(xs)
    if n == 0:
        return None
    mid = [xs[(n - 1) // 2], xs[n // 2]]
    if any(m is None for m in mid):
        return f"> {cap:g}"
    return float(sum(mid) / 2.0)


def aggregate(files, group_n):
    """files = [(seed, T, path)] · group_n = {"P_center": 32, "S_free": 48, "Cl": 64} → 런별 · 온도별 표 + 봉인 문장."""
    import re
    missing = [g for g, _, _ in CARD_GROUPS if g not in group_n]
    if missing:
        raise SystemExit(f"⛔ --group_n 에 카드 원소군 원자수가 없다: {missing} (카드 §보고량 값을 준다 — 도구가 정하지 않는다)")
    runs = []
    for seed, T, p in files:
        r = json.loads(pathlib.Path(p).read_text())
        row = {"seed": seed, "T_K": T, "path": str(p), "n_frames": r["n_frames"], "dt_ps": r["dt_ps"], "total_ps": r["total_ps"],
               "n_free": r.get("n_free"), "n_P_bonded_anions": r.get("n_P_bonded_anions"), "verdict": r.get("verdict"), "groups": {}}
        for g, kind, el in CARD_GROUPS + EXTRA_GROUPS:
            ev = [e for e in r["events"] if e["kind"] == kind and e["elem"] == el]
            row["groups"][g] = {"N_ev": len(ev), "N_at": len({e["atom"] for e in ev}),
                                "t1_ps": (min(e["start_ps"] for e in ev) if ev else None)}
        runs.append(row)
    temps = sorted({r["T_K"] for r in runs})
    by_T = {}
    for T in temps:
        rs = [r for r in runs if r["T_K"] == T]
        expo = sum(r["total_ps"] for r in rs) / 1000.0
        cap = max(r["total_ps"] for r in rs)
        tab = {"n_runs": len(rs), "seeds": sorted(r["seed"] for r in rs), "exposure_ns": expo, "groups": {}}
        for g, _, _ in CARD_GROUPS + EXTRA_GROUPS:
            N = sum(r["groups"][g]["N_ev"] for r in rs); A = sum(r["groups"][g]["N_at"] for r in rs)
            k = sum(1 for r in rs if r["groups"][g]["N_ev"] > 0)
            ci = _poisson_ci(N, expo)
            per = [r["groups"][g]["N_ev"] for r in sorted(rs, key=lambda q: q["seed"])]
            mu = N / len(rs)
            disp = (float(np.var(per, ddof=1)) / mu) if (mu > 0 and len(rs) > 1) else None   # 분산/평균 — 포아송이면 ≈ 1 (서술용 · 판정 아님)
            ent = {"sum_N_ev": N, "rate_per_ns_cell": N / expo, "ci95": ci, "k_runs": k, "k_of": len(rs),
                   "t1_median_ps": _median_censored([r["groups"][g]["t1_ps"] for r in rs], cap), "sum_N_at": A,
                   "per_run_N_ev": per, "dispersion_index_var_over_mean": disp}
            if g in group_n:
                ent["moved_atom_fraction"] = A / (len(rs) * group_n[g])
            tab["groups"][g] = ent
        by_T[T] = tab
    # 겉보기 활성화 — 카드 조건: 사건 ≥ 10 인 온도가 2 개 이상 (그 온도들만 · 포아송 가중)
    act = {}
    for g, _, _ in CARD_GROUPS:
        pts = [(T, by_T[T]["groups"][g]["sum_N_ev"], by_T[T]["groups"][g]["rate_per_ns_cell"]) for T in temps if by_T[T]["groups"][g]["sum_N_ev"] >= 10]
        if len(pts) < 2:
            act[g] = {"fitted": False, "why": f"사건 ≥ 10 인 온도 {len(pts)} 개 < 2 — 카드 조건 미충족 · 맞추지 않는다"}
            continue
        x = np.array([1.0 / (KB_EV * T) for T, _, _ in pts]); y = np.log([rt for _, _, rt in pts]); w = np.array([float(n) for _, n, _ in pts])   # σ_ln = 1/√n → w = n
        W = w.sum(); xb = (w * x).sum() / W; yb = (w * y).sum() / W
        Sxx = (w * (x - xb) ** 2).sum(); slope = (w * (x - xb) * (y - yb)).sum() / Sxx
        icpt = yb - slope * xb; resid = y - (icpt + slope * x); chi2v = float((w * resid ** 2).sum()); dof = len(pts) - 2
        act[g] = {"fitted": True, "temps_K": [T for T, _, _ in pts], "Ea_apparent_eV": float(-slope), "sigma_eV": float(1.0 / math.sqrt(Sxx)),
                  "chi2": chi2v, "dof": dof, "reduced_chi2": (chi2v / dof if dof > 0 else None),
                  "fit_note": ("점 2 개 — 적합도 판단 불가 (dof 0)" if dof == 0 else ("χ²/dof ≫ 1 — 온도 의존이 단일 아레니우스와 안 맞는다 · σ 는 포아송만 반영" if chi2v / dof > 4 else "χ²/dof 정상 범위")),
                  "⛔": "사건 빈도의 겉보기 활성화 에너지 — 이온 이동 장벽이 아니다 (카드) · χ² 는 서술용 (카드 문턱 아님)"}
    # 봉인 문장 (카드 §판정_문구_봉인 틀 그대로)
    sent = []
    for T in temps:
        tab = by_T[T]
        if all(tab["groups"][g]["sum_N_ev"] == 0 for g, _, _ in CARD_GROUPS + EXTRA_GROUPS):
            sent.append(f"이 셀·이 프로토콜에서 {T:g} K 의 골격은 {tab['n_runs']} × {cap:g} ps 동안 자리를 떠나지 않았다 "
                        f"(사건 빈도 단측 95 % 상한 ≈ {tab['groups']['P_center']['ci95']['hi']:.1f} /ns/셀).")
            continue
        for g, _, _ in CARD_GROUPS:
            e = tab["groups"][g]
            if e["sum_N_ev"] == 0:
                sent.append(f"{T:g} K · {g}: 사건 0 ({tab['n_runs']} × {cap:g} ps · 단측 95 % 상한 ≈ {e['ci95']['hi']:.2f} /ns/셀).")
            else:
                sent.append(f"{T:g} K 에서 {g} 사건 빈도는 {e['rate_per_ns_cell']:.2f} /ns/셀 [{e['ci95']['lo']:.2f}, {e['ci95']['hi']:.2f}] 이고 "
                            f"{tab['n_runs']}런 중 {e['k_runs']} 런에서 났다.")
    for g, a in act.items():
        if a["fitted"]:
            sent.append(f"{g}: 사건 빈도의 겉보기 활성화 에너지 {a['Ea_apparent_eV']:.2f} ± {a['sigma_eV']:.2f} eV ({'/'.join(f'{t:g}' for t in a['temps_K'])} K · 포아송 가중) — 이온 이동 장벽이 아니다.")
    return {"schema": "framework_event_rate_aggregate/v1", "group_definition": {g: f"census kind={k} · elem={e}" for g, k, e in CARD_GROUPS + EXTRA_GROUPS},
            "group_n_card": group_n, "runs": runs, "by_T": {f"{T:g}": v for T, v in by_T.items()}, "apparent_activation": act, "sealed_sentences": sent,
            "⚠": "census 는 P 중심 규칙 — B 를 안 세고 BS₃ 의 S 는 '자유 S' 로 분류된다 (카드 결과와 같이 적는다)"}


def _files_from_root(root):
    import re
    out = []
    for p in sorted(pathlib.Path(root).rglob("site_census.json")):
        m = re.search(r"/s(\d+)/(?:d[\d.]+_cfg\d+/)?T(\d+)/site_census\.json$", str(p))
        if m:
            out.append((int(m.group(1)), float(m.group(2)), p))
    return out


def _selftest_aggregate():
    import tempfile
    ok = bad = 0
    def ck(c, m):
        nonlocal ok, bad
        if c:
            ok += 1
        else:
            bad += 1; print("  ✗", m)
    from scipy.stats import chi2
    with tempfile.TemporaryDirectory() as td:
        def put(seed, T, events):
            d = pathlib.Path(td, f"s{seed}", f"T{T}"); d.mkdir(parents=True, exist_ok=True)
            (d / "site_census.json").write_text(json.dumps({"n_frames": 4000, "dt_ps": 0.1, "total_ps": 400.0, "n_free": 144, "n_P_bonded_anions": 128,
                                                             "verdict": "framework_mobile" if events else "framework_rigid", "events": events}))
        ev = lambda kind, el, atom, t: {"kind": kind, "elem": el, "atom": atom, "start_ps": t}
        for s in range(2, 7):
            put(s, 600, [])                                                               # 600 K: 사건 0
        cnt = {2: 3, 3: 4, 4: 0, 5: 2, 6: 3}                                              # 650 K: P 중심 12 사건 (4 런)
        for s, n in cnt.items():
            put(s, 650, [ev("free", "P", 100 + i, 50.0 * (i + 1)) for i in range(n)] + ([ev("P-bonded", "S", 7, 10.0)] if s == 2 else []))
        for s in range(2, 7):                                                             # 700 K: P 중심 30 사건 · 자유 S 1
            put(s, 700, [ev("free", "P", 200 + i, 20.0 * (i + 1)) for i in range(6)] + ([ev("free", "S", 300, 5.0)] if s == 3 else []))
        files = _files_from_root(td)
        ck(len(files) == 15, f"경로에서 시드·온도 15 개를 읽는다 — {len(files)}")
        r = aggregate(files, {"P_center": 32, "S_free": 48, "Cl": 64})
        z = r["by_T"]["600"]["groups"]["P_center"]
        ck(z["sum_N_ev"] == 0 and abs(z["ci95"]["hi"] - 1.4979) < 1e-3 and z["t1_median_ps"] == "> 400", f"사건 0: 단측 95 % 상한 ≈ 1.5 /ns (카드) · t₁ '> 400' — {z}")
        ck(any("600 K 의 골격은 5 × 400 ps 동안 자리를 떠나지 않았다" in s for s in r["sealed_sentences"]), "봉인 문장: 사건 0 인 온도")
        m = r["by_T"]["650"]["groups"]["P_center"]
        ck(m["sum_N_ev"] == 12 and abs(m["rate_per_ns_cell"] - 6.0) < 1e-12 and m["k_runs"] == 4 and abs(m["ci95"]["lo"] - chi2.ppf(0.025, 24) / 4) < 1e-9 and abs(m["ci95"]["hi"] - chi2.ppf(0.975, 26) / 4) < 1e-9,
           f"650 K: 12 사건 / 2 ns = 6.0 · Garwood · k 4/5 — {m['rate_per_ns_cell']} {m['k_runs']}")
        ck(m["t1_median_ps"] == 50.0 and abs(m["moved_atom_fraction"] - 12 / 160) < 1e-12, f"t₁ 중앙값 50 (절단 1 개 포함) · 움직인 원자 12/(5×32) — {m['t1_median_ps']}")
        ck(r["by_T"]["650"]["groups"]["P-bonded_S"]["sum_N_ev"] == 1 and r["by_T"]["650"]["groups"]["S_free"]["sum_N_ev"] == 0, "⛔음성: P 결합 S 이탈은 자유 S 로 안 섞인다 (따로 기록)")
        s7 = r["by_T"]["700"]["groups"]["S_free"]
        ck(s7["sum_N_ev"] == 1 and s7["t1_median_ps"] == "> 400", f"⛔음성: 절단 4/5 → t₁ 중앙값 '> 400' — {s7['t1_median_ps']}")
        a = r["apparent_activation"]
        ck(a["P_center"]["fitted"] and a["P_center"]["temps_K"] == [650.0, 700.0] and a["S_free"]["fitted"] is False, f"겉보기 활성화: P 중심만 (650·700 K ≥ 10 사건) · 자유 S 는 조건 미충족 — {a['S_free']}")
        x = 1 / (KB_EV * 650) - 1 / (KB_EV * 700); ck(abs(a["P_center"]["Ea_apparent_eV"] - math.log(15.0 / 6.0) / x) < 1e-9, "두 점이면 Ea = ln(r2/r1)/Δ(1/kT) 로 정확히")
        ck(m["per_run_N_ev"] == [3, 4, 0, 2, 3] and abs(m["dispersion_index_var_over_mean"] - (float(np.var([3, 4, 0, 2, 3], ddof=1)) / 2.4)) < 1e-12 and z["dispersion_index_var_over_mean"] is None,
           "런별 사건 수 · 분산/평균(서술용) · 사건 0 이면 None (0 으로 안 적는다)")
        ck(a["P_center"]["dof"] == 0 and a["P_center"]["reduced_chi2"] is None and "dof 0" in a["P_center"]["fit_note"], "점 2 개 적합은 χ²/dof 를 None 으로 (판단 불가 표기)")
        try:
            aggregate(files, {"P_center": 32}); badg = False
        except SystemExit:
            badg = True
        ck(badg, "⛔음성: --group_n 에 카드 원소군이 빠지면 멈춘다 (도구가 원자수를 정하지 않는다)")
    print(f"{'✅' if not bad else '⛔'} aggregate selftest {ok}/{ok + bad}")
    return bad


def main():
    ap = argparse.ArgumentParser(description="C6 원자별 자리 이탈 census (개정안 §2)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--traj", help="extxyz 궤적 (Lattice 필수)")
    ap.add_argument("--dt_ps", type=float, help="프레임 간격 ps (없으면 옆의 aimd_results.json 의 save_fs)")
    ap.add_argument("--card", help="문턱을 읽을 개정안 카드 (없으면 기본값 + 경고)")
    ap.add_argument("--out", help="결과 JSON")
    ap.add_argument("--aggregate", metavar="ROOT", help="ROOT 아래 s<seed>/[d…_cfg…/]T<K>/site_census.json 을 모아 온도별 사건 빈도 (b2o3 사건빈도 카드 §보고량)")
    ap.add_argument("--group_n", help="카드 원소군 원자수 (필수 · 예: P_center=32,S_free=48,Cl=64)")
    a = ap.parse_args()
    if a.selftest:
        rc = _selftest()
        rc2 = _selftest_aggregate()
        raise SystemExit(rc or (1 if rc2 else 0))
    if a.aggregate:
        if not a.group_n:
            ap.error("--aggregate 에는 --group_n 이 필요하다 (카드 원소군 원자수)")
        gn = {k.strip(): int(v) for k, v in (x.split("=") for x in a.group_n.split(","))}
        files = _files_from_root(a.aggregate)
        if not files:
            raise SystemExit(f"⛔ {a.aggregate} 아래 site_census.json 이 없다")
        r = aggregate(files, gn)
        print(f"런 {len(files)} · 온도 {list(r['by_T'].keys())}")
        print(f"{'T':>5s} {'group':>11s} {'ΣN_ev':>6s} {'rate/ns':>8s} {'95% CI':>17s} {'k/n':>5s} {'t1 med':>8s} {'moved':>7s}")
        for T, tab in r["by_T"].items():
            for g, e in tab["groups"].items():
                ci = e["ci95"]; t1 = e["t1_median_ps"]
                t1s = t1 if isinstance(t1, str) else f"{t1:.1f}"
                mv = f"{e['moved_atom_fraction']:.3f}" if "moved_atom_fraction" in e else "—"
                print(f"{T:>5s} {g:>11s} {e['sum_N_ev']:6d} {e['rate_per_ns_cell']:8.2f} [{ci['lo']:6.2f}, {ci['hi']:6.2f}] {e['k_runs']}/{e['k_of']:<3d} {t1s:>8s} {mv:>7s}")
        for s in r["sealed_sentences"]:
            print("  ·", s)
        if a.out:
            pathlib.Path(a.out).write_text(json.dumps(r, ensure_ascii=False, indent=1, default=str) + "\n"); print(f"-> {a.out}")
        return
    if not a.traj:
        ap.error("--traj 가 필요하다 (--selftest 제외)")
    if a.card:
        th = read_thresholds(a.card); print(f"문턱 ← {pathlib.Path(a.card).name}: {th}")
    else:
        th = dict(DEFAULTS); print(f"⚠ 문턱을 카드가 아니라 기본값에서 썼다: {th} — 판정 기록에는 --card 로 다시.")
    r = census_file(a.traj, a.dt_ps, th)
    r["traj"] = str(a.traj); r["card"] = a.card
    print(f"[{a.traj}] frames={r['n_frames']} dt={r['dt_ps']} ps total={r['total_ps']:.1f} ps · 골격 {r['n_framework']} "
          f"(P결합 음이온 {r['n_P_bonded_anions']} · 자유 {r['n_free']})")
    print(f"  ★ 판정: **{r['verdict']}** · 이벤트 {r['n_events']}")
    for k, v in r["by_elem"].items():
        print(f"    {k}: {v['events']} 이벤트 · 원자 {v['n_atoms']}개 {v['atoms'][:10]}")
    for k, v in sorted(r["margin_max_by_elem_kind"].items()):
        print(f"    여유 {k}: 최대 {v['max_A']:.2f} Å / 문턱 {v['escape_A']} Å (원자 {v['atom']})")
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n")
        print(f"-> {a.out}")


if __name__ == "__main__":
    main()
