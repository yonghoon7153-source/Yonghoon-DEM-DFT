#!/usr/bin/env python3
"""quench_ss_event.py — 담금질 궤적(traj.xyz + thermo.csv)에서 **S–S 근접 사건**을 프레임별로 추적한다.

왜 (회신 CC · 2026-09-26 · 외부 1저자 Q9): seed5 의 final 에서 PS₄ 하나가 깨지고 S–S 2.03 Å 가 남았다.
  *"먼저 그 S–S 가 무엇인지 확인하세요 — 담금질 궤적에서 언제 생겼는지(고온 구간인지 냉각 말미인지),
   끝까지 유지되는지, 4배위를 잃은 P 가 PS₃ 인지 다리를 공유하는 형태인지."* 궤적이 있으니 비용 ≈ 0.

무엇을 재나 (프레임마다)
  · 최단 S–S 거리(최소상) 와 그 쌍 · 쌍의 두 S 가 P 에 결합돼 있는지(R_PS 2.6 Å · melt_quench_uma.indicators 와 같은 컷)
    → 형태 (쌍의 두 S 가 각각 P 에 붙어 있는가로만 가른다): `P-S-S-P`(둘 다 = 과황화 다리) · `P-S-S`(한쪽만 = 말단 과황화,
      P–S–S) · `S-S_free`(둘 다 P 없음 = 떨어져 나온 S₂) · `none`(컷 위). PS₃ 가 생겼는지는 별도 열 `P_not_4coord` 로 본다 —
      seed5 의 질문("4배위를 잃은 P 가 PS₃ 인지 다리를 공유하는 형태인지")은 이 둘을 같이 읽어야 답이 된다.
  · PS₄ 보존율 · P–S 배위 분포 · 다리 S(P 2개 이상에 붙은 S) · 4배위 아닌 P 목록  (전부 indicators 재사용)
  · 온도: thermo.csv 의 T_K(순간) · T_set_K(설정) — 프레임 ↔ thermo 행 대응은 frame_index_map 규칙(개수 같아야 함)
사건 판정
  · onset = 최단 S–S 가 --ss_cut(기본 2.30 Å) 아래로 **처음** 들어간 프레임 · 그때의 쌍을 고정하고 이후 프레임에서
    **같은 쌍**의 거리를 추적 → 지속 분율 · 마지막 프레임 유지 여부 · 쌍이 바뀐 횟수
  · 구간 라벨: T_set 이 최고값이면 `melt_hold` · 최저값이면 `final_hold` · 그 사이면 `quench`

⛔ 이 도구가 **못 하는 것**
  · 결합인지 판정하지 않는다 — 거리 기준이다 (2.30 Å 는 S–S 공유결합 2.03–2.10 과 비결합 최근접 ≥ 3.3 사이의 창).
    전자구조(결합 차수)는 안 본다. 보고에는 "거리 2.03 Å" 로만 쓴다 (회신 CC).
  · 게이트를 판정하지 않는다 — 판정은 외부 1저자 몫. 개수·시각·형태를 옮길 뿐이다.
  · thermo 행 수와 프레임 수가 다르면 시간축을 **plan.json 의 save_ps 로 가정**하고 그 사실을 기록한다(조용히 넘어가지 않는다).
  · 저장 간격(save_ps) 사이의 사건은 못 본다.

사용
  python3 tools/ionic/quench_ss_event.py <run_dir> [--ss_cut 2.30] [--stride 1] [--table 50] [--out JSON] [--tools_dir DIR]
  python3 tools/ionic/quench_ss_event.py --selftest
"""
import argparse
import json
import math
import os
import pathlib
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SS_CUT = 2.30


def _load_mq(tools_dir=None):
    """melt_quench_uma 의 indicators · mic_dists · read_thermo · R_PS 를 빌린다 (컷오프를 여기 복사하지 않는다)."""
    d = tools_dir or HERE
    if d not in sys.path:
        sys.path.insert(0, d)
    import melt_quench_uma as mq  # noqa: E402
    return mq


def frame_stats(sym, pos, cell, mq, ss_cut=SS_CUT):
    sym = np.asarray(sym); pos = np.asarray(pos, float); cell = np.asarray(cell, float)
    ind = mq.indicators(sym, pos, cell)
    iS = np.where(sym == "S")[0]; iP = np.where(sym == "P")[0]
    out = {"PS4_fraction": ind.get("PS4_fraction"), "P_S_coord_hist": ind.get("P_S_coord_hist"),
           "bridging_S": ind.get("bridging_S_P2S7_like"), "P_P_bonds": ind.get("P_P_bonds_P2S6_like")}
    if len(iS) < 2:
        out.update({"ss_min_A": None, "ss_pair": None, "ss_kind": "n/a"})
        return out
    D = mq.mic_dists(pos[iS], pos[iS], cell); np.fill_diagonal(D, np.inf)
    a, b = np.unravel_index(int(np.argmin(D)), D.shape)
    dmin = float(D[a, b]); i, j = int(iS[a]), int(iS[b])
    pair = (min(i, j), max(i, j))
    kind = "none"
    p_of = {}
    if len(iP):
        DPS = mq.mic_dists(pos[iP], pos[iS], cell)          # (nP, nS)
        nS_per_P = (DPS <= mq.R_PS).sum(axis=1)
        out["P_not_4coord"] = [[int(iP[k]), int(n)] for k, n in enumerate(nS_per_P) if n != 4]
        for s_loc, s_glob in ((a, i), (b, j)):
            p_of[s_glob] = [int(iP[k]) for k in np.where(DPS[:, s_loc] <= mq.R_PS)[0]]
        if dmin < ss_cut:
            has = [len(p_of[i]) > 0, len(p_of[j]) > 0]
            kind = "P-S-S-P" if all(has) else ("P-S-S" if any(has) else "S-S_free")
    else:
        out["P_not_4coord"] = []
        if dmin < ss_cut:
            kind = "S-S_free"
    out.update({"ss_min_A": round(dmin, 4), "ss_pair": list(pair), "ss_kind": kind,
                "ss_pair_P_neighbors": {str(k): v for k, v in p_of.items()}})
    return out


def _segment(tset, tmax, tmin, tol=1.0):
    if tset is None:
        return "unknown"
    if abs(tset - tmax) <= tol:
        return "melt_hold"
    if abs(tset - tmin) <= tol:
        return "final_hold"
    return "quench"


def analyze(run_dir, mq, ss_cut=SS_CUT, stride=1, log=print):
    from ase.io import iread
    run = pathlib.Path(run_dir)
    traj, thermo = run / "traj.xyz", run / "thermo.csv"
    if not traj.exists():
        raise FileNotFoundError(f"{traj} 가 없다 — 궤적 없이는 못 잰다")
    t_axis, T_K, T_set, axis_note = None, None, None, ""
    try:
        imap, n_traj = mq.frame_index_map(traj, thermo)
        th = mq.read_thermo(thermo)
        t_axis = [float(x) for x in th["t_ps"]]
        T_K = [float(x) for x in th["T_K"]] if "T_K" in th else None
        T_set = [float(x) for x in th["T_set_K"]] if "T_set_K" in th else None
        axis_note = f"thermo.csv 행 {n_traj} = 프레임 {n_traj} (frame_index_map)"
    except (ValueError, FileNotFoundError, KeyError) as e:
        n_traj = sum(1 for _ in iread(str(traj), index=":", format="extxyz"))
        save_ps = None
        pj = run / "plan.json"
        if pj.exists():
            try:
                plan = json.loads(pj.read_text(encoding="utf-8"))
                save_ps = plan.get("save_ps") or (plan.get("md") or {}).get("save_ps")
            except Exception:
                save_ps = None
        if not save_ps:
            raise ValueError(f"⛔ 시간축을 만들 수 없다 — {e} · plan.json 의 save_ps 도 없다")
        t_axis = [k * float(save_ps) for k in range(n_traj)]
        axis_note = f"⚠ thermo 대응 실패({e}) → t = 프레임 × save_ps {save_ps} ps **가정** · 온도 열 없음"
    tmax = max(T_set) if T_set else None; tmin = min(T_set) if T_set else None
    rows = []
    onset = None; pair0 = None; switches = 0; last_pair = None
    for k, at in enumerate(iread(str(traj), index=":", format="extxyz")):
        if k % stride:
            continue
        sym, pos, cell = at.get_chemical_symbols(), at.get_positions(), np.asarray(at.get_cell())
        st = frame_stats(sym, pos, cell, mq, ss_cut)
        d_pair0 = None
        if pair0 is not None:
            d_pair0 = float(mq.mic_dists(pos[[pair0[0]]], pos[[pair0[1]]], cell)[0, 0])
        row = {"frame": k, "t_ps": t_axis[k] if k < len(t_axis) else None,
               "T_K": (T_K[k] if T_K and k < len(T_K) else None), "T_set_K": (T_set[k] if T_set and k < len(T_set) else None),
               "segment": _segment(T_set[k] if T_set and k < len(T_set) else None, tmax, tmin),
               **st, "d_onset_pair_A": (round(d_pair0, 4) if d_pair0 is not None else None)}
        if st["ss_min_A"] is not None and st["ss_min_A"] < ss_cut:
            if onset is None:
                onset, pair0 = k, tuple(st["ss_pair"]); last_pair = pair0
                row["d_onset_pair_A"] = st["ss_min_A"]
            elif tuple(st["ss_pair"]) != last_pair:
                switches += 1; last_pair = tuple(st["ss_pair"])
        rows.append(row)
    res = {"run_dir": str(run), "n_frames": n_traj, "stride": stride, "ss_cut_A": ss_cut, "R_PS_A": mq.R_PS, "time_axis": axis_note,
           "rows": rows, "onset": None}
    ps4_first_drop = next((r for r in rows if r["PS4_fraction"] is not None and r["PS4_fraction"] < 1.0 - 1e-9), None)
    res["PS4_first_below_1"] = ({"frame": ps4_first_drop["frame"], "t_ps": ps4_first_drop["t_ps"], "T_set_K": ps4_first_drop["T_set_K"],
                                 "segment": ps4_first_drop["segment"], "PS4_fraction": ps4_first_drop["PS4_fraction"]} if ps4_first_drop else None)
    if onset is not None:
        after = [r for r in rows if r["frame"] >= onset]
        held = [r for r in after if r["d_onset_pair_A"] is not None and r["d_onset_pair_A"] < ss_cut]
        o = rows[[r["frame"] for r in rows].index(onset)]
        last = rows[-1]
        res["onset"] = {"frame": onset, "t_ps": o["t_ps"], "T_K": o["T_K"], "T_set_K": o["T_set_K"], "segment": o["segment"],
                        "pair": list(pair0), "d_A": o["ss_min_A"], "kind": o["ss_kind"], "P_neighbors_of_pair": o["ss_pair_P_neighbors"],
                        "P_not_4coord_at_onset": o.get("P_not_4coord")}
        res["persistence"] = {"frames_after_onset": len(after), "frames_pair_below_cut": len(held),
                              "fraction": round(len(held) / len(after), 4) if after else None,
                              "last_frame_pair_d_A": last["d_onset_pair_A"], "last_frame_below_cut": (last["d_onset_pair_A"] is not None and last["d_onset_pair_A"] < ss_cut),
                              "last_frame_kind": last["ss_kind"], "pair_switches_after_onset": switches,
                              "longest_gap_frames_above_cut": _longest_gap([r["d_onset_pair_A"] for r in after], ss_cut)}
        kinds = {}
        for r in after:
            kinds[r["ss_kind"]] = kinds.get(r["ss_kind"], 0) + 1
        res["kind_histogram_after_onset"] = kinds
    res["summary"] = _summary(res)
    for ln in res["summary"]:
        log(ln)
    return res


def _longest_gap(ds, cut):
    best = cur = 0
    for d in ds:
        if d is None or d >= cut:
            cur += 1; best = max(best, cur)
        else:
            cur = 0
    return best


def _summary(res):
    L = [f"프레임 {res['n_frames']} · 컷 S–S < {res['ss_cut_A']} Å · P–S 배위 컷 {res['R_PS_A']} Å · 시간축: {res['time_axis']}"]
    p = res.get("PS4_first_below_1")
    L.append("PS₄ 보존율 < 1 첫 프레임: " + (f"#{p['frame']} t={p['t_ps']} ps · T_set={p['T_set_K']} · {p['segment']} · 값 {p['PS4_fraction']:.4f}" if p else "없음 (전 구간 1.0)"))
    o = res.get("onset")
    if not o:
        L.append("S–S 근접 사건: **없음** (전 프레임 최단 S–S ≥ 컷)")
        return L
    L.append(f"S–S onset: #{o['frame']} t={o['t_ps']} ps · T={o['T_K']} K (설정 {o['T_set_K']}) · 구간 **{o['segment']}** · 쌍 {o['pair']} · d {o['d_A']} Å · 형태 **{o['kind']}** · 쌍의 P 이웃 {o['P_neighbors_of_pair']}")
    pr = res["persistence"]
    L.append(f"지속: onset 뒤 {pr['frames_after_onset']} 프레임 중 {pr['frames_pair_below_cut']} 에서 같은 쌍 < 컷 (분율 {pr['fraction']}) · 마지막 프레임 d={pr['last_frame_pair_d_A']} Å ({'유지' if pr['last_frame_below_cut'] else '해소'}) · 쌍 교체 {pr['pair_switches_after_onset']} 회 · 컷 위 최장 연속 {pr['longest_gap_frames_above_cut']} 프레임")
    L.append(f"형태 분포(onset 뒤): {res.get('kind_histogram_after_onset')}")
    return L


# ───────────────────────── selftest ─────────────────────────
def _synthetic(tmpdir, event=True, thermo_rows=None):
    """PS₄ 1 개 + 자유 S 1 + Li 4 · 12 Å 셀 · 10 프레임.
    event="detach"(=True): 5 프레임부터 S0 가 P 를 떠나 자유 S 옆(2.05 Å)으로 → PS₃ + `S-S_free`
    event="attach": 5 프레임부터 자유 S 가 결합 S1 옆(2.05 Å)으로 → PS₄ 그대로 + `P-S-S`
    event=False: 사건 없음"""
    from ase import Atoms
    from ase.io import write
    L = 12.0
    P = np.array([6.0, 6.0, 6.0]); v = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(3) * 2.05
    Sfree = np.array([1.5, 1.5, 1.5]); Li = np.array([[3, 9, 3], [9, 3, 9], [9, 9, 3], [3, 3, 9]], float)
    run = pathlib.Path(tmpdir); (run / "traj.xyz").unlink(missing_ok=True)
    rows = []
    for k in range(10):
        S = P + v; Sf = Sfree.copy()
        if event and k >= 5:
            if event == "attach":
                Sf = S[0] + (S[0] - P) / np.linalg.norm(S[0] - P) * 2.05   # 자유 S 가 결합 S0 바깥쪽 2.05 Å 로 (P–S0 2.05 · P–Sf 4.10 > R_PS)
            else:
                S[0] = Sfree + np.array([2.05, 0, 0])                        # S0 가 자유 S 옆으로 (P 에서 멀어짐)
        at = Atoms(["P"] + ["S"] * 4 + ["S"] + ["Li"] * 4, positions=np.vstack([P, S, Sf, Li]), cell=np.eye(3) * L, pbc=True)
        write(str(run / "traj.xyz"), at, format="extxyz", append=True)
        rows.append(k)
    n_th = len(rows) if thermo_rows is None else thermo_rows
    with open(run / "thermo.csv", "w") as f:
        f.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
        for k in range(n_th):
            tset = 1200.0 if k < 3 else (300.0 if k >= 8 else 1200.0 - (k - 2) * 180.0)
            f.write(f"{k*1.0:.3f},{tset+3:.1f},{tset:.1f},1.6,1728,0,0,0\n")
    json.dump({"save_ps": 1.0}, open(run / "plan.json", "w"))
    return run


def _selftest():
    import tempfile
    mq = _load_mq(); ok = bad = 0
    def ck(c, m):
        nonlocal ok, bad
        if c:
            ok += 1
        else:
            bad += 1; print("  ✗", m)
    with tempfile.TemporaryDirectory() as td:
        r = analyze(_synthetic(td, event="detach"), mq, log=lambda *a: None)
        o = r["onset"]
        ck(o is not None and o["frame"] == 5 and o["kind"] == "S-S_free" and o["segment"] == "quench", f"떨어짐: 5 프레임 onset · S-S_free · 냉각 중 — {o}")
        ck(o and abs(o["d_A"] - 2.05) < 1e-3 and set(o["pair"]) == {1, 5}, f"쌍 = (S1, 자유 S5) · d 2.05 — {o and o['pair']}")
        ck(r["persistence"]["fraction"] == 1.0 and r["persistence"]["last_frame_below_cut"] and r["persistence"]["pair_switches_after_onset"] == 0, "지속 1.0 · 마지막 유지 · 교체 0")
        ck(r["PS4_first_below_1"] and r["PS4_first_below_1"]["frame"] == 5 and o["P_not_4coord_at_onset"] == [[0, 3]], "PS₄ < 1 첫 프레임 5 · P0 가 3 배위 (PS₃)")
        ck(r["rows"][0]["segment"] == "melt_hold" and r["rows"][-1]["segment"] == "final_hold", "구간 라벨: 처음 melt_hold · 끝 final_hold")
    with tempfile.TemporaryDirectory() as td:
        ra = analyze(_synthetic(td, event="attach"), mq, log=lambda *a: None)
        oa = ra["onset"]
        ck(oa is not None and oa["frame"] == 5 and oa["kind"] == "P-S-S" and ra["PS4_first_below_1"] is None and oa["P_not_4coord_at_onset"] == [],
           f"붙음: 자유 S 가 결합 S 옆으로 → P-S-S(말단 과황화) · PS₄ 는 1.0 유지 · PS₃ 없음 — {oa}")
    with tempfile.TemporaryDirectory() as td:
        r0 = analyze(_synthetic(td, event=False), mq, log=lambda *a: None)
        ck(r0["onset"] is None and r0["PS4_first_below_1"] is None, "⛔음성: 사건 없는 궤적 → onset None · PS₄ 1.0 유지")
    with tempfile.TemporaryDirectory() as td:
        r1 = analyze(_synthetic(td, event="detach", thermo_rows=7), mq, log=lambda *a: None)
        ck(r1["time_axis"].startswith("⚠") and r1["rows"][0]["T_K"] is None and r1["onset"]["frame"] == 5, "⛔음성: thermo 행 수 ≠ 프레임 → save_ps 가정 표기 · 온도 없음(0 아님)")
    with tempfile.TemporaryDirectory() as td:
        run = _synthetic(td, event="detach"); (run / "thermo.csv").unlink(); (run / "plan.json").unlink()
        try:
            analyze(run, mq, log=lambda *a: None); bad_ = False
        except ValueError:
            bad_ = True
        ck(bad_, "⛔음성: thermo 도 plan.json 도 없으면 시간축을 지어내지 않고 죽는다")
    print(f"{'✅' if not bad else '⛔'} quench_ss_event selftest {ok}/{ok + bad}")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("run_dir", nargs="?")
    ap.add_argument("--ss_cut", type=float, default=SS_CUT)
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--table", type=int, default=0, help="N 프레임마다 한 줄 표 (0 = 안 찍음)")
    ap.add_argument("--out")
    ap.add_argument("--tools_dir", help="melt_quench_uma.py 가 있는 폴더 (기본 = 이 파일 폴더)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.run_dir:
        ap.error("run_dir 이 필요하다")
    mq = _load_mq(a.tools_dir)
    res = analyze(a.run_dir, mq, a.ss_cut, a.stride)
    if a.table:
        print(f"{'frame':>6s} {'t_ps':>8s} {'T_set':>7s} {'seg':>10s} {'PS4':>6s} {'ssmin':>6s} {'pair':>10s} {'kind':>9s} {'d_onset':>7s}")
        for r in res["rows"]:
            if r["frame"] % a.table == 0 or (res["onset"] and abs(r["frame"] - res["onset"]["frame"]) <= 2):
                print(f"{r['frame']:6d} {r['t_ps'] if r['t_ps'] is not None else float('nan'):8.1f} {r['T_set_K'] if r['T_set_K'] is not None else float('nan'):7.0f} {r['segment']:>10s} "
                      f"{r['PS4_fraction']:6.3f} {r['ss_min_A']:6.3f} {str(r['ss_pair']):>10s} {r['ss_kind']:>9s} {r['d_onset_pair_A'] if r['d_onset_pair_A'] is not None else float('nan'):7.3f}")
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
